# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBDatasetSpec,
    NWBAttributeSpec
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB extension for storing the cortical surface of subjects in ECoG experiments.',
        name='ndx-ecog',
        version='0.3.1',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@catalystneuro.com'.split(',')))
    )

    core_ndtypes = ['NWBDataInterface', 'Subject', 'Images', 'NWBData']
    for ndtype in core_ndtypes:
        ns_builder.include_type(ndtype, namespace='core')

    Parcellation = NWBDatasetSpec(
        neurodata_type_def='Parcellation',
        doc='a parcellation of the surface',
        shape=(None,),
        dims=('vertex_index',),
        attributes=[
            NWBAttributeSpec(
                name='labels',
                doc='if the dtype of the parcellation is uint, they are '
                    'categories and these are the labels',
                dtype='text',
                shape=(None,),
                required=False
            )
        ]
    )

    Parcellations = NWBGroupSpec(
        default_name='parcellations',
        neurodata_type_def='Parcellations',
        neurodata_type_inc='NWBDataInterface',
        doc='parcellations of this surface',
        datasets=[
            NWBDatasetSpec(
                neurodata_type_inc='Parcellation',
                doc='a parcellation of this surface',
                quantity='+'
            )
        ]
    )

    surface = NWBGroupSpec(
        neurodata_type_def='Surface',
        neurodata_type_inc='NWBDataInterface',
        quantity='?',
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
        ],
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='Parcellations',
                doc='parcellations for this surface',
                quantity='?'
            )
        ]
    )

    surfaces = NWBGroupSpec(
        neurodata_type_def='CorticalSurfaces',
        neurodata_type_inc='NWBDataInterface',
        name='cortical_surfaces',
        doc='Group that holds Surface types.',
        quantity='?',
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='Surface',
                quantity='*',
                doc='Group representing the faces and vertices that compose a brain cortical surface.',
            )
        ]
    )

    ecog_subject = NWBGroupSpec(
        neurodata_type_def='ECoGSubject',
        neurodata_type_inc='Subject',
        name='subject',
        doc='Extension of subject that holds cortical surface data.',
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='CorticalSurfaces',
                doc='Group representing the faces and vertices '
                    'that compose a brain cortical surface.',
                quantity='?'),
            NWBGroupSpec(
                neurodata_type_inc='Images',
                doc='Images of the brain',
                quantity='?'
            )
        ]
    )

    new_data_types = [surface, surfaces, ecog_subject, Parcellation, Parcellations]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
