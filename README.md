# Snakeglish

Snakeglish reads your python code and speaks back a human readable description.

## Example Test Cases

The `test_cases` directory has all the examples. Each test case has the
directory layout like this:

```
├── test_cases
│   └── <example_name>
│       ├── code.py
│       └── description.txt
```

The `code.py` file is the input code, and the `description.txt` file is the
generated description of that code.

## Local Setup

Install [Poetry](https://python-poetry.org/), then use `poetry install` to
install the dependencies.
