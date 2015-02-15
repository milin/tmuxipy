from fabric.api import local
import kaptan


class Window(object):

    LAYOUTS = {
        'main-horizontal': [
            'split-window -v',
            'split-window -h -t {}'
        ]
    }

    def __init__(self, name, tmux, config, win_num):
        self.name = name
        self.tmux = tmux
        self.config = config
        self.panes_objs = {}
        self.win_num = win_num
        self.layout = self.config.get('windows.{}.layout'.format(win_num))
        self.panes = self.config.get('windows.{}.panes'.format(self.win_num))

    def create(self):
        _execute("{} {} {}".format(self.tmux, 'new-session -d -s', self.name))
        self.create_panes()
        _execute("{} {} {}".format(self.tmux, '-2 attach-session -t', self.name), capture=True)

    def create_panes(self):
        for pane_num, pane_data in enumerate(self.panes):
            if pane_num < len(self.panes) - 1:
                tpane = Pane(
                    pane_num,
                    self.tmux,
                    self.win_num,
                    self.config,
                    self.LAYOUTS[self.layout.get('name')][pane_num].format(pane_num)
                )
                tpane.create()
                tpane.send_keys(pane_data)
                self.panes_objs[pane_num] = tpane

        if self.layout.get('name') == 'main-horizontal':
            self.panes_objs[0].resize(self.layout.get('main-pane-height'))


class Pane(object):

    def __init__(self, pane_number, tmux, win_number, config, cmds):
        self.pane_number = pane_number
        self.tmux = tmux
        self.win_number = win_number
        self.cmds = cmds

    def resize(self, size):
        cmd = "{} resize-pane -y {} -t {} ".format(self.tmux, size, self.pane_number)
        _execute(cmd)

    def create(self):
        cmd = "{} {}".format(self.tmux, self.cmds)
        _execute(cmd)

    def send_keys(self, pane_cmd):
        cmd = '{} send-keys -t {} "{}" "C-m"'.format(
            self.tmux,
            self.pane_number,
            pane_cmd
        )
        _execute(cmd)


class TmuxSessionBuilder(object):
    """
    """

    def __init__(self, config=None, server=None):
        """
        If conf is None, it builds the default conf
        """
        self.tmux = _execute('which tmux', capture=True)
        self.config = config
        self.windows = {}

    def build(self):
        if not self.config:
            # Default Configuration
            _execute("{} {}".format(self.tmux, 'new-session -d -s test'))
            _execute("{} {}".format(self.tmux, 'select-window -t test:0'))
            _execute("{} {}".format(self.tmux, 'split-window -v'))
            _execute("{} {}".format(self.tmux, 'split-window -h -t 1'))
            _execute("{} {}".format(self.tmux, 'resize-pane -y 55 -t 0'))
            _execute("{} {}".format(self.tmux, 'send-keys -t 0 "ls -ltr" "C-m"'))
            _execute("{} {}".format(self.tmux, 'send-keys -t 1 "pwd" "C-m"'))
            _execute("{} {}".format(self.tmux, 'send-keys -t 2 "htop" "C-m"'))
            _execute("{} {}".format(self.tmux, '-2 attach-session -t test'), capture=True)
        else:
            config = kaptan.Kaptan()
            config.import_config(self.config)

            for win_num, window in enumerate(config.get('windows')):
                win = Window(
                    window.get('session_name'),
                    self.tmux,
                    config,
                    win_num
                )
                self.windows[win_num] = win
                win.create()

def _execute(cmd, capture=False):
    ret = local(cmd, capture=capture)
    return ret

