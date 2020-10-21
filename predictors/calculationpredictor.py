"""
Calculation preditor for kicktipp bet bot.
"""
from helper.match import Match
from .base import PredictorBase
import math


class CalculationPredictor(PredictorBase):
    MAX_GOALS = 5
    DOMINATION_THRESHOLD = 9
    DRAW_THRESHOLD = 1.3
    NONLINEARITY = 0.5

    def predict(self, match: Match):

        difference = math.fabs(match.rate_home - match.rate_road)

        if difference < self.DRAW_THRESHOLD:
            return (1, 1)

        totalGoals = round(
            min((difference / self.DOMINATION_THRESHOLD), 1) * self.MAX_GOALS)
        ratio = ((match.rate_home / match.rate_road if match.rate_home > match.rate_road else match.rate_road /
                  match.rate_home) / (match.rate_home + match.rate_road)) ** self.NONLINEARITY

        winner = round(totalGoals * ratio)
        looser = round(totalGoals * (1.0 - ratio))

        if winner <= looser:
            winner += 1

        if match.rate_home > match.rate_road:
            return (looser, winner)
        else:
            return (winner, looser)
