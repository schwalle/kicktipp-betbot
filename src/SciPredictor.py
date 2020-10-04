import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class MatchPredictor:
    """ Class to calculates the probabilities for different scores (outcomes) of two teams.

    Attributes
    ----------
    l1 : float
        Projected score for team 1 (expectation value for Poisson distribution)
    l2 : float
        Projected score for team 2 (expectation value for Poisson distribution)
    """

    def __init__(self, l1=0.0, l2=0):
        self._poisson_n_bins = 8

        self.l1 = l1
        self.l2 = l2

    def poisson_pmf(self, l, n_bins=None):
        """ Returns the probablity mass function of the Poissonian distribution with average number l
        See https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html

        Parameters
        ----------
        l : float
            Average number of events per interval ("shape parameter")
        n_bins : int
            Number of bins. If None (default), the value from the class attribute _poisson_n_bins is used.

        Returns
        -------
        Probability mass function of Poisson distribution
        """
        if n_bins is None:
            n_bins = self._poisson_n_bins

        n = np.arange(0, n_bins)
        return stats.poisson.pmf(n, l)

    def calculate_score_probs(self, mode='all'):
        """ Calculates the probabilities for different scores (outcomes) of two teams. The required information is
        the expection value for their goal distributions l1 and l2 (class attributes).

        Parameters
        ----------
        mode : str, {'all' (default), 'draws', 'team1_wins', 'team2_wins'}
            If 'all', the complete probabiliy matrix is returned. If 'draw' only the diagonal elements (corresponding to
            all possible draws) are non-zero. If 'team1_wins', only the elements corresponding to outcomes where team 1
            wins are non-zero. 'team2_wins' is analaog to 'team1_wins'.

        Returns
        -------
        nd.array
            The returned matrix is a quadratic 2x2 matrix. The first dimension corresponds to team 1, second dimension
            to team 2. E.g. score_probs[2,1] gives the probability for the score being 2:1


        """
        y1 = self.poisson_pmf(self.l1)
        y2 = self.poisson_pmf(self.l2)

        score_probs = np.tensordot(y1, y2, axes=0)  # vector * vector => matrix
        if mode == 'all':
            pass
        elif mode == 'draws':
            # diagonal elements correspond to probabilites of the draws (0:0, 1:1, 2:2, ...)
            score_probs = np.diag(np.diag(score_probs))
        elif mode == 'team1_wins':
            # elements of lower left triangle (excluding diagonals => k=-1) correspond to probabilies for outcomes at
            # which team 1 wins (1:0, 2:0, 2:1, ...)
            score_probs = np.tril(score_probs, k=-1)
        elif mode == 'team2_wins':
            # elements of upper right triangle (excluding diagonals => k=1) correspond to probabilies for outcomes at
            # which team 2 wins (0:1, 0:2, 1:, ...)
            score_probs = np.triu(score_probs, k=1)
        else:
            raise(ValueError('Invalid value for "mode".'))

        return score_probs

    @staticmethod
    def plot_score_probs(score_probs):
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        ax.imshow(score_probs, cmap='jet')
        ax.set_ylabel('Goals Team 1')
        ax.set_xlabel('Goals Team 2')
        ax.set_title('Score probabilites (%)')
        # write probability (in %) in each element of the matrix
        for (j, i), label in np.ndenumerate(score_probs):
            ax.text(i, j, round(label*100, 1), ha='center', va='center')
        plt.show()

    def plot_poisson_pmf(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        n_bins = np.arange(0, self._poisson_n_bins)
        y1 = self.poisson_pmf(self.l1)
        y2 = self.poisson_pmf(self.l2)

        ax.plot(n_bins, y1, 'o-', color='red', label='Team 1')
        ax.plot(n_bins, y2, 'o-', color='blue', label='Team 2')

        ax.set_xlabel('Scored goals')
        ax.set_ylabel('Probability')
        ax.set_title('Poisson distribution')
        ax.grid()
        ax.legend()

        plt.show()

    @property
    def probs_tendency(self):
        """ Calculate the probability for the "tendency" of the outcome for a match played by two teams.

        Returns
        -------
        list with 3 elements
            [probability team 1 wins, probability team 2 wins, probabilty for a draw]
        """
        p_team1 = np.sum(self.calculate_score_probs(mode='team1_wins'))
        p_team2 = np.sum(self.calculate_score_probs(mode='team2_wins'))
        p_draw = np.sum(self.calculate_score_probs(mode='draws'))

        return [p_team1, p_team2, p_draw]

    def prob_goal_difference(self, d, mode='all'):
        """ Calculate the probability for the goal difference of the match played by two teams to be d.

        Parameters
        ----------
        d : int
            Goal difference. Positive: team 1 wins, negative: team 2 wins, 0: draw
        mode : str
            Passed to call of calculate_score_probs. See definition there.

        Returns
        -------
        float
            Probability

        """
        score_probs = self.calculate_score_probs(mode=mode)
        k = -1*d
        # Parameter k: defines which diagonal axis offset to main diagonal is used. The axis offset by -d corresponds to
        # the outcomes with a goal difference of d.
        return np.sum(np.diag(score_probs, k=k))

    def most_likely_goal_difference(self, mode='all'):

        # calculate probabilities for all possible goal differences (limited by the width of the Poisson distribution)
        d_ar = np.arange(-(self._poisson_n_bins-1), self._poisson_n_bins)
        prob = np.zeros(len(d_ar))
        for idx, d in enumerate(d_ar):
            prob[idx] = self.prob_goal_difference(d, mode)

        return d_ar[np.argmax(prob)], np.max(prob)

    def most_likely_score(self, d=None, mode='all'):
        """ Returns the most likely score.
        Parameters "mode" and "d" set furhter constrains on the subset of score probabilites to be considered.

        Parameters
        ----------
        d : int
            Goal difference. Positive: team 1 wins, negative: team 2 wins, 0: draw
        mode : str
            Passed to call of calculate_score_probs. See definition there.

        Returns
        -------
        tuple
            ([result], probability) e.g. ([2,1], 0.06)
        """
        score_probs = self.calculate_score_probs(mode=mode)
        if d is not None:
            # Set all elements except the diagonal offset by -d to zero
            # Remaining non-zero elements correspond to results with a goal difference of d.
            score_probs = np.diag(np.diag(score_probs, k=-d), k=-d)
        result = list(np.unravel_index(np.argmax(score_probs), score_probs.shape))  # gets the indicies with the highest
        # probability inside score_probs as list.
        # See: https://stackoverflow.com/questions/9482550/argmax-of-numpy-array-returning-non-flat-indices

        prob = np.max(score_probs)

        return result, prob

    @property
    def predicted_score(self):
        # 1) Calculate most likely tendency
        tendency = np.argmax(self.probs_tendency)  # 0: team 1 wins, 1: team 2 wins, 2: draw

        # 2) What is the most likely goal difference within the tendency
        if tendency == 0:
            mode ='team1_wins'
        elif tendency == 1:
            mode = 'team2_wins'
        elif tendency == 2:
            mode = 'draws'
        else:
            raise(ValueError('Invalid value for tendendy'))
        d, _ = self.most_likely_goal_difference(mode=mode)

        # 3) What is the most likely result with the predicted goal difference?
        return self.most_likely_score(d=d, mode=mode)


if __name__ == "__main__":
    mp = MatchPredictor(0.2, 0.4)
    mp.plot_poisson_pmf()
    #mp.plot_score_probs(mp.calculate_score_probs)

    pass