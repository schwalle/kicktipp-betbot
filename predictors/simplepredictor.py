"""
Simple preditor for kicktipp bet bot.
"""
from helper.match import Match
from .base import PredictorBase
import random
import math


class SimplePredictor(PredictorBase):
    DOMINATION_THRESHOLD = 6
    DRAW_THRESHOLD = 1.2
    
    def predict(self, match: Match):

        diff = math.fabs(match.rate_home - match.rate_road)
        home_wins = match.rate_home < match.rate_road

        if diff < self.DRAW_THRESHOLD:
            return (1, 1)

        if diff >= self.DOMINATION_THRESHOLD:
            result = (3, 1)
        elif diff >= self.DOMINATION_THRESHOLD / 2:
            result = (2, 1)
        else:
            result = (1, 0)

        return result if home_wins else tuple(reversed(result))
