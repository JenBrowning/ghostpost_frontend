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

# import os
# import argparse
# import time
# import datetime
# import logging
# import signal



# """Boiler plate for logger on global/module level """
# logger = logging.getLogger(__name__)

# """Exit flag part of sys.signal """
# exit_flag = False
# files_logged = []
# found_text = {}

# # def scan_file(file_name, starting_line, magic_text):
#     '''open file to read
#     enumerate through the lines in a file using a for loop
#     When line number reaches starting line that is when you start searching for the magic_text
#     Every time it finds the magic text in lines and subsequent lines it will log that it found the text.
#     Return last line that was ended on.
#     '''


# def find_files(directory, extension, magictext):
#     """Find all files in given directory, if dir exists"""
#     global files_logged
#     global found_text
#     dir_path = os.path.abspath(directory)
#     dir_files = os.listdir(dir_path)
#     for file in dir_files:
#         if file.endswith(extension) and file not in files_logged:
#             logger.info('New file found: {}'.format(file))
#             files_logged.append(file)
#         if file.endswith(extension):
#             file_path = os.path.join(dir_path, file)
#             if find_string_in_files(file_path, magictext):
#                 break
#     for file in files_logged:
#         if file not in dir_files:
#             logger.info('File deleted: {}'.format(file))
#             files_logged.remove(file)
#             found_text[file] = 0


# def find_string_in_files(file, magictext):
#     """Given single file, looks for text, stores in global dict for record"""
#     global found_text
#     file_base = os.path.basename(file)
#     with open(file) as f:
#         all_lines = f.readlines()
#         for line_number, line in enumerate(all_lines):
#             if magictext in line:
#                 if file_base not in found_text.keys():
#                     found_text[file_base] = line_number
#                 if (line_number >= found_text[file_base]
#                         and file_base in found_text.keys()):
#                     logger.info('Text="{0}" file="{1}" '
#                                 'line: {2}'.format(magictext,
#                                                    file_base,
#                                                    line_number + 1))
#                     found_text[file_base] += 1
#                     return True


# def logger_initiate():
#     """Adjusts how info is displayed in log and sets default log"""
#     logger.setLevel(logging.DEBUG)
#     return logging.basicConfig(
#         format=(
#             '%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s'),
#         datefmt='%Y-%m-%d %H:%M:%S')


# def logger_banner(startorend, time, start=True):
#     """Log banner start/end"""
#     time_message = 'Time Started'
#     if not start:
#         time_message = 'Up time'
#     return logger.info(
#         '\n\n' +
#         '-*'*30 +
#         '-\n\n'
#         ' {2} running file name: {0}\n'
#         ' {3}: {1}\n\n'.format(__file__,
#                                time, startorend, time_message)
#         + '-*'*30 + '-\n'
#     )


# def signal_handler(sig_num, frame):
#     """Smooth exit from system"""
#     global exit_flag
#     logger.warn('Signal Recieved: {}'.format(str(sig_num)))
#     if sig_num:
#         exit_flag = True


# def create_parser():
#     """Create Parser that accepts {optional extension} {optional polling interval} {directory to search} {magic text}"""
#     parser = argparse.ArgumentParser(description='Watching for files containing magictext')
#     parser.add_argument('--ext', help='File extensions to filter on, default=.txt', default='.txt')
#     parser.add_argument('--poll', help="Polling interval in seconds, default=1.0", type=float, default=1.0)
#     parser.add_argument('directory', help='Directory to watch.')
#     parser.add_argument('magictext', help='Text to search for within matching files.')
#     return parser


# def main():
#     """Currently only prints the files in a directory with extention"""
#     parser = create_parser()
#     input_args = parser.parse_args()
#     if not input_args:
#         parser.print_usage()
#         sys.exit(1)
#     logger_initiate()
#     start_time = datetime.datetime.now()
#     logger_banner('Started', start_time)

#     signal.signal(signal.SIGINT, signal_handler)
#     signal.signal(signal.SIGTERM, signal_handler)
#     logger.info('Searching directory="{0}" ext="{1}" interval="{2}" text="{3}" '.format(input_args.directory, input_args.ext, input_args.poll, input_args.magictext))
#     while not exit_flag:
#         try:
#             find_files(input_args.directory,
#                        input_args.ext, input_args.magictext)
#         except OSError as e:
#             logger.error('Directory does not exist: {}'.format(e))
#         except Exception as e:
#             logger.error('Unknown/unhandled error: {}'.format(e))
#         time.sleep(input_args.poll)

#     total_time = datetime.datetime.now() - start_time
#     logger_banner('Ended', total_time, start=False)


# if __name__ == "__main__":
#     """Accepts parser, initiates logger, runs banners"""
#     main()
