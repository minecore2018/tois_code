

import sys
from CostMatrix import cm
import cPickle

class computeCa:
    def __init__(self):
        self.tauR=0
        self.tauP=0

    def compute(self,lamR,tauR,lamP,tauP):
        return float((lamR*tauR) + (lamP*tauP))

    def set_tauP(self,tP):
        self.tauP=cPickle.load(open(tP,'rb'))

    def set_tauR(self,tR):
        self.tauR=cPickle.load(open(tR,'rb'))

    def get_tauR(self):
        return int(self.tauR)

    def get_tauP(self):
        return int(self.tauP)

def main(argv):
    try:
        wd= argv[0] # Joint Cost Model's Working Directory (Specific Resp and Priv Cat )
        numTestInstances=argv[1] # 10000#argv[3]
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[2]),float(argv[3]),float(argv[4]),float(argv[5]),float(argv[6]),float(argv[7]))
        cMatrix.setAlpha(float(argv[8]))
        lamR=cMatrix.getLam_r()
        lamP=cMatrix.getLam_p()
        cca=computeCa()
        cca.set_tauP(wd+'/tauP_value.'+str(numTestInstances)+'.p')
        cca.set_tauR(wd+'/tauR_value.'+str(numTestInstances)+'.p')
        annotation_cost = cca.compute(lamR,cca.get_tauR(),lamP,cca.get_tauP())
        print "The total annotation cost is: ", annotation_cost
        print "RESULTVALUE ",annotation_cost
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])