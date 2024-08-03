import unittest
import os
import yaml
from datetime import datetime
from src.OSInterface import *
class TestOSInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.OSInterface = OSInterface()
        super(TestOSInterface, self).__init__(*args, **kwargs)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, '..', 'config', 'config.yml')
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.back_base_path = f"{self.config['BCK']['path']}QDIRepositoryBackup{self.OSInterface.get_current_date_string()}"


    def test_directory_exists(self):
        """
        Test if the specified directory exists.
        """
        try:
            os.rmdir(self.backup_base_path)
        except:
            None
        self.OSInterface.gen_root_bck_dir()
        self.assertTrue(os.path.isdir(self.back_base_path), f"Directory does not exist: {self.back_base_path}")

    def test_old_directory_doesnt_exist(self):
        """
        Test old directory doesn't exist
        """
        self.assertFalse(os.path.isdir(f"{self.config['BCK']['path']}/199001011000"), f"Directory does not exist:{self.config['BCK']['path']} 199001011000")


    def tearDown(self):
        pass
        # This method is called after each test. Clean up any resources if needed.pass

if __name__ == '__main__':
    unittest.main()
