import unittest
from src.QEMInterface import *

class TestQEMInterface(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.QEMInterface = QEMInterface()
        super(TestQEMInterface, self).__init__(*args, **kwargs)

    def test_get_session_id(self):
        session_id = self.QEMInterface.get_session_id()
        self.assertTrue(len(session_id)>0, "Returns a not null session_id token")

    def test_get_replicate_servers(self):
        session_id = self.QEMInterface.get_session_id()
        replicate_servers = self.QEMInterface.get_replicate_servers(session_id)
        self.assertTrue(len(replicate_servers) > 0, "Returns Replicate Servers")

    def test_get_task_list(self):
        pass
        # self.fail()
