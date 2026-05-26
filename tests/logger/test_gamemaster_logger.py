from unittest import TestCase

from gamemaster.logger.loggers import get_gamemaster_logger


class TestGameMasterLogger(TestCase):
    def test_returns_the_same_logger(self):
        logger_1 = get_gamemaster_logger()
        logger_2 = get_gamemaster_logger()

        self.assertIs(logger_1, logger_2)