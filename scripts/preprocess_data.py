import yaml
from pathlib import Path
from configs.yaml_step_executor import YamlStepExecutor
from src.utils.logger import get_logger

log = get_logger()

config_path = 'configs/preprocess_config.yaml'
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

def main():

    executor = YamlStepExecutor(config)
    executor.load_steps()
    try:
        executor.execute()
        log.info("All enabled steps completed successfully.")
    except Exception as e:
        log.error(f"Execution failed: {e}")

if __name__ == "__main__":
    main()