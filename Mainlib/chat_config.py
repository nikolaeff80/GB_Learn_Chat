import getopt
import json
import sys


def get_json_options(file):
    """
    Get chat options from json file
    :param file: File name
    :return: Dict with setup options
    """
    try:
        with open(file, "r") as f:
            config = json.load(f)
    except ValueError as err:
        print("Can`t read config file: {}, with error: {}".format(file, err))
        sys.exit(2)
    return config


def get_cmd_options(args, short_opts):
    """
    Get options for command line args
    :param args:
    :param short_opts:
    :return:
    """
    try:
        opts, _ = getopt.getopt(args[1:], short_opts)
    except getopt.GetoptError as err:
        print("Invalid argument value with error: {}".format(err))
        sys.exit(2)
    return opts
