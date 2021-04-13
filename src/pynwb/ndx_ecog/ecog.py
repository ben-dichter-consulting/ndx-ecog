from pynwb import get_class
import numpy as np


Parcellation = get_class('Parcellation', 'ndx-ecog')
Parcellations = get_class('Parcellations', 'ndx-ecog')
Surface = get_class('Surface', 'ndx-ecog')


def surface_init(self, name, vertices, faces, parcellations):
    if np.max(faces) >= len(vertices):
        raise ValueError(
            'index of faces exceeds number vertices for {}. Faces '
            'should be 0-indexed, not 1-indexed'.
            format(name))
    if np.min(faces) < 0:
        raise ValueError('faces hold indices of vertices and should be non-negative')
    Surface.__init__(self, name, vertices, faces, parcellations)
    
Surface.__init__ = surface_init

CorticalSurfaces = get_class('CorticalSurfaces', 'ndx-ecog')
ECoGSubject = get_class('ECoGSubject', 'ndx-ecog')
