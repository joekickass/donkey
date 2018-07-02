# -*- coding: utf-8 -*-
import os
import pytest

from donkeycar.parts.keras import KerasPilot, KerasLinear
from donkeycar.parts.keras import default_linear
from .setup import models_dir, model, pilot
from .setup import tubs_dir, create_sample_tubs


def test_create_linear():
    kl = KerasLinear()
    assert kl.model is not None


def test_create_linear_with_model(model):
    kl = KerasLinear(model)
    assert kl.model is not None


def test_train_model(models_dir, tubs_dir, pilot):
    """ Test train model for 1 epoch """
    # Create a tub with 100 records
    tub = create_sample_tubs(tubs_dir, cnt=1, records=100)[0]

    # Create path to model
    model_path = os.path.join(models_dir, 'test-train-model')

    # Create generators
    x = ['cam/image_array']
    y = ['angle', 'throttle']
    train_gen, val_gen = tub.get_train_val_gen(x, y)

    ret = pilot.train(train_gen, val_gen, model_path, epochs=1)

    assert ret is not None
