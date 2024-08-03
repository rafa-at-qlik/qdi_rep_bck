import requests
import warnings
import json
import logging
import yaml
import os

warnings.filterwarnings("ignore")
# Logging Config
logger = logging.getLogger(__name__)
time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(filename='QDIRepositoryBck.log',format='%(asctime)s - %(levelname)s - %(message)s', filemode='a', level=logging.INFO, datefmt=time_format)

class QEMInterface:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.access_path = os.path.join(self.base_dir, '..', 'config', 'access.yml')
        with open(self.access_path, 'r') as f:
            self.access_cfg = yaml.safe_load(f)
        self.em_host = self.access_cfg['QEM']['host']
        self.em_user = self.access_cfg['QEM']['user']
        self.em_password = self.access_cfg['QEM']['password']
        self.base_api_url = f"https://{self.em_host}/attunityenterprisemanager/api/v1"

    def get_session_id(self):
        logger.info('Getting APISessionID')
        l_api_session_id = None
        try:
            session = requests.Session()
            session.auth = (self.em_user, self.em_password)
            auth = session.post(f"{self.base_api_url}/login", verify=False)
            response = session.get(f"{self.base_api_url}/login", verify=False)
            l_api_session_id = response.headers.get('EnterpriseManager.APISessionID')
            logger.info('Session token APISessionID successfully retrieved')
        except Exception as e:
            logger.error(f"Error while trying to get APISessionID in method get_session_id {logger.exception(e)}" )
        return l_api_session_id

    def get_replicate_servers(self, v_session_id):
        logger.info('Getting the List of Replicate Servers - method get_replicate_servers')
        get_server_list_url = f"https://{self.em_host}/attunityenterprisemanager/api/v1/servers"
        rep_server_list = list()
        try:
            task_response = requests.get(get_server_list_url, headers={'EnterpriseManager.APISessionID': v_session_id, "Content-Length": "0"}, verify=False)
            configjson = json.loads(task_response.text)
            logger.info('Replicate Server List Successfully retrieved')
            servers = configjson['serverList']
            for index in range(0, len(servers)):
                server = servers[index]
                if server['$type'] == 'ReplicateServerInfo':
                    rep_server_list.append(server['name'])
                    logger.info(f"Server {server['name']} is a Replicate Server")
        except Exception as e:
            logger.error(f"Error while trying to get Replicate Server {logger.exception(e)}")
        return rep_server_list

    def get_task_list(self, v_session_id, v_server):
        logger.info(f"Retrieving Tasks for Server {v_server} - method get_task_list")
        get_task_list_url = f"https://{self.em_host}/attunityenterprisemanager/api/v1/servers/{v_server}/tasks"
        rep_server_tasks_lst = list()
        try:
            task_response = requests.get(get_task_list_url, headers={'EnterpriseManager.APISessionID': v_session_id, "Content-Length": "0"}, verify=False)
            configjson = json.loads(task_response.text)
            tasks = configjson['taskList']
            for index in range(0, len(tasks)):
                task = tasks[index]
                rep_server_tasks_lst.append(task['name'])
                logger.info(f"task {task['name']} added to list")
            logger.info(f"Tasks List Successfully retrieved for server {v_server}")
        except Exception as e:
            logger.error(f"Error while trying to retrieve tasks for server {v_server} {logger.exception(e)} - method get_task_list")
        return rep_server_tasks_lst

    def backup_alltasks(self, v_session_id, v_server):
        logger.info(f"Exporting all tasks for server {v_server}")
        export_all_url = f"https://{self.em_host}/attunityenterprisemanager/api/v1/servers/{v_server}?action=export"
        export_all_tasks = None
        try:
            export_all_response = requests.get(export_all_url,
                                         headers={'EnterpriseManager.APISessionID': v_session_id, "Content-Length": "0"},
                                         verify=False)
            export_all_tasks = json.loads(export_all_response.text)
        except Exception as e:
            logger.error(f"Error while trying to backup all tasks from server {v_server} {logger.exception(e)} - method backup_alltasks")
        return export_all_tasks

    def backup_task(self, v_session_id, v_server, v_task):
        logger.info(f"Retrieving Tasks for Server {v_server} - method get_task_list")
        export_task_url = f"https://{self.em_host}/attunityenterprisemanager/api/v1/servers/{v_server}/tasks/{v_task}?action=export&withendpoints=true"
        export_task = None
        try:
            export_task_response = requests.get(export_task_url,
                                         headers={'EnterpriseManager.APISessionID': v_session_id, "Content-Length": "0"},
                                         verify=False)
            export_task = json.loads(export_task_response.text)
        except Exception as e:
            logger.error(f"Error while trying to backup all task {v_task} from server {v_server} {logger.exception(e)} - method backup_task")
        return export_task