from quadric_decimation import QuadricDecimation
import pyvista
import numpy as np

datafolder = "/home/louis/Environnements/singularity_homes/keops-full/GitHub/face_data/data/cranes/raw"


reductions = [0.5, 0.8, 0.9, 0.95, 0.99, 0.995]

for r in reductions:

    #Decimate a mesh
    reference_mesh = pyvista.read(datafolder + "/" + "patient_1_229_m.obj")
    d = QuadricDecimation(target_reduction=r, use_numba=True)
    d.fit(reference_mesh)

    # Save decimation infos
    tmp = str(r).replace(".", "_")
    np.save(f"alphas{tmp}.npy", d.alphas)
    np.save(f"collapses{tmp}.npy", d.collapses_history)
    np.save(f"faces{tmp}.npy", d.faces)