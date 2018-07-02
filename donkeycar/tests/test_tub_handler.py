# -*- coding: utf-8 -*-
import os
from donkeycar.parts.datastore import TubHandler
from .setup import tubs_dir, create_sample_tubs


def test_create_tub_handler(tubs_dir):
    th = TubHandler(tubs_dir)
    assert th is not None


def test_get_tub_list(tubs_dir):
    # Create 5 tubs
    create_sample_tubs(tubs_dir)

    th = TubHandler(tubs_dir)
    assert len(th.get_tub_list()) == 5


def test_next_tub_number(tubs_dir):
    # Create 5 tubs
    create_sample_tubs(tubs_dir)

    th = TubHandler(tubs_dir)
    assert th.next_tub_number() == 5


def test_new_tub_writer(tubs_dir):
    # Create 5 tubs
    create_sample_tubs(tubs_dir)

    # Add new tub writer to handler
    th = TubHandler(tubs_dir)
    inputs=['cam/image_array', 'angle', 'throttle']
    types=['image_array', 'float', 'float']
    tw = th.new_tub_writer(inputs, types)

    assert len(th.get_tub_list()) == 6
    assert int(tw.path.split('_')[-2]) == 5