import unittest
import mock
import simplejson as json

from tmuxipy.main import TmuxSessionBuilder


TESTING_MODULE = 'tmuxipy.tmux_session_builder'

class TestTmuxSessionBuilder(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch(TESTING_MODULE + '.Session.create')
    @mock.patch(TESTING_MODULE + '._execute')
    @mock.patch(TESTING_MODULE + '.kaptan.Kaptan.import_config')
    def test_build(self,
                   mock__execute,
                   mock_kaptan_import_config,
                   mock_session_create):
        config = json.dumps({"session_name": "test"})
        tmux_session_builder = TmuxSessionBuilder(config=config)
        mock_kaptan_import_config.return_value = config
        tmux_session_builder.build()
        self.assertTrue(mock_kaptan_import_config.called)
        self.assertTrue(mock_session_create.called)
