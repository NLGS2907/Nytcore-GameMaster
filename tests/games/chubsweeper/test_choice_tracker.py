from unittest import TestCase
from unittest.mock import Mock

from gamemaster.games import ChoiceTracker, ImagePairHolder, ImageType


class TestChoiceTracker(TestCase):
    def setUp(self):
        self.safes_num = 5
        self.mines_num = 2

        self.safes = [self._holder_mock() for _ in range(self.safes_num)]
        self.mines = [self._holder_mock() for _ in range(self.mines_num)]

        self.choice_tracker = ChoiceTracker(safes=self.safes, mines=self.mines)


    def _holder_mock(self):
        return Mock(ImagePairHolder, **{"blurred_copy_with_number.return_value": Mock(ImageType)})


    def test_is_initialized_properly(self):
        self.assertHasAttr(self.choice_tracker, "score")
        self.assertEqual(self.choice_tracker.score, 0)

        self.assertHasAttr(self.choice_tracker, "doomed")
        self.assertFalse(self.choice_tracker.doomed)


    def test_can_measure_length(self):
        self.assertEqual(len(self.choice_tracker), self.safes_num + self.mines_num)


    def test_can_generate_numbered_blurs(self):
        self.assertEqual(len(self.choice_tracker.numbered_blurred()),
                         self.safes_num + self.mines_num)


    def _generate_test_choices(self, is_safe: bool) -> ChoiceTracker:
        return ChoiceTracker(
            safes=([Mock(ImagePairHolder)] if is_safe else []),
            mines=([Mock(ImagePairHolder)] if not is_safe else [])
        )


    def test_can_see_if_it_is_a_safe(self):
        choice_tracker = self._generate_test_choices(is_safe=True)

        self.assertFalse(choice_tracker.is_mine(1))


    def test_can_see_if_it_is_a_mine(self):
        choice_tracker = self._generate_test_choices(is_safe=False)

        self.assertTrue(choice_tracker.is_mine(1))


    def test_can_see_if_uncovered(self):
        choice_tracker = self._generate_test_choices(is_safe=True)

        self.assertFalse(choice_tracker.uncovered(1))


    def test_can_uncover_choice(self):
        choice_tracker = self._generate_test_choices(is_safe=True)

        choice_tracker.uncover(1)

        self.assertTrue(choice_tracker.uncovered(1))


    def test_uncovers_safe(self):
        choice_tracker = self._generate_test_choices(is_safe=True)
        score = choice_tracker.score

        choice_tracker.uncover(1)

        self.assertFalse(choice_tracker.doomed)
        self.assertEqual(choice_tracker.score, score + 1)


    def test_uncovers_mine(self):
        choice_tracker = self._generate_test_choices(is_safe=False)
        score = choice_tracker.score

        choice_tracker.uncover(1)

        self.assertTrue(choice_tracker.doomed)
        self.assertEqual(choice_tracker.score, score)


    def test_can_not_retrieve_when_out_of_range(self):
        with self.assertRaises(IndexError):
            self.choice_tracker.uncover(len(self.choice_tracker) + 1)


    def test_can_show_choices_depending_on_uncover_status(self):
        dummy_num = 67 # any will do
        expected = [
            holder.blurred_copy_with_number(dummy_num) for holder in (self.safes + self.mines)
        ]

        self.assertCountEqual(self.choice_tracker.showable_faces(), expected)


    def test_can_walk_through_choices(self):
        expected_holders = [*self.safes, *self.mines]
        holders = [choice._holder for choice in self.choice_tracker]

        self.assertCountEqual(holders, expected_holders)

