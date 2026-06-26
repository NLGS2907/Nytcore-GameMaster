from unittest import TestCase
from unittest.mock import Mock

from gamemaster.repositories import (
    IPlayerRepository,
    IRPSResultRepository,
    PlayerRepository,
    RepositoryConfiguration,
    RPSResultRepository,
)


class TestRepositoryConfiguration(TestCase):
    def setUp(self):
        player_repo_mock = Mock(PlayerRepository)
        rps_result_repo_mock = Mock(RPSResultRepository)

        self.repo_config = RepositoryConfiguration(player_repository=player_repo_mock,
                                                   rps_result_repository=rps_result_repo_mock)


    def test_is_created_with_all_the_internal_repos(self):
        self.assertIsInstance(self.repo_config.player, IPlayerRepository)
        self.assertIsInstance(self.repo_config.rps_result, IRPSResultRepository)
