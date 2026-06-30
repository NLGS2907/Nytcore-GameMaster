from discord import RadioGroupOption
from discord.ui import Checkbox, Label, RadioGroup

from ....games import ElementRPSOptions, WinningRoundsSetting
from ..options_modal_base import BaseOptionsModal


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

        radio_group = RadioGroup(
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
            component=radio_group
        )

        self.add_item(win_rounds)
        

    def update_options(self):
        use_hex: Label = self.children[0]
        self.options.use_hex_emojis = use_hex.component.value

        win_rounds: Label = self.children[1]
        self.options.winning_rounds = WinningRoundsSetting(int(win_rounds.component.value))
