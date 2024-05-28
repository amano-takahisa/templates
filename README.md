# Templates

To quick start projects.

The following tools are assumed to be installed and configured:

- [Git](https://git-scm.com/)
- [GitHub-cli](https://cli.github.com/)
- [Rye](https://rye.astral.sh/)

Replace `my_project` with the name of the project, `amano-takahisa` with your GitHub username.

## Jupyter Notebook Based Project

Building an environment to manage jupyter notebooks with Git.

Additional Requirements:

- [jq](https://jqlang.github.io/jq/)


### Setup Project Environment

Create a directory for the project and initialize a git repository.

```bash
mkdir my_project && cd $_ && gh repo create --private $_

# initialize a git repository
rye init --virtual
rye sync
source .venv/bin/activate

# install jupyter notebook in the virtual environment
rye add \
    jupyterlab \
    matplotlib \
    numpy
rye add --optional dev \
    autodoc-pydantic \
    click \
    isort \
    jupyterlab-code-formatter \
    jupyterlab-vim \
    nbconvert \
    nbformat \
    nbsphinx \
    pre-commit \
    pytest \
    pytest-cov \
    sphinx \
    sphinx-rtd-theme
```

### Configuration for documentation

Run the following command to create a `docs` directory and a `docs/source` directory.

```bash
sphinx-quickstart \
    --sep \
    --project=my_project \
    --author=Taka \
    -v=0.1.0 \
    --release=0.1.0 \
    --language=en \
    --ext-githubpages \
    --extensions=nbsphinx,sphinx_rtd_theme \
    docs
```

Update `docs/source/conf.py` as follows:

```python
# files start from `_` are excluded from the documentation
exclude_patterns = ['**/_*']

html_theme = 'sphinx_rtd_theme'
```

Add `snapshot_nb.py` to the `scripts` directory.


### Configuration for Jupyter Notebook

Copy [`.jupyter`](https://github.com/amano-takahisa/dotfiles/tree/master/.jupyter)
directory to `$HOME/.jupyter` directory if you want to use the same settings on jupyter notebook.


### Configuration for Python

Add following sections to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79

[tool.ruff.format]
quote-style = "single"
```

### Configuration for Git

Add followings to `.gitignore`:

```gitignore
# rye
.python-version
requirements.lock
requirements-dev.lock

# Jupyter notebook
.ipynb_checkpoints
```

Add a filter not to commit execution results of jupyter notebook.

ref: [Jupyter Notebook(ipynb)の実質コードのみをgitリポジトリ管理するには ](https://ni66ling.hatenadiary.jp/entry/2018/01/02/022905)

Run:
```bash
git config --local filter.clean_ipynb.clean 'jupyter nbconvert --stdin --stdout --clear-output'
git config --local filter.clean_ipynb.smudge cat

echo '*.ipynb  filter=clean_ipynb' >> .git/info/attributes
# or
# echo '*.ipynb  filter=clean_ipynb' >> .gitattributes
```

### Configuration for GitHub Actions

The repository is need to be public to use GitHub Pages.

On GitHub repository page, go to `Settings` -> `Pages` and set Build and deployment source
to `GitHub Actions`.

Add `.github/workflows/gh-pages.yml` to the project.

### Commit and push the above changes

```bash
git remote add origin git@github.com:amano-takahisa/my_project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Usage

1. Add or update jupyter notebooks, reStructuredText files in the `docs/source` directory.
2. Add file names to `docs/source/index.rst` if necessary.
3. Run `make html` in the `docs` directory to build the documentation.

When `make html` is executed, html files are created by nbsphinx after notebooks
have been executed, if all cell execution results are cleared before hand.
If you know that the running notebook will take a long time, add a prefix `_`
to the filename of the notebook and run the script `snapshot_nb.py` before
running `make html`.
Notebooks start with `_` will be converted as reStructuredText files and
they will not be executed by `make html` as Sphinx ignores them.

GitHub Pages will be updated automatically when the `main` branch is updated on
(https://amano-takahisa.github.io/my_project).

## Python Package Development

```bash
# Create a directory for the project
mkdir my_project && cd $_ && gh repo create --private $_

# initialize a git repository
rye init
rye sync
source .venv/bin/activate

# install development tools
rye add \
    jupyterlab \
    matplotlib \
    numpy
rye add --optional dev \
    autodoc-pydantic \
    click \
    isort \
    jupyterlab-code-formatter \
    jupyterlab-vim \
    nbconvert \
    nbformat \
    nbsphinx \
    pre-commit \
    pytest \
    pytest-cov \
    sphinx \
    sphinx-rtd-theme
```
### Configuration for documentation

Run the following command to create a `docs` directory and a `docs/source` directory.

```bash
sphinx-quickstart \
    --sep \
    --project=my_project \
    --author=Taka \
    -v=0.1.0 \
    --release=0.1.0 \
    --language=en \
    --ext-githubpages \
    --extensions=nbsphinx,sphinx_rtd_theme \
    docs
```

Update `docs/source/conf.py` as follows:

```python
# files start from `_` are excluded from the documentation
exclude_patterns = ['**/_*']

html_theme = 'sphinx_rtd_theme'
```

Add `snapshot_nb.py` to the `scripts` directory.


### Configuration for Jupyter Notebook

Copy [`.jupyter`](https://github.com/amano-takahisa/dotfiles/tree/master/.jupyter)
directory to `$HOME/.jupyter` directory if you want to use the same settings on jupyter notebook.

### Configuration for Python

Add following sections to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79

[tool.ruff.lint]
select = [
  "ALL",
  ]

ignore = [
  "Q000",  # Single quotes found but double quotes preferred
  "ANN003",  # Missing type annotation for **{name}
  "ANN101",  # Missing type annotation for self in method
  "D105",  # Missing docstring in magic method
  "ISC001",  # Implicitly concatenated string literals on one line
  "COM812",  # Trailing comma missing. Compatibility issues https://github.com/astral-sh/ruff/issues/9216
]


[tool.ruff.format]
docstring-code-format = true
quote-style = "single"

[tool.ruff.lint.flake8-quotes]
inline-quotes = "single"

[tool.ruff.lint.per-file-ignores]
"__init__.py" = [
  "D104",  # Missing docstring in public package
  ]
"**/{tests,docs}/*" = [
  "INP001",  # File {filename} is part of an implicit namespace package. Add an __init__.py.
  "D100",  # Missing docstring in public module
  "D101",  # Missing docstring in public class
  "D102",  # Missing docstring in public method
  "D103",  # Missing docstring in public function
  "ANN201", # Missing return type annotation for public function
  "S101",  # Use of assert detected
  "PLR0913",  # Too many arguments in function definition ( > 5 )
  ]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.pyright]
include = ["src"]
venvPath = "."
venv = ".venv"

[tool.pytest.ini_options]
addopts = "--cov --cov-report=term --cov-report=html --cov-branch"
```

### Configuration for Git

Add followings to `.gitignore`:

```gitignore
# rye
.python-version
requirements.lock
requirements-dev.lock

# Jupyter notebook
.ipynb_checkpoints

# pytest
.coverage
coverage.xml
htmlcov
```

Add a filter not to commit execution results of jupyter notebook.

ref: [Jupyter Notebook(ipynb)の実質コードのみをgitリポジトリ管理するには ](https://ni66ling.hatenadiary.jp/entry/2018/01/02/022905)

Run:
```bash
git config --local filter.clean_ipynb.clean 'jupyter nbconvert --stdin --stdout --clear-output'
git config --local filter.clean_ipynb.smudge cat

echo '*.ipynb  filter=clean_ipynb' >> .git/info/attributes
# or
# echo '*.ipynb  filter=clean_ipynb' >> .gitattributes
```

### Configuration for GitHub Actions

The repository is need to be public to use GitHub Pages.

On GitHub repository page, go to `Settings` -> `Pages` and set Build and deployment source
to `GitHub Actions`.

Add `.github/workflows/gh-pages.yml` to the project.

### Commit and push the above changes

```bash
git remote add origin git@github.com:amano-takahisa/my_project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Usage
