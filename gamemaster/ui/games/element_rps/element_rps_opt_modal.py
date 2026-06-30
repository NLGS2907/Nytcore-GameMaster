from discord import RadioGroupOption, TextStyle
from discord.ui import Checkbox, Label, RadioGroup, TextInput

from ....games import ElementRPSOptions, WinningRoundsSetting
from ..options_modal_base import BaseOptionsModal

ROUND_TIMEOUT_MIN: int = 10
ROUND_TIMEOUT_MAX: int = 99


class ElementRPSOptionsModal(BaseOptionsModal[ElementRPSOptions]):
    """Options modal for a game of Element Rock-Paper-Scissors."""

    def prepare(self):
        use_hex = Label(
            text="Use hexagonal element codes as emojis.",
            component=Checkbox(
                default=(self.options.use_hex_emojis)
            )
        )
        self.add_item(use_hex)

        wind_rounds_settings = RadioGroup(
            required=True,
            options=[
                RadioGroupOption(
                    label=setting.name.replace("_", " ").capitalize(),
                    value=setting.value,
                    default=(setting == self.options.winning_rounds)
                ) for setting in WinningRoundsSetting
            ]
        )
        win_rounds = Label(
            text="How many rounds?",
            description="Number of rounds one of the players must win to claim victory.",
            component=wind_rounds_settings
        )
        self.add_item(win_rounds)

        round_timeout = Label(
            text="Round Timeout",
            description="Seconds until the round finishes on its own.",
            component=TextInput(style=TextStyle.short,
                                required=False,
                                min_length=1,
                                max_length=2,
                                placeholder=str(self.options.round_timeout))
        )
        self.add_item(round_timeout)
        

    def update_options(self):
        use_hex: Checkbox
        win_rounds: RadioGroup
        round_timeout: TextInput
        use_hex, win_rounds, round_timeout = self._unpack_components()

        self.options.use_hex_emojis = use_hex.value
        self.options.winning_rounds = WinningRoundsSetting(int(win_rounds.value))

        # needs to be in a separate line from assigment, since it can raise exceptions
        candidate_timeout = self._validate_round_timeout(round_timeout.value)
        self.options.round_timeout = candidate_timeout


    def _validate_round_timeout(self, timeout: str) -> int:
        """Ensures the round timeout is a valid numeric number.

        Raises:
            TypeError: If the value passed isn't numeric.
            ValueError: If the value isn't between the min and max range allowed.

        Returns:
            The timeout in seconds, ready to be assigned.
        """

        if not timeout:
            return self.options.round_timeout

        if not timeout.isdecimal():
            raise TypeError(f"Round timeout {timeout!r} ought to have a numeric value")

        num_timeout = int(timeout)
        if num_timeout < ROUND_TIMEOUT_MIN or num_timeout > ROUND_TIMEOUT_MAX:
            raise ValueError(f"Round timeout {timeout!r} should be in the range "
                             f"[{ROUND_TIMEOUT_MIN}, {ROUND_TIMEOUT_MAX}]")

        return num_timeout
