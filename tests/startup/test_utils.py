import unittest
import tempfile

from src.startup.utils import folder_exists_and_is_writeable


class TestUtils(unittest.TestCase):

    def test_folder_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            success, _ = folder_exists_and_is_writeable(tmp)
            self.assertTrue(success)

    def test_folder_not_exists(self):
        success, _ = folder_exists_and_is_writeable('./_not_existing')
        self.assertFalse(success)
