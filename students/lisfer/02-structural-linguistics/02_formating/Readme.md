# Format Tiles

## Installation

```bash
virtualenv venv -p python3
source ./venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm   # for tests
python -m spacy download en_core_web_md
```

## Run Tests

```bash
source ./venv/bin/activate
pytest
```

## Run Program

```bash
Usage: main.py [OPTIONS] [SENTENCE]

Options:
  --input TEXT   Name of income file
  --output TEXT  Name of outcome file
  --help         Show this message and exit.

```

## Results on the Examiner Corpus:

It was updated 4361 lines from  5000.
Resutls are in `output.txt` file
