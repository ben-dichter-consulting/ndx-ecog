# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB extension for storing the cortical surface of subjects in ECoG experiments.',
        name='ndx-ecog',
        version='0.1.1',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('Subject', namespace='core')

    surface = NWBGroupSpec(
        neurodata_type_def='Surface',
        neurodata_type_inc='NWBDataInterface',
        quantity='+',
        doc='Group representing the faces and vertices that compose a brain cortical surface.',
        datasets=[  # set Faces and Vertices as elements of the Surfaces neurodata_type
            NWBDatasetSpec(
                doc='Faces for the surface, indexes vertices.',
                shape=(None, 3),
                name='faces',
                dtype='uint32',
                dims=('face_number', 'vertex_index')),
            NWBDatasetSpec(
                doc='Vertices for surface, points in 3D space.',
                shape=(None, 3),
                name='vertices',
                dtype='float32',
                dims=('vertex_number', 'xyz'))
        ])

    surfaces = NWBGroupSpec(
        neurodata_type_def='CorticalSurfaces',
        neurodata_type_inc='NWBDataInterface',
        name='cortical_surfaces',
        doc='Group that holds Surface types.',
        quantity='?',
        groups=[surface]
    )

    images = NWBGroupSpec(
        neurodata_type_inc='Images',
        doc="Images of subject's brain.",
        name='images',
        quantity='?')

    ecog_subject = NWBGroupSpec(
        neurodata_type_def='ECoGSubject',
        neurodata_type_inc='Subject',
        name='subject',
        doc='Extension of subject that holds cortical surface data.',
        groups=[surfaces, images]
    )

    new_data_types = [ecog_subject]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
