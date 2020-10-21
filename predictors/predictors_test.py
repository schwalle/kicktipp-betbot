import pytest
from . import base

def test_scanpreditors():
    subpackages = base.explore_package()
    assert len(subpackages) > 0
    pass

def test_instanciatepreditors():
    predictors = base.get_predictors()
    assert 'SimplePredictor' in predictors.keys()
    predictorobj = predictors['SimplePredictor']()
    assert issubclass(type(predictorobj), base.PredictorBase)
    pass