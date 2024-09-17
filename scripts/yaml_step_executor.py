import importlib
import sys
from pathlib import Path
from src.utils.logger import get_logger

log = get_logger()

class YamlStepExecutor:
    def __init__(self, config):
        self.config = config
        self.steps = []

    def load_steps(self):
        # Add the project root to the Python path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        log.debug(f"Python path: {sys.path}")

        for step_config in self.config['steps']:
            log.debug(f"Attempting to import module: {step_config['module']}")
            try:
                module = importlib.import_module(step_config['module'])
                class_name = step_config['class']
                step_class = getattr(module, class_name)
                step_instance = step_class(**step_config.get('params', {}))
                self.steps.append((
                    step_instance,
                    step_config.get('execute', True),
                    step_config.get('stop', False)
                ))
                log.debug(f"Successfully loaded step: {class_name} from {step_config['module']}")
            except Exception as e:
                log.error(f"Failed to load step: {step_config['module']}.{step_config['class']}")
                log.error(f"Error: {str(e)}")
                raise
        
        log.info(f"Loaded {len(self.steps)} steps successfully.")

    def execute(self):
        for i, (step, execute, stop) in enumerate(self.steps, 1):
            log.info(f"Step {i}: {step.__class__.__name__} (execute={execute})")
            if execute:
                step.process()
                log.info(f"Step {step.__class__.__name__} completed successfully.")
            else:
                log.info(f"Skipping step: {step.__class__.__name__}")
            
            if stop:
                log.info(f"Stopping after step: {step.__class__.__name__} (YAML-stop={stop})")
                break
        else:
            log.info("All steps completed without interruption.")