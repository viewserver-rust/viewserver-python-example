# viewserver-python-example

Example project demonstrating how to use `viewserver-python` to build
Python-driven ViewServer operators.

## Setup

### Option A: Install from GitHub Release (recommended)

```bash
# Install Poetry if you don't have it
pip install poetry

# Install pure-Python deps + pre-built viewserver-python wheel
poetry install --extras viewserver
```

The `viewserver-python` wheel URL is in `pyproject.toml`. Update it when a
new version is released. Find releases at:
https://github.com/viewserver-rust/viewserver-core/releases

### Option B: Install from local wheel (development)

```bash
# Build viewserver-python from source (requires Rust toolchain)
cd ../viewserver-core3/viewserver-python
maturin build --release

# Install pure-Python deps, then the local wheel
cd ../viewserver-python-example
poetry install
poetry run pip install ../viewserver-core3/target/wheels/viewserver_python-*.whl
```

### Option C: Direct pip install (no Poetry)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas pyarrow numpy
pip install https://github.com/viewserver-rust/viewserver-core/releases/download/python-v0.1.0/viewserver_python-0.1.0-cp310-cp310-win_amd64.whl
```

## Usage

### Run the standalone transform demo (no engine needed)

```bash
poetry run python -m viewserver_example.standalone
```

### Run as a ViewServer node

Edit `config.json` to point at your ReportingEngine, then:

```bash
poetry run python -m viewserver_example.node --config config.json
```

### Run tests

```bash
poetry run pytest
```

## Project structure

```
viewserver-python-example/
├── pyproject.toml              # Poetry project with viewserver-python URL dependency
├── config.json                 # ViewServer node config (edit for your environment)
├── src/
│   └── viewserver_example/
│       ├── __init__.py
│       ├── node.py             # Full ViewServer node with Python operators
│       ├── standalone.py       # Standalone pandas transform demo (no engine)
│       └── transforms.py       # Reusable transform functions
└── tests/
    └── test_transforms.py      # Unit tests for transforms (no engine needed)
```

## How it works

The `viewserver-python` package is a native Rust extension (built with PyO3/maturin)
that embeds the ViewServer engine. It's distributed as a pre-built `.whl` file
attached to GitHub Releases — no Rust toolchain needed on the consumer machine.

The GitHub Actions workflow in the main repo builds the wheel, runs tests, and
creates a release with the wheel attached on every merge to `main`.
