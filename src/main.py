from QEMInterface import *
from OSInterface import *
from concurrent.futures import ThreadPoolExecutor
import yaml


# Logging Config
logger = logging.getLogger(__name__)
time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(filename='QDIRepositoryBck.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='a', level=logging.INFO, datefmt=time_format)

###################################################

###################################################
# Retrieving Config
config_path = os.path.join('..', 'config', 'config.yml')
with open(config_path, 'r') as f:
    config_cfg = yaml.safe_load(f)

###################################################

if __name__ == '__main__':
    qeminterface = QEMInterface()
    osinterface = OSInterface()
    root_bck_dir = osinterface.gen_root_bck_dir()
    session_id = qeminterface.get_session_id()
    rep_servers = qeminterface.get_replicate_servers(session_id)
    for rep_server in rep_servers:
        (server_bck_dir, server_bck_ALL_dir) = osinterface.gen_server_bck_dir(root_bck_dir, rep_server)
        export_all_tasks = qeminterface.backup_alltasks(session_id, rep_server)
        export_all_json_path = os.path.join(server_bck_ALL_dir, 'export_all_tasks.json')
        with open(export_all_json_path, 'w') as f:
            json.dump(export_all_tasks, f)
        tasks = qeminterface.get_task_list(session_id, rep_server)
        for task in tasks:
            export_task = qeminterface.backup_task(session_id, rep_server, task)
            export_task_path = os.path.join(server_bck_dir, f"export_task_{task}.json")
            with open(export_task_path, 'w') as f:
                json.dump(export_task, f)
