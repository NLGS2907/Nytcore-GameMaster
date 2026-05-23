"""General implementation of groups and cogs, so that they may be inherited from."""

from traceback import format_exc
from typing import TYPE_CHECKING, Any, Optional, TypeAlias, Union

from discord import Interaction
from discord.app_commands import AppCommandError, Group
from discord.ext.commands import Cog
from discord.utils import MISSING

if TYPE_CHECKING:

    from discord import Permissions
    from discord.app_commands import locale_str
    from discord.ext.commands import Context

    from ..gamemaster import GameMaster

GroupsList: TypeAlias = list[type["_BaseGroup"]]


class _BaseGroup(Group):
    """General Base group."""

    def __init__(self,
                 bot: "GameMaster",
                 *,
                 name: Union[str, "locale_str"] = MISSING,
                 description: Union[str, "locale_str"] = MISSING,
                 parent: Optional[Group] = None,
                 guild_ids: Optional[list[int]] = None,
                 guild_only: bool = MISSING,
                 nsfw: bool = MISSING,
                 auto_locale_strings: bool = True,
                 default_permissions: Optional["Permissions"] = MISSING,
                 extras: dict[Any, Any] = MISSING) -> None:
        """Initializes a group.

        The great majority of the args are already documented on the parent class.

        Args:
            bot: The bot instance to link to this group.
        """

        super().__init__(name=name,
                         description=description,
                         parent=parent,
                         guild_ids=guild_ids,
                         guild_only=guild_only,
                         nsfw=nsfw,
                         auto_locale_strings=auto_locale_strings,
                         default_permissions=default_permissions,
                         extras=extras)
        self.bot: "GameMaster" = bot


class _BaseCog(Cog):
    """General base cog."""


    def __init__(self, bot: "GameMaster") -> None:
        """Initializes a cog.

        The great majority of the args are already documented on the parent class.

        Args:
            bot: The bot instance to link to this cog.
        """

        self.bot: "GameMaster" = bot
        self._load_groups()


    def _load_groups(self) -> None:
        """Loads all the groups registered in this cog."""

        for group_cls in self.groups():
            self.bot.tree.add_command(group_cls(self.bot))


    @classmethod
    def groups(cls) -> GroupsList:
        """Returns the groups list associated with this cog."""

        return []


    async def cog_app_command_error(self,
                                    interaction: Interaction,
                                    _error: AppCommandError) -> None:
        """Default error message handler for exceptions.

        Args:
            interaction: The discord interaction from which the error originated.
            error: An instance of the error itself.
        """

        msg_content = "**[ERROR]** Looks like an error has ocurred."
        if interaction.response.is_done():
            await interaction.edit_original_response(content=msg_content)
        else:
            await interaction.response.send_message(msg_content, ephemeral=True)
        graceful_err = "\n\t|\t".join(f"Exception thrown in app_commands:\n{format_exc()}".split("\n"))
        self.bot.log.error(graceful_err)


    async def cog_before_invoke(self, ctx: "Context") -> None:
        """Logs the command right BEFORE being processed.
        
        Args:
            ctx: The discord command current context.
        """

        guild_exists = ("" if ctx.guild is None else f" in {ctx.guild.name!r}")
        msg_exists = ("a message without content" if not ctx.message.content
                      else f"the message {ctx.message.content!r}")
        self.bot.log.debug((f"[CMD] {ctx.author.name!r} is trying to execute command " +
                            f"{ctx.command.name!r}{guild_exists}, with {msg_exists}."))


    async def cog_after_invoke(self, ctx: "Context") -> None:
        """Logs the command right AFTER being processed.
        
        Args:
            ctx: The discord command current context.
        """

        hay_guild = ("" if ctx.guild is None else f" en {ctx.guild.name!r}")
        hay_mensaje = ("a message without content" if not ctx.message.content
                       else f"the message {ctx.message.content!r}")
        self.bot.log.debug((f"[CMD] {ctx.author.name!r} executed the command " +
                            f"{ctx.command.name!r}{hay_guild}, with {hay_mensaje}."))


async def setup(bot: "GameMaster"):
    """This one setup function is here for compatibility, and does nothing."""
    ...
