#!/bin/bash

# Exit script on error
set -e

# Download and install Miniconda
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
# bash miniconda.sh -b -p $HOME/miniconda
# export PATH="$HOME/miniconda/bin:$PATH"
# source ~/.bashrc

# Install gdown
pip install gdown

# Create necessary directories
mkdir -p data weights/2023-10-28-18-33-37 weights/2024-01-11-20-02-45

# Download weights
gdown https://drive.google.com/uc?id=1E9FPB5WFIBMLrOJqZLpoVOK4Mjzrrxhv -O weights/2023-10-28-18-33-37/
gdown https://drive.google.com/uc?id=1477-st1s1TxXN6oqfM5ZnsQwd8BCzVg1 -O weights/2023-10-28-18-33-37/
gdown https://drive.google.com/uc?id=1Zdjnkn4EHOI5_k08apofwRgTjWpai4E4 -O weights/2024-01-11-20-02-45/
gdown https://drive.google.com/uc?id=1kQkQG-q_VvLRozv30hyeLB7P_jiEEqiE -O weights/2024-01-11-20-02-45/

# Create and activate Conda environment
conda create -n foundationpose python=3.9
source activate base
conda activate foundationpose

# Install Eigen3
conda install -y conda-forge::eigen=3.4.0
export CMAKE_PREFIX_PATH="$CMAKE_PREFIX_PATH:$CONDA_PREFIX"

# Install dependencies
python -m pip install -r requirements.txt

# Install NVDiffRast
python -m pip install --quiet --no-cache-dir git+https://github.com/NVlabs/nvdiffrast.git

# Install Boost
conda install -y -c conda-forge boost

# Install PyTorch3D
python -m pip install --quiet --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py39_cu118_pyt200/download.html


# Build extensions
CMAKE_PREFIX_PATH=$CONDA_PREFIX/lib/python3.9/site-packages/pybind11/share/cmake/pybind11 bash build_all_conda.sh

# Print completion message
echo "FoundationPose setup completed successfully."
