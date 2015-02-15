# -*- coding: utf-8 -*
import argparse

import simplejson as json

from tmux_session_builder import TmuxSessionBuilder

parser = argparse.ArgumentParser(description=(
    'Utility to create tmux sessions, windows and panes from preconfigured json '
    'files '
))

parser.add_argument(
    '-c', '--config',
    dest='config',
    default=None,
    required=False,
    help='Path to the configuration file'
)


def main():
    """Main Application"""
    args = parser.parse_args()
    config=None
    if args.config:
        with open(args.config) as myfile:
            config = json.loads(''.join(myfile))

    tmux_builder = TmuxSessionBuilder(config=config)
    tmux_builder.build()

if __name__ == '__main__':
    main()
