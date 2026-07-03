from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

from discord import Interaction, InteractionResponse

from gamemaster.modals import ProfileEditModal
from gamemaster.models import Player
from gamemaster.repositories import PlayerRepository


class TestProfileEditModal(IsolatedAsyncioTestCase):
    def setUp(self):
        self.player_name = "Kiki"
        player_mock = Mock(Player, **{
            "username": self.player_name
        })
        player_repo_mock = Mock(PlayerRepository)

        self.profiled_edit_modal = ProfileEditModal(player_mock, player_repo_mock)

        self.response_mock = AsyncMock(InteractionResponse)
        self.interaction_mock = Mock(Interaction, **{"response": self.response_mock})


    def test_is_initialized_properly(self):
        self.assertHasAttr(self.profiled_edit_modal, "title")
        self.assertEqual(self.profiled_edit_modal.title,
                         f" Edit {self.player_name} Profile Details")

        self.assertHasAttr(self.profiled_edit_modal, "timeout")
        self.assertIsNone(self.profiled_edit_modal.timeout)


    async def test_can_process_submit_callback_with_no_changes(self):
        await self.profiled_edit_modal.on_submit(self.interaction_mock)

        self.response_mock.send_message.assert_called_once_with("_No changes were made._",
                                                                ephemeral=True)
