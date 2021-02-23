from datetime import datetime
import os
import unittest

import numpy as np
from pynwb import NWBFile, NWBHDF5IO

from ndx_ecog import ECoGSubject, CorticalSurfaces, Surface, Parcellations


class ECoGSubjectTest(unittest.TestCase):

    def setUp(self):
        self.vertices = np.random.randn(20, 3)
        self.faces = np.random.randint(0, 20, (10, 3)).astype('uint')
        self.nwbfile = NWBFile('description', 'id', datetime.now().astimezone())
        self.parcellations = Parcellations()

        self.parcellations.create_parcellations(
            name='my_map',
            data=np.random.randint(0, 5, (10,)),
            labels=['a', 'b', 'c', 'd', 'e']
        )

    def test_init_ecog_subject(self):

        cortical_surfaces = CorticalSurfaces(surfaces=[
            Surface('test', vertices=self.vertices, faces=self.faces, parcellations=self.parcellations)
        ])
        self.nwbfile.subject = ECoGSubject(subject_id='id', cortical_surfaces=cortical_surfaces)
        np.testing.assert_allclose(self.nwbfile.subject.cortical_surfaces['test'].vertices, self.vertices)
        np.testing.assert_allclose(self.nwbfile.subject.cortical_surfaces['test'].faces, self.faces)
        np.testing.assert_array_equal(
            self.nwbfile.subject.cortical_surfaces['test'].parcellations['my_map'],
            self.parcellations['my_map']
        )

    def test_add_cs_to_ecog_subject(self):

        cortical_surfaces = CorticalSurfaces(surfaces=[
            Surface('test', vertices=self.vertices, faces=self.faces)
        ])
        self.nwbfile.subject = ECoGSubject()
        self.nwbfile.subject.cortical_surfaces = cortical_surfaces

    def test_io(self):

        cortical_surfaces = CorticalSurfaces(
            surfaces=[
                Surface(
                    'test',
                    vertices=self.vertices,
                    faces=self.faces,
                    parcellations=self.parcellations
                )]
        )
        self.nwbfile.subject = ECoGSubject(subject_id='id', cortical_surfaces=cortical_surfaces)

        with NWBHDF5IO('test.nwb', 'w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO('test.nwb', 'r') as io:
            nwbfile = io.read()
            np.testing.assert_allclose(
                self.nwbfile.subject.cortical_surfaces.surfaces['test'].vertices,
                nwbfile.subject.cortical_surfaces.surfaces['test'].vertices)
            np.testing.assert_allclose(
                self.nwbfile.subject.cortical_surfaces.surfaces['test'].faces,
                nwbfile.subject.cortical_surfaces.surfaces['test'].faces)

            np.testing.assert_array_equal(
                self.nwbfile.subject.cortical_surfaces['test'].parcellations['my_map'],
                nwbfile.subject.cortical_surfaces.surfaces['test'].parcellations['my_map'][:]
            )

        os.remove('test.nwb')
