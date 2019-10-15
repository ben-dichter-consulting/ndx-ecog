# -*- coding: utf-8 -*-

from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec
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

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    tetrode_series = NWBGroupSpec(
        neurodata_type_def='TetrodeSeries',
        neurodata_type_inc='ElectricalSeries',
        doc=('An extension of ElectricalSeries to include the tetrode ID for '
             'each time series.'),
        attributes=[
            NWBAttributeSpec(
                name='trode_id',
                doc='The tetrode ID.',
                dtype='int32'
            )
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [tetrode_series]

    # TODO: specify the types that are used by the extension and their
    # namespaces
    ns_builder.include_type('ElectricalSeries', namespace='core')

    # export the spec to namespace and extensions files in the spec folder
    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
