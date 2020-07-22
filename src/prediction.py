"""
This module holds all preditors used by kicktipp bet bot.
A generator is a class that defines a method 'predict' with one argument.
"""
from match import Match
import random
import math


class SimplePredictor(object):
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


class CalculationPredictor(object):
    MAX_GOALS = 6
    DOMINATION_THRESHOLD = 10
    DRAW_THRESHOLD = 1.5
    NONLINEARITY = 0.6

    def predict(self, match: Match):

        difference = math.fabs(match.rate_home - match.rate_road)

        if difference < self.DRAW_THRESHOLD:
            return (1, 1)

        totalGoals = round(
            min((difference / self.DOMINATION_THRESHOLD), 1) * self.MAX_GOALS)
        ratio = ((match.rate_home / match.rate_road if match.rate_home > match.rate_road else match.rate_road / match.rate_home) / (match.rate_home + match.rate_road)) ** self.NONLINEARITY

        winner=round(totalGoals * ratio)
        looser=round(totalGoals * (1.0 - ratio))

        if winner <= looser:
            winner += 1

        if match.rate_home > match.rate_road:
            return (looser, winner)
        else:
            return (winner, looser)
