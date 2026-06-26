import tempfile
from pathlib import Path
from unittest import TestCase

from gamemaster.files.search import search_files, search_paths


class TestFileSearches(TestCase):
    def setUp(self):
        self.temp_dir_ctx = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir_ctx.name)
        (self.base_path / "config.json").write_text("{}")

        self.src_dir = self.base_path / "src"
        self.src_dir.mkdir()
        (self.src_dir / "main.py").write_text("print('hello')")
        (self.src_dir / "utils.py").write_text("def tool(): pass")

        self.docs_dir = self.base_path / "docs"
        self.docs_dir.mkdir()


    def tearDown(self):
        self.temp_dir_ctx.cleanup()


    def test_search_files_recursive(self):
        result = search_files(pattern="*.py", path_name=str(self.base_path), recursive=True)

        expected = [(self.src_dir / "main.py").as_posix(),
                    (self.src_dir / "utils.py").as_posix(),]

        self.assertEqual(sorted(result), sorted(expected))


    def test_search_paths_excluding_files(self):
        result = search_paths(
            pattern="*",
            path_name=str(self.base_path),
            recursive=False,
            include_files=False,
            include_dirs=True,
        )

        expected = [self.src_dir.as_posix(), self.docs_dir.as_posix()]

        self.assertEqual(sorted(result), sorted(expected))


    def test_search_files_with_ignore_patterns(self):
        result = search_files(
            pattern="*",
            path_name=str(self.base_path),
            recursive=True,
            ignore_patterns=("*.md",),
        )

        readme_path_str = (self.docs_dir / "readme.md").as_posix()
        self.assertNotIn(readme_path_str, result)
