from helper.match import Match
import pkgutil
import importlib
import os.path

class PredictorBase():
    """
    Predictor base class
    all actual predictors shall derive from this class and implement the predict method
    """
    def predict(self, match: Match):
        """
        predict a match by returning the number of goals as tuple (home_goals, road_goals)
        """
        raise NotImplementedError

def explore_package():    
    return [sub_module_name for _, sub_module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)])]

def get_predictors():
    """
    Get all predictors from all modules in this folder
    return: dict{name:str, cls:class}
    """
    for mod in explore_package():
        importlib.import_module('.'+mod, __package__)
    return {cls.__name__: cls for cls in PredictorBase.__subclasses__()}