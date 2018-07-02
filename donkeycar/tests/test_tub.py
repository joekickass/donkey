# -*- coding: utf-8 -*-
import os
import pytest
import tempfile
import tarfile
from PIL import Image
from donkeycar.parts.datastore import Tub
from .setup import tubs_dir
from .setup import create_sample_tubs, create_sample_tub, create_sample_record


def test_tub_create_from_nonexisting_path(tubs_dir):
    # Create non-existing path
    tub_path = os.path.join(tubs_dir, 'tub_0')

    # Create a new tub by specifying inputs & types
    inputs=['cam/image_array', 'angle', 'throttle']
    types=['image_array', 'float', 'float']
    t = Tub(tub_path, inputs=inputs, types=types)

    assert t is not None


def test_tub_create_from_nonexisting_path_wo_inputs_raises_error(tubs_dir):
    # Create non-existing path
    tub_path = os.path.join(tubs_dir, 'tub_0')

    # Try create tub without inputs
    with pytest.raises(AttributeError):
        Tub(tub_path)

def test_tub_load(tubs_dir):
    # The sample tub will create a directory with metadata
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]
    path = tub.path

    t = Tub(path)
    assert t is not None


def test_tub_load_empty_dir_raises_error(tubs_dir):
    # Create an empty dir (missing tub metadata)
    tub_dir = os.mkdir(os.path.join(tubs_dir, 'tub_0'))
    with pytest.raises(TypeError):
        Tub(tub_dir)


def test_get_last_ix(tubs_dir):
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    assert tub.get_last_ix() == 9


def test_get_last_ix_after_adding_new_record(tubs_dir):
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Add a new record
    record = create_sample_record()
    tub.put_record(record)

    assert tub.get_last_ix() == 10


def test_get_last_ix_for_empty_tub(tubs_dir):
    # Create an empty dir (missing tub metadata)
    tub_path = os.path.join(tubs_dir, 'tub_0')

    # Create a new tub by specifying inputs & types
    inputs=['cam/image_array', 'angle', 'throttle']
    types=['image_array', 'float', 'float']
    t = Tub(tub_path, inputs=inputs, types=types)

    assert t.get_last_ix() == -1


def test_get_last_ix_for_one_record(tubs_dir):
    # Create a tub with 1 records
    tub = create_sample_tubs(tubs_dir, cnt=1, records=1)[0]

    assert tub.get_last_ix() == 0


def test_tub_update_df(tubs_dir):
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    tub.update_df()

    assert len(tub.df) == 10


def test_tub_get_df(tubs_dir):
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    df = tub.get_df()

    assert len(df) == 10


def test_tub_add_record(tubs_dir):
    """Tub can save a record and then retrieve it."""
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Create and add new record
    rec_in = create_sample_record()
    rec_index = tub.put_record(rec_in)

    rec_out = tub.get_record(rec_index-1)
    assert rec_in.keys() == rec_out.keys()


def test_tub_get_num_records(tubs_dir):
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    cnt = tub.get_num_records()
    assert cnt == 10


def test_tub_check_removes_illegal_records(tubs_dir):
    """ Check removes illegal records """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    record = tub.get_json_record_path(tub.get_last_ix())
    with open(record, 'w') as f:
        f.write('illegal json data')
    assert tub.get_num_records() == 10

    tub.check(fix=True)
    assert tub.get_num_records() == 9


def test_tub_remove_record(tubs_dir):
    """ Remove record from tub """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]
    assert tub.get_num_records() == 10

    tub.remove_record(0)
    assert tub.get_num_records() == 9


def test_tub_put_image(tubs_dir):
    """ Add an encoded image to the tub """
    # Create non-existing path
    tub_path = os.path.join(tubs_dir, 'tub_0')

    # Create new tub with image type
    inputs = ['user/speed', 'cam/image']
    types = ['float', 'image']
    img = Image.new('RGB', (120, 160))
    t=Tub(path=tub_path, inputs=inputs, types=types)

    # Add encoded img
    t.put_record({'cam/image': img, 'user/speed': 0.2, })

    assert t.get_record(t.get_last_ix())['user/speed'] == 0.2


def test_tub_put_unknown_type(tubs_dir):
    """ Creating a record with unknown type should fail """
    # Create non-existing path
    tub_path = os.path.join(tubs_dir, 'tub_0')

    # Try create tub with unknown type
    inputs = ['user/speed']
    types = ['bob']
    t=Tub(path=tub_path, inputs=inputs, types=types)
    with pytest.raises(TypeError):
        t.put_record({'user/speed': 0.2, })


def test_delete_tub(tubs_dir):
    """ Delete the tub content """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]
    assert tub.get_num_records() == 10

    # Delete all content
    tub.delete()
    assert tub.get_num_records() == 0


def test_get_record_gen(tubs_dir):
    """ Create a records generator and pull 20 records from it """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Create records generator
    records = tub.get_record_gen()

    assert len([ next(records) for x in range(20) ]) == 20


def test_get_batch_gen(tubs_dir):
    """ Create a batch generator and pull 1 batch (128) records from it """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Create a batch generator
    batches = tub.get_batch_gen()
    batch = next(batches)

    assert len( batch.keys() ) == 3
    assert len( list( batch.values() )[0] ) == 128


def test_get_train_val_gen(tubs_dir):
    """ Create training and validation generators. """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Create generators
    x = ['angle', 'throttle']
    y = ['cam/image_array']
    train_gen, val_gen = tub.get_train_val_gen(x, y)

    train_batch = next(train_gen)
    assert len(train_batch)

    # X is a list of all requested features (angle & throttle)
    X = train_batch[0]
    assert len(X) == 2
    assert len(X[0]) == 128
    assert len(X[1]) == 128

    # Y is a list of all requested labels (image_array)
    Y = train_batch[1]
    assert len(Y) == 1
    assert len(Y[0]) == 128

    val_batch = next(val_gen)
    # X is a list of all requested features (angle & throttle)
    X = val_batch[0]
    assert len(X) == 2
    assert len(X[0]) == 128
    assert len(X[1]) == 128

    # Y is a list of all requested labels (image_array)
    Y = train_batch[1]
    assert len(Y) == 1
    assert len(Y[0]) == 128


def test_tar_records(tubs_dir):
    """ Tar all records in the tub """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    # Save the tar file in a temporary dir
    with tempfile.TemporaryDirectory() as tmpdirname:
        tar_path = os.path.join(tmpdirname, 'tub.tar.gz')
        tub.tar_records(tar_path)

        # tar file should hold 10 records + metadata file
        with tarfile.open(name=tar_path, mode='r') as t:
            assert len(t.getnames()) == 11


def test_recreating_tub(tubs_dir):
    """ Recreating a Tub should restore it to working state """
    # Create a tub with 10 records
    tub = create_sample_tubs(tubs_dir, cnt=1)[0]

    assert tub.get_num_records() == 10
    assert tub.current_ix == 10
    assert tub.get_last_ix() == 9
    path = tub.path
    tub = None

    inputs=['cam/image_array', 'angle', 'throttle']
    types=['image_array', 'float', 'float']
    t = Tub(path, inputs=inputs, types=types)
    assert t.get_num_records() == 10
    assert t.current_ix == 10
    assert t.get_last_ix() == 9