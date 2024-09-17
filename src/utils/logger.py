import logging
import logging.config
import yaml
import inspect
import os

def setup_logging(config_path='src/utils/logger_config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config)

def get_logger():
    # Get the name of the file that's calling this function
    caller_frame = inspect.stack()[1]
    caller_filename = os.path.basename(caller_frame.filename)
    logger_name = os.path.splitext(caller_filename)[0]  # Remove file extension

    if config['log_settings']['enable_logs']:
        return logging.getLogger(logger_name)
    else:
        return logging.getLogger('null')

# Load configuration once when the module is imported
with open('src/utils/logger_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Set up logging
setup_logging()