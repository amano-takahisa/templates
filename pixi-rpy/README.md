# Setup Geospatial R and Python Development Environment with Pixi

This guide will help you set up a geospatial development environment with R and Python using the Pixi package manager.

RStudio and Jupyter Labs are setup for R and Python development, respectively.

## Pre-requisites

- Pixi
- Docker
- Git

Install pixi.

```bash
curl -fsSL https://pixi.sh/install.sh | bash
# or use your package manager
```

## Initialize Repository

```bash
gh repo create --private my-project
mkdir my-project
cd my-project
pixi init
git init
echo "# my-project" > README.md
echo "This is a dummy project to demonstrate the setup of a geospatial development environment with R and Python using the Pixi package manager." >> README.md
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:amano-takahisa/my-project.git
git push -u origin main
```

Initialize pixi features.

**Note**: This is a HACK to create environments before adding dependencies.

```bash
echo '\n[feature.dev.dependencies]' >> pixi.toml
echo '\n[feature.test.dependencies]' >> pixi.toml
```

Add pixi environments.

```bash
pixi project environment add \
    dev \
    --feature dev \
    --feature test \
    --solve-group default
```

Add required python packages for products.

```bash
pixi add \
    python \
    geopandas \
    rasterio \
    xarray
# add more packages as needed
```

Add required python packages for development.

```bash
pixi add --feature dev \
    jupyterlab \
    jupyterlab_code_formatter \
    jupyterlab_vim \
    ruff \
    isort
# add more packages as needed
```

Add required pythonn packages for testing.

```bash
pixi add --feature test \
    pytest \
    pytest-cov \
    ruff
# add more packages as needed
```

Add required R packages for products.

```bash
pixi add \
    r \
    r-terra \
    r-sf
# add more packages as needed
```

Add required R packages for development.

```bash
pixi add --feature dev \
    r-styler
# add more packages as needed
```


Install the packages to dev environment.

```bash
pixi install --environment dev
```

## Use RStudio

Option 1: Run RStudio locally.

```bash
# Enter to the pixi shell environment
pixi shell --environment dev
# Use Pixi environment in RStudio
sudo sh -c "echo rsession-which-r=$(which R) > /etc/rstudio/rserver.conf"
sudo sh -c "echo rsession-ld-library-path=$(pwd)/.pixi/envs/dev/lib >> /etc/rstudio/rserver.conf"

# TODO: add R environment variables
sudo rstudio-server start

# to stop, run
# $ sudo rstudio-server stop
# to restart, run
# $ sudo rstudio-server restart
```

And open your browser to `http://localhost:8787`.
Login with your username and password.

TODO: Fix Warning: GDAL Error 1: PROJ: proj_identify: Open of /home/takahisa/Documents/git/my-project/.pixi/envs/dev/share/proj failed
