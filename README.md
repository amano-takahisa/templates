# Templates

To quick start projects.

The following tools are assumed to be installed and configured:

- [Git](https://git-scm.com/)
- [GitHub-cli](https://cli.github.com/)
- [Rye](https://rye-up.com/)

Replace `my_project` with the name of the project, `amano-takahisa` with your GitHub username.

## Jupyter Notebook Based Project

Building an environment to manage jupyter notebooks with Git.

Additional Requirements:

- [jq](https://jqlang.github.io/jq/)


### Steps

Create a directory for the project and initialize a git repository.

```bash
mkdir my_project && cd $_ && gh repo create --private $_

# initialize a git repository
rye init --virtual
rye sync
source .venv/bin/activate

# install jupyter notebook in the virtual environment
rye add --dev jupyterlab-code-formatter jupyterlab-vim isort jupyterlab
```

Add followings to `.gitignore`:

```gitignore
# rye
.python-version
requirements.lock
requirements-dev.lock

# Jupyter notebook
.ipynb_checkpoints
```

Copy [`.jupyter`](https://github.com/amano-takahisa/dotfiles/tree/master/.jupyter)
directory to `$HOME/.jupyter` directory if you want to use the same settings on jupyter notebook.

Add following sections to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79

[tool.ruff.format]
quote-style = "single"
```

Add a filter not to commit execution results of jupyter notebook.

ref: [Jupyter Notebook(ipynb)の実質コードのみをgitリポジトリ管理するには ](https://ni66ling.hatenadiary.jp/entry/2018/01/02/022905)

Run:
```bash
git config --local filter.clean_ipynb.clean 'jq --indent 1 --monochrome-output ". + if .metadata.git.suppress_outputs | not then { cells: [.cells[] | . + if .cell_type == \"code\" then { outputs: [], execution_count: null } else {} end ] } else {} end"'
git config --local filter.clean_ipynb.smudge cat

echo '*.ipynb  filter=clean_ipynb' >> .git/info/attributes
# or
# echo '*.ipynb  filter=clean_ipynb' >> .gitattributes
```

Commit and push.

```bash
git remote add origin git@github.com:amano-takahisa/my_project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```
