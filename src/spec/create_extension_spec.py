# -*- coding: utf-8 -*-

from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec
# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec

from export_spec import export_spec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB extension for storing the cortical surface of subjects in ECoG experiments',
        name='ndx-ecog',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('Subject', namespace='core')

    surface = NWBGroupSpec(
        neurodata_type_def='Surface',
        neurodata_type_inc='NWBDataInterface',
        quantity='+',
        doc='brain cortical surface',
        datasets=[  # set Faces and Vertices as elements of the Surfaces neurodata_type
            NWBDatasetSpec(
                doc='faces for surface, indexes vertices', shape=(None, 3),
                name='faces', dtype='uint32', dims=('face_number', 'vertex_index')),
            NWBDatasetSpec(
                doc='vertices for surface, points in 3D space', shape=(None, 3),
                name='vertices', dtype='float', dims=('vertex_number', 'xyz'))],
        attributes=[
            NWBAttributeSpec(
                name='help', dtype='text', doc='help',
                value='This holds Surface objects')])

    surfaces = NWBGroupSpec(
        neurodata_type_def='CorticalSurfaces',
        neurodata_type_inc='NWBDataInterface',
        name='cortical_surfaces',
        doc='triverts for cortical surfaces', quantity='?',
        groups=[surface],
        attributes=[NWBAttributeSpec(
            name='help', dtype='text', doc='help',
            value='This holds the vertices and faces for the cortical surface '
                  'meshes')])

    images = NWBGroupSpec(neurodata_type_inc='Images', doc="images of subject's brain",
                          name='images', quantity='?')

    ecog_subject = NWBGroupSpec(
        neurodata_type_def='ECoGSubject',
        neurodata_type_inc='Subject',
        name='subject',
        doc='extension of subject that holds cortical surface data',
        groups=[surfaces, images]
    )

    new_data_types = [ecog_subject]

    # export the spec to namespace and extensions files in the spec folder
    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
