from datetime import datetime
import os
import yaml
import logging

# Logging Config
logger = logging.getLogger(__name__)
time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(filename='QDIRepositoryBck.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='a', level=logging.INFO, datefmt=time_format)

class OSInterface:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, '..', 'config', 'config.yml')
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.backup_base_path = f"{self.config['BCK']['path']}QDIRepositoryBackup{self.get_current_date_string()}"

    def get_current_date_string(self):
        return datetime.now().strftime("%Y%m%d%H%M")

    def gen_root_bck_dir(self):
        l_backup_base_path = self.backup_base_path
        try:
            os.mkdir(l_backup_base_path)
        except FileExistsError:
            logger.info('Base Backup Directory already exists')
        return l_backup_base_path
    def gen_server_bck_dir(self, l_backup_base_path, v_server):
        server_bck_dir = os.path.join(l_backup_base_path, v_server)
        server_bck_ALL_dir = os.path.join(server_bck_dir, 'ALL')
        try:
            os.mkdir(server_bck_dir)
            os.mkdir(server_bck_ALL_dir)
        except FileExistsError:
            logger.info(f"Backup Directory for server {v_server} already exists")
        return server_bck_dir, server_bck_ALL_dir

    def gen_task_bck_dir(self, v_server, v_task):
        pass