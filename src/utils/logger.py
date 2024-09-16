import logging
import logging.config
import os
import yaml

def setup_logging(config_path='src/utils/logger_config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

def get_logger(name=None):
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger

# Set up logging when the module is imported
setup_logging()
log = get_logger('Data preprocessing')