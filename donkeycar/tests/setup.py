import os
import platform
import pytest

from donkeycar.parts.datastore import Tub
from donkeycar.parts.keras import KerasLinear, default_linear
from donkeycar.parts.simulation import SquareBoxCamera, MovingSquareTelemetry


def on_pi():
    if 'arm' in platform.machine():
        return True
    return False


@pytest.fixture
def tubs_dir(tmpdir):
    tubs_dir = str(tmpdir.mkdir('tubs'))
    return tubs_dir


@pytest.fixture
def tub_dir_created(tub_dir):
    tubs_dir, tub_dir = tub_dir

    return (tubs_dir, tub_dir)


@pytest.fixture
def empty_tub(tub_dir):
    tubs_dir, tub_dir = tub_dir
    return Tub(tub_dir)


def create_sample_tubs(root_dir, cnt=5, records=10):
    '''
    Create samples of tubs with records. You can specify both how many tubs to create, and
    how many records each tub should contain.
    '''
    tub_paths = [ os.path.join(root_dir, 'tub_{}'.format(i)) for i in range(cnt) ]
    return [ create_sample_tub(tub_path, records=records) for tub_path in tub_paths ]


def create_sample_tub(path, records=10):
    inputs=['cam/image_array', 'angle', 'throttle']
    types=['image_array', 'float', 'float']
    t = Tub(path, inputs=inputs, types=types)
    for _ in range(records):
        record = create_sample_record()
        t.put_record(record)
    return t


def create_sample_record():
    cam = SquareBoxCamera()
    tel = MovingSquareTelemetry()
    x, y = tel.run()
    img_arr = cam.run(x, y)
    angle = x
    throttle = y
    return {'cam/image_array': img_arr, 'angle': angle, 'throttle': throttle }


@pytest.fixture
def models_dir(tmpdir):
    models_dir = tmpdir.mkdir('models')
    return str(models_dir)


@pytest.fixture
def model():
    return default_linear()


@pytest.fixture
def pilot(model):
    return KerasLinear(model)