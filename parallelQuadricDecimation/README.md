## Description

This is a small python module to improve the current implementation of quadricDecimation by tracking the sequence of collapses. It has two main application :
- Given a set of meshes that are in correspondence, apply the same decimation to all of them to keep the correspondence
- Given a mesh with a subset of vertices as landmarks, know where to project the landmarks

## Installation

So far to make it run :
- Build the vtk's wheel with `bash ../build_wheel.sh` (see pyvistadoc to adapt the script on your python version)
- install pyvista, vedo
- reinstall vtk with `pip install ../build/dist/name_of_wheel.whl`
- quadric_decimation depends also on scipy and gudhi to nearest neighbors computations

## TODO list :

### Cpp code / wrapping
- Understand deeper the algo : why the return of pyvista.decimate is not in the same order as our manual decimation and imposes us te reorder points ? Does it come from pyVista or from vtk ? -> apparently from vtk, what is the logic behind ?
- Why with a high target reduction there is a mismatch between manual decimation and pyvista.decimate (example with the cow and target_reduction=0.95) ? At first glance it seems to happen when a topological change append, maybe this is good to alert the user and stop decimation before it happens ?
- how to integrate this slighty modified vtk in scikit-shapes ? -> look at CMake/vtkWheel* to modify the name of the library and avoid potential conflict with true vtk (OK solution but heavy)


