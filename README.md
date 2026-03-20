# viewserver-python-example

Example project demonstrating how to use `viewserver-python` to build
Python-driven ViewServer operators.

## Setup

### Option A: Install from GitHub Packages (CI/production)

```bash
# Configure Poetry to use the GitHub Packages registry
poetry config http-basic.github __token__ ghp_YOUR_GITHUB_TOKEN

# Install dependencies
poetry install
```

### Option B: Install from local wheel (development)

```bash
# Build viewserver-python from source
cd ../viewserver-core3/viewserver-python
maturin build --release

# Create venv and install
cd ../viewserver-python-example
poetry install --no-root
poetry run pip install ../viewserver-core3/target/wheels/viewserver_python-*.whl
```

## Usage

### Run the example node

```bash
poetry run python -m viewserver_example.node --config config.json
```

### Run the standalone transform example

```bash
poetry run python -m viewserver_example.standalone
```

### Run tests

```bash
poetry run pytest
```

## Project structure

```
viewserver-python-example/
├── pyproject.toml              # Poetry project with viewserver-python dependency
├── config.json                 # ViewServer node config (edit for your environment)
├── src/
│   └── viewserver_example/
│       ├── __init__.py
│       ├── node.py             # Full ViewServer node with Python operators
│       ├── standalone.py       # Standalone pandas transform demo (no engine)
│       └── transforms.py       # Reusable transform functions
└── tests/
    ├── __init__.py
    └── test_transforms.py      # Unit tests for transforms (no engine needed)
```
