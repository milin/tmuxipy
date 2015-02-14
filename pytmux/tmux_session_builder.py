from fabric.api import local

class TmuxSessionBuilder(object):
    """
    """

    def __init__(self, conf=None, server=None):
        """
        If conf is None, it builds the default conf
        """
        self.tmux = self._execute('which tmux', capture=True)
        self.conf = None

    def build(self):
        if not self.conf:
            # Default Configuration
            self._execute("{} {}".format(self.tmux, 'new-session -d -s test'))
            self._execute("{} {}".format(self.tmux, 'select-window -t test:0'))
            self._execute("{} {}".format(self.tmux, 'split-window -v'))
            self._execute("{} {}".format(self.tmux, 'split-window -h -t 1'))
            self._execute("{} {}".format(self.tmux, 'resize-pane -y 55 -t 0'))
            self._execute("{} {}".format(self.tmux, 'send-keys -t 0 "ls -ltr" "C-m"'))
            self._execute("{} {}".format(self.tmux, 'send-keys -t 1 "pwd" "C-m"'))
            self._execute("{} {}".format(self.tmux, 'send-keys -t 2 "htop" "C-m"'))
            self._execute("{} {}".format(self.tmux, '-2 attach-session -t test'), capture=True)


    def _execute(self, cmd, capture=False):
        ret = local(cmd, capture=capture)
        return ret

