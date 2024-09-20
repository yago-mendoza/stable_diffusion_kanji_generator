![@hardmaru](https://github.com/yago-mendoza/stable_diffusion_kanji_generator/blob/main/docs/hardmaru_matrix.PNG)

# Stable Diffusion Kanji Generator

A comprehensive project for generating kanji images using stable diffusion models, with data preparation, model training, and deployment using Hugging Face.

## Table of Contents
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Data Preprocessing](#data-preprocessing)
- [Training the Model](#training-the-model)
- [Generating Images](#generating-images)
- [Model Theory](#model-theory)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Directory Structure

```
project-root/
├── data/
│   ├── dataset/
│   │   └── dataset128.json
│   ├── models/
│   │   └── checkpoints/
│   ├── processed/
│   │   ├── definitions/
│   │   ├── images128/
│   │   └── svg128/
│   └── raw/
│       ├── kanjidic2/
│       └── kanjivg/
├── scripts/
│   ├── generate_image.py
│   ├── preprocess_data.py
│   └── train_model.py
├── src/
│   ├── data_preprocessing/
│   │   ├── __init__.py
│   │   ├── dataset_builder.py
│   │   ├── decompress_data.py
│   │   ├── kanjidic_parser.py
│   │   └── svg_to_pixel.py
│   └── model/
│       ├── cache/
│       │   ├── locks/
│       │   ├── models--CompVis--stable-diffusion-v1-4/
│       │   ├── models--openai--clip-vit-large-patch14/
│       │   ├── models--runwayml--stable-diffusion-v1-5/
│       │   └── models--stabilityai--stable-diffusion-2-1-base/
│       ├── __init__.py
│       └── training.py
├── pyproject.toml
└── README.md
```

## Installation

This project uses Poetry for dependency management.

1. **Clone the repository**
    ```bash
    git clone https://github.com/username/kanji-stable-diffusion.git
    cd kanji-stable-diffusion
    ```

2. **Install Poetry** (if not already installed)
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Install project dependencies**
    ```bash
    poetry install
    ```

## Data Preprocessing

Preprocess the kanji data using the provided script:

```bash
poetry run python scripts/preprocess_data.py
```

This script will handle the parsing of KanjiDic2 data, SVG processing, and dataset building.

## Training the Model

Train the stable diffusion model with the following command:

```bash
poetry run python scripts/train_model.py
```

This will use the preprocessed data and train the model, saving checkpoints in the `data/models/checkpoints/` directory.

## Generating Images

Generate kanji images using the trained model:

```bash
poetry run python scripts/generate_image.py
```

## Model Theory

This project utilizes stable diffusion models to generate high-quality kanji images. Stable diffusion is a deep learning method that generates images by gradually denoising random Gaussian noise, making it particularly effective for generating detailed and coherent images like kanji characters.

## Usage

After training, use the model to generate kanji images:

```python
from src.model.training import generate_image

prompt = "A kanji character for 'mountain' in cursive style"
image = generate_image(prompt)
image.save("kanji_mountain_cursive.png")
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the [MIT License](LICENSE).
