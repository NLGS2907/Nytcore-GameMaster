from discord.ui import LayoutView, TextDisplay


class ThrowableView(LayoutView):
    """Simple view for when whe need to populate the message with *something*."""

    def __init__(self, content: str):
        """Initializes the throwable view.
        
        Args:
            content: The text to use as content for the view.
        """
        super().__init__()

        self.add_item(TextDisplay(content))
