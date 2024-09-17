<project_description>
<project_prompt>
<overview>
Train or fine-tune a Stable Diffusion model to generate novel kanji images from English definitions.
</overview>

<current_structure>
stable-diffusion-kanji-generator/
├── data/
│   ├── dataset/
│   │   └── dataset.json
│   ├── processed/
│   │   ├── definitions/
│   │   │   ├── kanjidic_processed.json
│   │   │   └── kanjivg_processed.json
│   │   ├── images128/
│   │   └── svg128/
│   └── raw/
│       ├── kanjidic2/
│       │   ├── kanjidic2.xml
│       │   └── kanjidic2.xml.gz
│       └── kanjivg/
│           ├── kanjivg.xml
│           └── kanjivg-20220427.xml.gz
├── scripts/
│   ├── preprocess_config.yaml
│   ├── preprocess_data.py
│   └── yaml_step_executor.py
├── src/
│   ├── data_preprocessing/
│   │   ├── __init__.py
│   │   ├── dataset_builder.py
│   │   ├── decompress_data.py
│   │   ├── kanjidic_parser.py
│   │   └── svg_to_pixel.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── logger_config.yaml
│   └── __init__.py
├── .gitignore
├── README.md
└── pyproject.toml
</current_structure>

<data_sources>
- data/dataset/dataset.json
</data_sources>

<output>
- Trained Stable Diffusion model
- Documentation of process and results
- Examples of generated kanji (successes, failures, novel/interesting cases)
</output>

<additional_notes>
- Flexibility in choice of deep learning framework
- Option to train from scratch or fine-tune existing model
- Focus on demonstrating concept rather than high-resolution results
- Project is already set up with Poetry for dependency management
</additional_notes>

<preprocessing_strategy>
<yaml_configuration>
The preprocessing steps are managed through scripts/preprocess_config.yaml. This YAML file defines each preprocessing step, including the class to use and its arguments.
</yaml_configuration>

<class_structure>
Each preprocessing step corresponds to a class located in src/data_processing. These classes handle specific tasks and require arguments specified in the YAML under the "process" method.
</class_structure>

<execution_control>
Each step in the YAML can include execute or stop booleans to control whether it runs, allowing selective execution of preprocessing steps.
</execution_control>

<orchestration>
The YamlStepExecutor class (located in scripts/yaml_step_executor.py) orchestrates this flow, dynamically loading and executing the classes based on the YAML configuration.
</orchestration>

<parallel_processing>
This system efficiently processes multiple tasks in parallel by managing the execution of various classes defined in src/<RELEVANT_TASK_NAME_FOLDER>.
</parallel_processing>

<script_execution>
The actual execution happens in /scripts via Python scripts (e.g., preprocess_data.py) that import the YAML configuration and pass the arguments to the classes, ensuring the entire pipeline runs according to the settings in the YAML file.
</script_execution>
</preprocessing_strategy>
</project_prompt>

<task_at_hand>
<requirements>
- Modularize and organize code into a well-defined structure
- Make code easy to understand, effective, and secure
- Use Rich library for terminal output
- Include instructions for LLM to output project folder structure
- Train/fine-tune model on dataset of English definitions and kanji images
- Document procedure, assumptions, and engineering choices
- Save checkpoint, training curves, experimental setup, and produced dataset
- Use Poetry for managing project dependencies and virtual environment
- Create Markdown files to document or communicate anything relevant
- Provide comprehensive documentation and explanation for every decision, code block, and integration with the existing codebase
</requirements>
<action_prompt>
Please implement the project described above, following the requirements and guidelines provided.
Generate the required folders and files, ensuring compatibility with the existing Poetry setup.
Ensure compatibility also with the project's already started practices.
You have the liberty to create Markdown files to document or communicate anything you think is relevant. Everything must be super well documented and explained, including every decision, every code block, and how it integrates with the previous codebase. This includes YAML configurations and any other aspects of the project.
Also, in a sparate markdown, feel free to add any advice or recommendation, be it about the current project or anything else that can be improved for being more clean and professional on the project. Document everything.
Do not feel limited by output length, quantity and quality.
The idea is that /scripts folder contains all the logic to run the project, and everything should be as modular as possible inside src folder.
Add tests if needed.
Atomical. Documented. Readable. Clean. Beautiful. Elegant.
Code using beautful and elegnat patterns whenver possible.
</action_prompt>
</task_at_hand>
</project_description>
