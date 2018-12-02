# python imports
import configparser
import os.path

# utils imports
from utils.constants import CFG_FILE, CFG_DEF, CFG_VALS

def load_config_section(config_file=CFG_FILE,config_section=CFG_DEF,required_vals=CFG_VALS):
    """ Loads in the specified configuration section.

    Parameters
    ----------
    config_file : string
        path to the configs.ini file to use
    config_section : string
        which section in the configs.ini file to use
    required_vals : [string]
        list of required values in the config section

    Returns
    -------
    config_section : ConfigParser
        a dict-like structure containing required_vals
    """
    if not os.path.isfile(config_file):
        return None
    config = configparser.ConfigParser()
    config.read(config_file)
    if config_section not in config:
        return None
    for val in required_vals:
        if val not in config[config_section]:
            return None
    return config[config_section]

DEFAULT_CONFIGS = load_config_section(CFG_FILE,CFG_DEF,CFG_VALS)
