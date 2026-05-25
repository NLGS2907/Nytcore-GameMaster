"""The module for holding the GameMaster."""

from io import BytesIO
from logging import DEBUG, getLogger
from os import getenv
from platform import system
from typing import TYPE_CHECKING, TypeAlias, Union

from discord import Intents, Permissions
from discord.abc import User  # NOT the same as `discord.User`
from discord.ext.commands import Bot
from discord.utils import utcnow

from .db import db, run_migrations
from .files import search_files
from .logger import add_file_handler, add_terminal_handler, get_gamemaster_logger, log_lvl
from .models import IMG_FORMAT
from .repositories import PlayerRepository, RepositoryConfiguration

if TYPE_CHECKING:
    from datetime import datetime, timedelta
    from logging import Logger

    from discord import Emoji

# suppress weird Windows warning
try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy
    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except ImportError:
    get_gamemaster_logger().warning("Could not import 'WindowsSelectorEventLoopPolicy', "
                                    "probably because this is not Windows.")

VersionTuple: TypeAlias = tuple[int, int, int]

COGS_PATH: str = "./gamemaster/cogs"
EmojisMap: TypeAlias = dict[str, "Emoji"]


class GameMaster(Bot):
    """The bot class for the GameMaster.
    
    Attributes:
        booted_at: A timestamp to know when was the bot booted up.
        log: A comfortable reference to the custom logger. Besides this one, one can always
             retrieve it using `getLogger()` with the bot namespace.
        ds_log: A reference to a secondary, special logger used by the discord.py library itself. 
    """

    def __init__(self, verbose: bool=True, **options):
        """Initializes the GameMaster.
        
        Args:
            verbose: Elevates the log level to show everything.
            **options: Extra options to pass on to the parent initializer.
        """

        super().__init__("!", # Deprecated, but legacy syntax requires it
                         intents=GameMaster.preferred_intents(),
                         application_id=getenv("BOT_ID"),
                         options=options)

        self.repositories: RepositoryConfiguration = RepositoryConfiguration(
            player_repository=PlayerRepository()
        )
        self._verbose: bool = verbose
        self.booted_at: "datetime" = utcnow()
        self._emojis: EmojisMap = {}
        log_level = log_lvl(self._verbose)

        self.log: "Logger" = get_gamemaster_logger(log_level)
        self.ds_log: "Logger" = getLogger("discord")
        self.ds_log.setLevel(DEBUG)
        add_terminal_handler(self.ds_log, console_level=log_level)
        add_file_handler(self.ds_log)

        self.db_log: "Logger" = getLogger("peewee")
        self.db_log.setLevel(DEBUG)
        add_terminal_handler(self.db_log, console_level=log_level)
        add_file_handler(self.db_log)

        self.db_migrate_log: "Logger" = getLogger("peewee_migrate")
        self.db_migrate_log.setLevel(DEBUG)
        add_terminal_handler(self.db_migrate_log, console_level=log_level)
        add_file_handler(self.db_migrate_log)


    @staticmethod
    def version() -> VersionTuple:
        """Returns the version information as a tuple.
        
        The format is (X, Y, Z) where:
        * X is the major patch
        * Y is a minor patch
        * Z is a small fix
        """

        return (0, 0, 1)

    @staticmethod
    def preferred_intents() -> Intents:
        """Reports the event buses that the gamemaster intends to subscribe to."""

        return Intents.all()


    @staticmethod
    def preferred_permissions() -> Permissions:
        """Reports the preferred perms that the bot intends to ask for.
        
        The layout of the perms is designed to reflect that of the developer portal.
        """

        perms = Permissions.none()

        perms.update(
            # General Perms
            view_channel=True,
            # ...
            view_guild_insights=True,
            # --------------------

            # Text Perms
            send_messages=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            # ...
            manage_messages=True,
            pin_messages=True,
            manage_threads=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            # ...
            use_external_emojis=True,
            use_external_stickers=True,
            add_reactions=True,
            use_application_commands=True,
            # ...
            use_external_apps=True,
            create_polls=True
            # --------------------
        )

        return perms


    async def setup_hook(self):
        """Initial actions to do before the bot fully wakes up."""

        run_migrations()
        await self.update_cogs(sync=True)
        await self.fetch_emojis()


    async def update_cogs(self, *, sync: bool=True):
        """Dynamically loads or reloads the cogs in the extensions directory.
        
        Args:
            sync: A boolean value indicating if it should sync the modules here discovered with
                  the server's command tree. This is usually not recommended when the changes
                  are within the logic of a command. If the commands' syntax is altered or a new
                  one is added then yes, it needs to sync.
        """

        self.log.info("Loading cogs")

        ext = ".py"
        for cog_path in search_files(pattern=f"*{ext}",
                                     path_name=COGS_PATH,
                                     ignore_patterns=("__init__.*", "*_base.*", "_*.py")):

            cog_module = cog_path.removesuffix(f"{ext}").replace("/", ".")
            if cog_module in self.extensions:
                self.log.debug(f"[COG] Reloading cog '{cog_module}'")
                await self.reload_extension(cog_module)
            else:
                self.log.debug(f"[COG] Loading cog '{cog_module}'")
                await self.load_extension(cog_module)

        if sync:
            self.log.info("Syncing command tree...")
            await self.tree.sync()


    async def fetch_emojis(self):
        """Fetches and stores all the emojis of the application."""

        self._emojis = {emoji.name: emoji for emoji in await self.fetch_application_emojis()}


    async def shutdown(self):
        """Closes all the bot's resources gracefully and shuts down in an orderly manner."""

        self.log.debug("Closing connection to database...")
        db.close()

        self.log.info(f"Shutting down {self.user}...")
        await self.close()


    @property
    def verbose(self) -> bool:
        """Checks if the bot is in verbose mode."""

        return self._verbose


    @property
    def uptime(self) -> "timedelta":
        """Calculates the uptime of the bot."""

        return utcnow() - self.booted_at


    @property
    def emojis(self) -> list["Emoji"]:
        """Retrieves all the emojis of the bot."""

        return self._emojis


    async def fetch_avatar(self, candidate: Union[int, User], img_fmt: str=IMG_FORMAT) -> BytesIO:
        """Returns an in-memory file that is the avatar image of a user.
        
        If the avatar URL is needed, use `User.avatar.url` instead.

        Args:
            candidate: The Discord user to retrieve the image from.
                       It can be either a `User` object or its ID.
            img_fmt: The image format that the image will have.
        """

        user = (candidate if isinstance(candidate, User) else await self.fetch_user(candidate))
        img = BytesIO()
        await user.display_avatar.save(img, seek_begin=True)

        return img
