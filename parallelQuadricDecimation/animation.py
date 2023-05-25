from quadric_decimation import QuadricDecimation

import time
import vedo

timer_id = -1


def play_animation(
    mesh_sequence,
    framerate=5,
    radius=0.005,
    landmarks=None,
    mappings=None,
    radius_landmarks=0.01,
):
    def bfunc():
        global timer_id
        plotter.timer_callback("destroy", timer_id)
        if "Play" in button.status():
            # instruct to call handle_timer() every 10 msec:
            timer_id = plotter.timer_callback("create", dt=100)
            t0 = time.time()
        button.switch()

    def handle_timer(event):
        t = time.time() - t0

        i = int(t * framerate) % len(mesh_sequence)

        if landmarks is None:
            plotter.pop().pop().pop().add(
                [
                    "Number of points: " + str(len(mesh_sequence[i].points)),
                    vedo.Mesh(mesh_sequence[i], c="k"),
                    vedo.Spheres(mesh_sequence[i].points, r=radius, c="r"),
                ]
            ).render()

        else:
            plotter.pop().pop().pop().pop().add(
                [
                    "Number of points: " + str(len(mesh_sequence[i].points)),
                    vedo.Mesh(mesh_sequence[i], c="k"),
                    vedo.Spheres(mesh_sequence[i].points, r=radius, c="r"),
                    vedo.Spheres(
                        mesh_sequence[i].points[mappings[i][landmarks]],
                        r=radius_landmarks,
                        c="b",
                    ),
                ]
            ).render()

    timer_id = -1
    t0 = time.time()
    plotter = vedo.Plotter(axes=0)
    button = plotter.add_button(bfunc, states=[" Play ", "Pause"], size=40)
    evntId = plotter.add_callback("timer", handle_timer)

    npoints = len(mesh_sequence[0].points)

    if landmarks is None:
        plotter.show(
            [
                "Number of points: " + str(npoints),
                vedo.Mesh(mesh_sequence[0], c="k"),
                vedo.Spheres(mesh_sequence[0].points, r=radius, c="r"),
            ]
        )

    else:
        plotter.show(
            [
                "Number of points: " + str(npoints),
                vedo.Mesh(mesh_sequence[0], c="k"),
                vedo.Spheres(mesh_sequence[0].points, r=radius, c="r"),
                vedo.Spheres(
                    mesh_sequence[0].points[mappings[0][landmarks]],
                    r=radius_landmarks,
                    c="b",
                ),
            ]
        )


import pyvista
import numpy as np

datafolder = "/home/louis/Environnements/singularity_homes/keops-full/GitHub/scikit-shapes-draft/data/SCAPE/scapecomp/"
reference_mesh = pyvista.read(datafolder + "/" + "mesh030.ply")

d = QuadricDecimation(target_reduction=0.99, use_numba=True)
start = time.time()
d.fit(reference_mesh)
end = time.time()
print("Fitting took " + str(end - start) + " seconds")

mesh = pyvista.read(datafolder + "/" + "mesh007.ply")
successive_decimations = []
indices_mappings = []

for stop_at in [
    0,
    1000,
    2000,
    4000,
    5000,
    6000,
    7000,
    7500,
    8000,
    8500,
    9000,
    9500,
    9750,
    10000,
    10250,
    10500,
    11000,
    11125,
    11250,
    11500,
    11750,
    12000,
    12100,
    12200,
    12300,
    12400,
]:
    start = time.time()
    decimated_mesh, indice_mapping = d.partial_transform(mesh, stop_at)
    end = time.time()
    print(
        "Decimation to "
        + str(stop_at)
        + " points took "
        + str(end - start)
        + " seconds"
    )
    successive_decimations.append(decimated_mesh)
    indices_mappings.append(indice_mapping)

# 10 random landmarks
landmarks = np.random.randint(0, len(mesh.points), 10)

play_animation(
    successive_decimations,
    framerate=8,
    radius=0.003,
    radius_landmarks=0.01,
    landmarks=landmarks,
    mappings=indices_mappings,
)


from vedo.applications import Browser

meshes = [vedo.Mesh(mesh).c("k") for mesh in successive_decimations]
plt = Browser(meshes, resetcam=0, axes=0)  # a vedo.Plotter
plt.show().close()
