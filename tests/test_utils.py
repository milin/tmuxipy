import mock
import unittest

from tmuxipy.utils import _execute

TESTING_MODULE = 'tmuxipy.utils'


class TestUtils(unittest.TestCase):

    @mock.patch(TESTING_MODULE + '.local')
    def test__execute(self, mock_local):
        _execute('ls -ltr')
        mock_local.assert_called_once_with('ls -ltr', capture=False)
