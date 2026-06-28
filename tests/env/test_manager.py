from os import environ
from unittest import TestCase
from unittest.mock import mock_open, patch

from gamemaster.env import BOT_MODE_ENV, COMMENT_CHAR, EnvManager


class TestEnvManager(TestCase):
    def setUp(self):
        self.env_manager = EnvManager()


    def test_defines_the_env_path_correctly(self):
        env_path = None
        path_name = "example"

        with patch.dict(environ, {BOT_MODE_ENV: path_name}):
            env_path = self.env_manager.env_path()

        self.assertIsNotNone(env_path)
        self.assertEqual(env_path, f"./{path_name}.env")


    def test_can_add_env_vars(self):
        self.assertEqual(len(self.env_manager), 0)

        self.env_manager.add_env("example", "this")

        self.assertEqual(len(self.env_manager), 1)


    def test_can_overwrite_env_with_same_key(self):
        env_key = "example"
        env_val = "other"
        self.env_manager.add_env(env_key, "this")
        self.env_manager.add_env(env_key, env_val, overwrite=True)

        self.assertEqual(len(self.env_manager), 1)
        self.assertIn(env_key, self.env_manager)
        self.assertEqual(self.env_manager[env_key], env_val)


    def test_can_choose_not_to_override_with_same_key(self):
        env_key = "a_key"
        env_val = "one"
        self.env_manager.add_env(env_key, env_val)
        self.env_manager.add_env(env_key, "two", overwrite=False)

        self.assertEqual(len(self.env_manager), 1)
        self.assertIn(env_key, self.env_manager)
        self.assertEqual(self.env_manager[env_key], env_val)


    def test_can_load_env_vars(self):
        env_key = "my"
        env_val = "precious"

        self.env_manager.add_env(env_key, env_val)

        with patch.dict(environ):
            env_length = len(environ)

            self.env_manager.and_load()
            self.assertEqual(len(environ), env_length + 1)
            self.assertIn(env_key, environ)
            self.assertEqual(environ[env_key], env_val)


    def test_load_envs_with_overwrite(self):
        env_key = "foo"
        env_val = "bar"

        self.env_manager.add_env(env_key, env_val)

        with patch.dict(environ, {env_key: "foos"}):
            self.assertNotEqual(environ[env_key], env_val)
            self.env_manager.and_load(overwrite=True)
            self.assertEqual(environ[env_key], env_val)


    def test_load_envs_without_overriding(self):
        env_key = "foo"
        env_val = "bar"

        self.env_manager.add_env(env_key, "kiki")

        with patch.dict(environ, {env_key: env_val}):
            self.env_manager.and_load(overwrite=False)
            self.assertEqual(environ[env_key], env_val)


    def test_reads_data_from_file(self):
        data = {
            "PROPERTY1": "abc",
            "DATE": "today",
            "# ignore_this_line": "hehe",
            "FAV_NUMBER": "6174"
        }
        file_data = "\n".join(f"{key}={val}" for key, val in data.items())
        env_manager = None
        with patch('builtins.open', new_callable=mock_open, read_data=file_data):
            env_manager = EnvManager.read_from_file("any/path/works/really.lol")

        self.assertIsNotNone(env_manager)

        with patch.dict(environ):
            env_manager.and_load()
            for key, value in data.items():
                with self.subTest():
                    if key.startswith(COMMENT_CHAR):
                        self.assertNotIn(key, environ)
                        continue
                    self.assertIn(key, environ)
                    self.assertEqual(environ[key], value)
