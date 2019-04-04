#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a long running program
that searches a directories files for text files
containing an input string,
if found, log the txt file and line found.
Don't repeat old found items
"""

__author__ = "Jen Browning"

import argparse
import time
import datetime
import logging
import signal
import os


logger = logging.getLogger(__file__)
exit_flag = False
files_found = []
magic_word_position = {}


def watch_directory(args):
    """Watches directory and shows when files matching the
    given extension are added or removed. Calls find_magic to search
    files for magic word"""
    global files_found
    global magic_word_position
    logger.info('Watching directory: {}, File Ext: {}, Polling Interval: {}, Magic Text: {}'.format(
                args.path, args.ext, args.interval, args.magic
    ))

    directory = os.path.abspath(args.path)
    files_in_directory = os.listdir(directory)
    for file in files_in_directory:
        if file.endswith(args.ext) and file not in files_found:
            logger.info('New file: {} found in {}'.format(file, args.path))
            files_found.append(file)
            magic_word_position[file] = 0
    for file in files_found:
        if file not in files_in_directory:
            logger.info('File: {} removed from {}'.format(file, args.path))
            files_found.remove(file)
            del magic_word_position[file]
    for file in files_found:
        find_magic(file, args.magic, directory)
    # while True:
    #     try: 
    #         logger.info('Inside Watch Loop')
    #         time.sleep(args.interval)
    #     except KeyboardInterrupt:
    #         break


def signal_handler(sig_num, frame):
    """Looks for signals SIGINT and SIGTERM; toggles the global exit_flag"""
    global exit_flag

    signames = dict((k, v) for v, k in reversed(sorted(
        signal.__dict__.items()))
        if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received signal: ' + signames[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True


def find_magic(filename, magic_word, directory):
    """Search for the magic word in the filename line by line and
    keep track of the last line searched"""

    global magic_word_position
    with open(directory, '/', filename) as f:
        for i, line in enumerate(f.readlines(), 1):
            if magic_word in line and i > magic_word_position[filename]:
                 logger.info('Discovered magic word: {} on line: {}'
                            ' in file: {}'.format(magic_word, i, filename))
            if i > magic_word_position[filename]:
                magic_word_position[filename] += 1


def create_parser():
    """Creates Parser; sets up command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt', 
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float, 
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser

    
def main():
    """
    Start up or shut down banner with a signal module.
    While loop that runs waiting for a SIGINT or SIGTERM to close.
    """  
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Running {0}\n'
        '   Started 0n {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not exit_flag:
        try:
            watch_directory(args)
        except OSError:
            logger.error('{} directory does not exist'.format(args.path))
            time.sleep(args.interval*2)
        except Exception as e:
            logger.error('Unhandled exception: {}'.format(e))
        time.sleep(args.interval)


    watch_directory(args)


    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Stopped {0}\n'
        '   Uptime was  {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )
 




if __name__ == '__main__':
    main()