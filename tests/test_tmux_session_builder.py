import unittest
import mock
import simplejson as json

from tmuxipy.tmux_session_builder import (
    TmuxSessionBuilder,
    Session
)


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


class TestSession(unittest.TestCase):

    def setUp(self):
        self.config = {'windows': [{'a': 'b'}, {'c': 'd'}]}
        self.session = Session(
            'Test',
            self.config,
            mock.sentinel.tmux
        )

    def test__init(self):
        test_config = {'a': 'b'}
        session_a = Session(
            'Test',
            test_config,
            mock.sentinel.tmux
        )
        self.assertEqual('Test', session_a.name)
        self.assertEqual(test_config, session_a.config)
        self.assertEqual(mock.sentinel.tmux, session_a.tmux)
        self.assertEqual({}, session_a.windows)

    @mock.patch(TESTING_MODULE + '.Window')
    @mock.patch.object(Session, '_sanity_check')
    @mock.patch.object(Session, '_execute_pre_commands')
    @mock.patch.object(Session, '_attach_to_session')
    def test_create(self,
                    mock__attach_to_session,
                    mock__execute_pre_commands,
                    mock__sanity_check,
                    mock_window):
        self.session.create()
        mock__sanity_check.assert_called_once_with()
        mock__execute_pre_commands.assert_called_once_with()
        mock__attach_to_session.assert_called_once_with()




