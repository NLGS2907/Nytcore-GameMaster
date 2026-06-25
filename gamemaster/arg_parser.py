from argparse import ArgumentParser


class BotArgParser(ArgumentParser):
    """Argument parser for executing the bot."""

    def __init__(self):
        super().__init__()

        self.add_argument("-v", "--verbose",
                          action="store_true",
                          dest="verbose",
                          help="Activate debug mode on the loggers.")
        self.add_argument("-b", "--only-bot",
                          action="store_true",
                          dest="only_bot",
                          help="Activate only the bot logger for stream handlers.")
