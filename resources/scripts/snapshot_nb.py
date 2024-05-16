#!/usr/bin/env python
"""
Search for all Jupyter notebooks start with prefix `_` and convert them to markdown files if the notebook is newer than the markdown file.
The markdown file is saved in the same directory as the Jupyter notebook without the prefix `_`.
"""

import subprocess
from pathlib import Path

import click


def find_notebooks(notebook_dir: Path, prefix: str = '_'):
    """Find all Jupyter notebooks start with prefix '_'.

    Args:
        notebook_dir:
            Directory to search for Jupyter notebooks.
        prefix:
            Prefix of Jupyter notebooks to search for.

    Returns:
        List of tuples of Jupyter notebook and name without prefix.

    """
    return [
        (nb, nb.stem.lstrip(prefix))
        for nb in notebook_dir.glob(f'{prefix}*.ipynb')
    ]


def convert_notebook(notebook: Path, dist_name: str, force: bool = False):
    """Convert Jupyter notebook to markdown file.

    The notebook is converted to markdown with markdown name.

    Args:
        notebook:
            Jupyter notebook to convert.
        dist_name:
            Name of the converted file to save.
            The name should be end with extension '.md' or '.rst'.
            The file is saved in the same directory as the notebook.
        force:
            Force to convert the notebook to markdown even if the markdown file is newer than the notebook.
    """
    dist_file = notebook.parent / dist_name
    if (
        not force
        and dist_file.exists()
        and dist_file.stat().st_mtime > notebook.stat().st_mtime
    ):
        return

    if dist_file.suffix == '.md':
        format_to = 'markdown'
    elif dist_file.suffix == '.rst':
        format_to = 'rst'
    else:
        raise ValueError(f'Invalid extension {dist_file.suffix}')

    args = [
        'jupyter',
        'nbconvert',
        '--to',
        format_to,
        '--output',
        dist_name,
        notebook.as_posix(),
    ]
    subprocess.run(args)


@click.command()
@click.option(
    '-d',
    '--notebook-dir',
    help='Directory to search for Jupyter notebooks.',
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, resolve_path=True
    ),
)
@click.option(
    '--prefix',
    default='_',
    show_default=True,
    help='Prefix of Jupyter notebooks to search for.',
    type=str,
)
@click.option(
    '--force',
    is_flag=True,
    help='Force to convert the notebook to markdown even if the markdown file is newer than the notebook.',
)
@click.option(
    '-f',
    '--format',
    'format_to',
    default='markdown',
    show_default=True,
    help='Format to convert the notebook to.',
    type=click.Choice(['markdown', 'rst']),
)
def main(
    notebook_dir: Path,
    prefix: str,
    force: bool = False,
    format_to: str = 'markdown',
):
    notebook_dir = Path(notebook_dir)
    notebooks = find_notebooks(notebook_dir, prefix)
    if not notebooks:
        print(f'No Jupyter notebooks found in {notebook_dir}')
        return
    format_ext = 'md' if format_to == 'markdown' else 'rst'
    for notebook, name in notebooks:
        print(f'Converting {notebook} to {name}.{format_ext}')
        convert_notebook(
            notebook=notebook, dist_name=f'{name}.{format_ext}', force=force
        )


if __name__ == '__main__':
    main()
