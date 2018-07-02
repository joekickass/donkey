# -*- coding: utf-8 -*-
from donkeycar.parts.datastore import TubGroup
from .setup import tubs_dir, create_sample_tubs


def test_tubgroup_load(tubs_dir):
    """ Load TubGroup from existing tubs dir """
    # Create 5 tubs
    tubs = create_sample_tubs(tubs_dir)
    paths = [ tub.path for tub in tubs ]

    # Create a TubGroup using a comma separated string
    str_of_tubs = ','.join(paths)
    t = TubGroup(str_of_tubs)
    assert t is not None


def test_tubgroup_inputs(tubs_dir):
    """ Get TubGroup inputs """
    # Create 5 tubs
    tubs = create_sample_tubs(tubs_dir)
    paths = [ tub.path for tub in tubs ]

    # Create a TubGroup using a comma separated string
    str_of_tubs = ','.join(paths)
    t = TubGroup(str_of_tubs)

    assert sorted(t.inputs) == sorted(['cam/image_array', 'angle', 'throttle'])


def test_tubgroup_types(tubs_dir):
    """ Get TubGroup types """
    # Create 5 tubs
    tubs = create_sample_tubs(tubs_dir)
    paths = [ tub.path for tub in tubs ]

    # Create a TubGroup using a comma separated string
    str_of_tubs = ','.join(paths)
    t = TubGroup(str_of_tubs)

    assert sorted(t.types) == sorted(['image_array', 'float', 'float'])


def test_tubgroup_get_num_tubs(tubs_dir):
    """ Get number of tubs in TubGroup """
    # Create 5 tubs
    tubs = create_sample_tubs(tubs_dir)
    paths = [ tub.path for tub in tubs ]

    # Create a TubGroup using a comma separated string
    str_of_tubs = ','.join(paths)
    t = TubGroup(str_of_tubs)

    assert t.get_num_tubs() == 5


def test_tubgroup_get_num_records(tubs_dir):
    """ Get number of records in TubGroup """
    # Create 5 tubs with 5 records each
    tubs = create_sample_tubs(tubs_dir, records=5)
    paths = [ tub.path for tub in tubs ]

    # Create a TubGroup using a comma separated string
    str_of_tubs = ','.join(paths)
    t = TubGroup(str_of_tubs)

    assert t.get_num_records() == 5*5
