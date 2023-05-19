import numpy as np
import pyvista
from gudhi.point_cloud.knn import KNearestNeighbors

class QuadricDecimation:
    '''
    This class implements the quadric decimation algorithm and make it possible to run it in parallel.
    '''

    def __init__(self, target_reduction=0.5):
        '''
        Initialize the quadric decimation algorithm with a target reduction.

        Args:
            target_reduction (float): the target reduction of the mesh.
        '''
        self.target_reduction = target_reduction

    def fit(self, mesh):
        '''
        Fit the quadric decimation algorithm on a reference mesh.
        First, the mesh is decimated with the target reduction (using vtk QuadricDecimation through pyvista wrapper).
        Then, the history of collapses and new points is read from files and the mesh is reconstructed.
        In addition, the information about the decimation process is stored in the object in order to be able to apply the 
        same decimation on other meshes that are in correspondence.

        More precisely, the following information are stored:
        - self.collapses_history : the history of collapses, a list of edges (e0, e1) that have been collapsed. The convention is that e0 is
        the point that remains and e1 is the point that is removed.
        - self.alpha the list of alpha coefficients such that when (e0, e1) collapses : e0 <- alpha * e0 + (1-alpha) * e1
        - self.faces : the faces of the decimated mesh (in padding mode)

        Args:
            mesh (pyvista.PolyData): the reference mesh.
        '''

        decimated_mesh = mesh.decimate(target_reduction=self.target_reduction)

        # Read the history of collapsed points
        file = open("~/collapses_history")
        list_str = file.readline().split()
        list_int = [int(i) for i in list_str]
        collapses_history = np.array(list_int).reshape(-1, 2)
        collapses_history = collapses_history[collapses_history[:,0] != -1]

        # Read the history of new points
        file = open("~/new_points_history")
        list_str = file.readline().split()
        list_float = [float(i) for i in list_str]
        newpoints_history = np.array(list_float).reshape(-1, 3)
        newpoints_history = newpoints_history[0:len(collapses_history)]

        # Apply the history of collapses to the mesh
        alphas = np.zeros(len(collapses_history))
        points = np.array(mesh.points.copy())
        for i in range(len(collapses_history)):
            e0, e1 = collapses_history[i]
            
            alpha = np.linalg.norm(newpoints_history[i] - points[e1]) / np.linalg.norm(points[e0] - points[e1])
            alphas[i] = alpha
            newpoint = (alpha * points[e0] + (1-alpha) * points[e1])
            points[e0] = newpoint

        keep = np.setdiff1d(np.arange(len(points)), collapses_history[:,1])
        points = points[keep]

        d_points = np.array(decimated_mesh.points.copy())

        # Error if the number of points are not the same (it happens when the target reduction is too high, TODO : understand why)
        if len(points) != len(d_points):
            raise ValueError("Different number of points, try with a smaller target reduction")
        
        # The points are not in the same order, we need to find the indices map
        # to reorder the faces of the decimated meshes
        knn = KNearestNeighbors(
            k=1,
            return_distance=False,
            return_index=True,
            implementation='ckdtree',
            n_jobs=-1).fit(d_points)
        
        indices_map = knn.transform(points)[:, 0]

        inverse_map = np.argsort(indices_map)
        faces = decimated_mesh.faces.copy().reshape(-1, 4)
        tmp = inverse_map[faces[:, 1:].copy()]
        faces[:, 1:] = tmp

        max_diff = np.abs(points - d_points[indices_map]).max()
        # Debug : check that max_diff is small

        self.alphas = alphas
        self.collapses_history = collapses_history
        self.faces = faces
        

    def transform(self, mesh):
        '''
        This function applies the decimation to a mesh that is in correspondence with the reference mesh.

        Args:
            mesh (pyvista.PolyData): the mesh to decimate.

        Returns:
            pyvista.PolyData: the decimated mesh.
        '''

        points = np.array(mesh.points.copy())

        for i in range(len(self.collapses_history)):
            e0, e1 = self.collapses_history[i]
            points[e0] = (self.alphas[i] * points[e0] + (1-self.alphas[i]) * points[e1])

        keep = np.setdiff1d(np.arange(len(points)), self.collapses_history[:,1])
        points = points[keep]

        return pyvista.PolyData(points, faces=self.faces.copy())