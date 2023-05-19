#!/bin/bash

# Install build dependencies

# Linux/Debian
sudo add-apt-repository -y ppa:deadsnakes/ppa  # if on Ubuntu 20.04 or 18.04, building 3.10 for example
sudo apt update
sudo apt install -y ninja-build cmake libgl1-mesa-dev python3-dev git
# sudo apt install -y python3.10-dev python3.10-distutils  # if using deadsnakes + Python 3.10
# If on 18.04, you'll need a newer cmake. You can follow VTK's instructions @ https://apt.kitware.com

# Linux/CentOS
sudo yum install epel-release
sudo yum install ninja-build cmake mesa-libGL-devel mesa-libGLU-devel

# git clone https://gitlab.kitware.com/vtk/vtk.git
mkdir build
cd build
# git checkout v9.1.0  # optional to select a version, but recommended

export PYBIN=/usr/bin/python3.8  # select your version of choice
cmake -GNinja \
      -DCMAKE_BUILD_TYPE=Release \
      -DVTK_BUILD_TESTING=OFF \
      -DVTK_BUILD_DOCUMENTATION=OFF \
      -DVTK_BUILD_EXAMPLES=OFF \
      -DVTK_DATA_EXCLUDE_FROM_ALL:BOOL=ON \
      -DVTK_MODULE_ENABLE_VTK_PythonInterpreter:STRING=NO \
      -DVTK_MODULE_ENABLE_VTK_WebCore:STRING=YES \
      -DVTK_MODULE_ENABLE_VTK_WebGLExporter:STRING=YES \
      -DVTK_MODULE_ENABLE_VTK_WebPython:STRING=YES \
      -DVTK_WHEEL_BUILD=ON \
      -DVTK_PYTHON_VERSION=3 \
      -DVTK_WRAP_PYTHON=ON \
      -DVTK_OPENGL_HAS_EGL=False \
      -DPython3_EXECUTABLE=$PYBIN ../
ninja

# build wheel in dist
$PYBIN -m pip install wheel
$PYBIN setup.py bdist_wheel