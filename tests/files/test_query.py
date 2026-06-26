from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from gamemaster.files import tail


class TestFilesQuery(TestCase):
    def setUp(self):
        self.simple_lines = ("Line 1\n"
                             "Line 2\n"
                             "Line three\n"
                             "Lain four\n"
                             "Line FIVE")
        self.simple_file = StringIO(self.simple_lines)


    def test_tail_of_simple_file(self):
        tail_lines = 3
        expected = self.simple_lines.splitlines(keepends=True)

        with patch('builtins.open', return_value=self.simple_file):
            result = tail("some/path.txt", tail_lines)

        self.assertEqual(result, expected[-tail_lines:])
