#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import time
from machinekit import launcher
from machinekit import config

PATH = os.path.dirname(os.path.realpath(__file__))
os.chdir(PATH)
os.environ['PYTHONPATH'] = PATH


def main():
    parser = argparse.ArgumentParser(
        description='This runs the Borunte HAL configuration'
    )
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    parser.add_argument(
        '-s', '--sim', help='enable simulation mode', action='store_true'
    )

    args = parser.parse_args()

    if args.debug:
        launcher.set_debug_level(5)

    if args.sim:
        os.environ['SIM_MODE'] = '1'
    os.environ['MACHINEKIT_INI'] = config.MACHINEKIT_INI

    try:
        launcher.check_installation()
        launcher.cleanup_session()  # kill any running Machinekit instances
        launcher.install_comp('./components/absolute_joint.icomp')
        launcher.start_realtime()  # start Machinekit realtime environment

        launcher.ensure_mklauncher()
        launcher.start_process('configserver -n Borunte-Tester .')

        launcher.load_hal_file('hal_config.py')  # load the main HAL file
        # enable on ctrl-C, needs to executed after HAL files
        launcher.register_exit_handler()

        while True:
            launcher.check_processes()
            time.sleep(1)

    except KeyboardInterrupt:
        # sys.stderr.write(
        #     '\n\n--------- ERROR ---------\n%s\n-------------------------\n\n' % str(e)
        # )
        sys.exit(0)
    finally:
        launcher.end_session()


if __name__ == '__main__':
    main()
