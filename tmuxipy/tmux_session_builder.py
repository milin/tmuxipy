import kaptan

from utils import _execute


class Session(object):

    def __init__(self, name, config, tmux):
        self.name = name
        self.config =config
        self.tmux = tmux
        self.windows = {}

    def create(self):
        _execute("{} {} {}".format(self.tmux, 'new-session -d -s', self.name))
        _execute("{} {} '{}'".format(self.tmux, 'rename-window', self.config.get('windows.0.name')))
        for win_num, window in enumerate(self.config.get('windows')):
            win = Window(
                self.config.get('windows.{}.name'.format(win_num)),
                self.tmux,
                self.config,
                win_num,
                self.name
            )
            self.windows[win_num] = win
            win.create()
        self._attach_to_session()

    def _attach_to_session(self):
        _execute("{} {} {}".format(self.tmux, '-2 attach-session -t', self.name), capture=True)


class Window(object):

    LAYOUTS = {
        'main-horizontal': [
            'split-window -v',
            'split-window -h -t {}'
        ]
    }

    def __init__(self, name, tmux, config, win_num, session_name):
        self.name = name
        self.session_name = session_name
        self.tmux = tmux
        self.config = config
        self.panes_objs = {}
        self.win_num = win_num
        self.layout = self.config.get('windows.{}.layout'.format(win_num))
        self.panes = self.config.get('windows.{}.panes'.format(self.win_num))
        self.pre_shell_cmds = self.config.get(
            'windows.{}.pre_shell_commands'.format(self.win_num)
        )

    def create(self):
        if self.win_num > 0:
            _execute("{} {}".format(self.tmux, 'new-window'))
            self._execute_pre_shell_cmds()
            _execute("{} {} '{}'".format(self.tmux, 'rename-window', self.name))
        self.create_panes()

    def create_panes(self):
        for pane_num, pane_data in enumerate(self.panes):
            try:
                layout_cmd =  self.LAYOUTS[self.layout.get('name')][pane_num].format(pane_num)
            except IndexError:
                layout_cmd = None
            tpane = Pane(
                pane_num,
                self.tmux,
                self.win_num,
                self.config,
                layout_cmd
            )
            if pane_num < len(self.panes) - 1:
                tpane.create()
            tpane.send_keys(pane_data)
            self.panes_objs[pane_num] = tpane

        if self.layout.get('name') == 'main-horizontal':
            self.panes_objs[0].resize(self.layout.get('main-pane-height'))

    def _execute_pre_shell_cmds(self):
        for cmd in self.pre_shell_cmds:
            _execute("{} send-keys -t 0 {} 'C-m'".format(self.tmux, cmd))


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
        if isinstance(pane_cmd, list):
            [self._send_keys(cmd) for cmd in pane_cmd]
        else:
            self._send_keys(pane_cmd)

    def _send_keys(self, pane_cmd):
        cmd = '{} send-keys -t {} "{}" "C-m"'.format(
            self.tmux,
            self.pane_number,
            pane_cmd
        )
        _execute(cmd)


class TmuxSessionBuilder(object):

    def __init__(self, config=None, server=None):
        """
        If conf is None, it builds the default conf
        """
        self.tmux = _execute('which tmux', capture=True)
        self.config = config

    def build(self):
        if not self.config:
            #Default Configuration
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
            session_name = config.get('session_name', '')
            session = Session(session_name, config, self.tmux)
            session.create()
