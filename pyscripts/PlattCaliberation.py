
import math
import sys
import numpy as np
from scipy.optimize import fmin_bfgs
from sklearn.utils import column_or_1d

class caliberate:
    def __init__(self):
        self.maxiter=100     #Maximum number of iterations
        self.minstep=1*math.pow(10,-12)  #Minimum step taken in line search
        self.sigma=1*math.pow(10,-12)     #Set to any value > 0

    def getLabels(self,fpath):
        labs={}
        f = open(fpath, 'r')
        lines=f.readlines()
        f.close()
        ctr=1
        for l in lines:
            labs[ctr]=int(l.strip('\n'))
            ctr=ctr+1
        return labs

    def getDecisions(self,fpath):
        deci={}
        f = open(fpath, 'r')
        lines=f.readlines()
        f.close()
        ctr=1
        for l in lines:
            deci[ctr]=float(l.strip('\n'))
            ctr=ctr+1
        return deci

    def _sigmoid_calibration(self,df, y, sample_weight=None):
        """Probability Calibration with sigmoid method (Platt 2000)
        Parameters
        ----------
        df : ndarray, shape (n_samples,)
            The decision function or predict proba for the samples.
        y : ndarray, shape (n_samples,)
            The targets.
        sample_weight : array-like, shape = [n_samples] or None
            Sample weights. If None, then samples are equally weighted.
        Returns
        -------
        a : float
            The slope.
        b : float
            The intercept.
        References
        ----------
        Platt, "Probabilistic Outputs for Support Vector Machines"
        """
        df = column_or_1d(df)
        y = column_or_1d(y)

        F = df  # F follows Platt's notations in the Reference Paper
        tiny = np.finfo(np.float).tiny  # to avoid division by 0 warning

        # Bayesian priors (see Platt end of section 2.2 in the Reference Paper)
        prior0 = float(np.sum(y <= 0))
        prior1 = y.shape[0] - prior0
        T = np.zeros(y.shape)
        T[y > 0] = (prior1 + 1.) / (prior1 + 2.)
        T[y <= 0] = 1. / (prior0 + 2.)
        T1 = 1. - T

        def objective(AB):
            # From Platt (beginning of Section 2.2 in the Reference Paper)
            E = np.exp(AB[0] * F + AB[1])
            P = 1. / (1. + E)
            l = -(T * np.log(P + tiny) + T1 * np.log(1. - P + tiny))
            if sample_weight is not None:
                return (sample_weight * l).sum()
            else:
                return l.sum()

        def grad(AB):
            # gradient of the objective function
            E = np.exp(AB[0] * F + AB[1])
            P = 1. / (1. + E)
            TEP_minus_T1P = P * (T * E - T1)
            if sample_weight is not None:
                TEP_minus_T1P *= sample_weight
            dA = np.dot(TEP_minus_T1P, F)
            dB = np.sum(TEP_minus_T1P)
            return np.array([dA, dB])

        AB0 = np.array([0., math.log((prior0 + 1.) / (prior1 + 1.))])
        AB_ = fmin_bfgs(objective, AB0, fprime=grad, disp=False)
        return (AB_[0], AB_[1])



def main(argv):
    try:
        c=caliberate()
        tLabels = c.getLabels(argv[0])
        tDecisions=c.getDecisions(argv[1])
        tL=np.array(tLabels.values())
        tD=np.array(tDecisions.values())
        tup=c._sigmoid_calibration(tD,tL)
        print tup
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])





