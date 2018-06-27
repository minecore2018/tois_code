
import sys
import cPickle

class FMB:
    def __init__(self):
        self.lam_r=1.0
        self.lam_p=5.0
        self.DPR={}
        self.DLR={}
        self.DWR={}
        self.pJ={}
        self.rJ={}

    def computeCost(self, testInstances, testInsCounter):
        #all D (testInsCounter) number of documents are reviewed for responsiveness.
        Truth_responsives=0
        Truth_privileges=0

        tau_r=testInsCounter
        cost_rreview=self.lam_r * int(tau_r)

        ts = open(testInstances, "r")
        testInslines=ts.readlines()
        ts.close()
        tau_p=0
        for ti in testInslines:
            if self.rJ[int(ti.strip('\n'))] == 1:
                tau_p=tau_p+1
                Truth_responsives=Truth_responsives+1
            if self.pJ[int(ti.strip('\n'))] == 1:
                Truth_privileges=Truth_privileges+1

        cost_preview=self.lam_p * tau_p
        total_cost=cost_rreview+cost_preview

        print "Total Responsive Truth (Gold Standard)= ",Truth_responsives
        print "Tau_r (To be Reviewed by a Human)= ",tau_r
        print "Total Privilege Truth (Gold Standard)= ",Truth_privileges
        print "Tau_p (To be Reviewed by a Human)= ",tau_p
        print "Fully-Manual Cost= ",total_cost
        print "RESULTVALUE ",total_cost

    def setJudgments(self,pJudgmentsFile,rJudgmentsFile):
        pRJ = open(pJudgmentsFile, "r")
        pRJls=pRJ.readlines()
        pRJ.close()
        for pRJln in pRJls:
            pjFields=pRJln.strip('\n').split(" ")
            self.pJ[int(pjFields[0])]=int(pjFields[1])
        rRJ = open(rJudgmentsFile, "r")
        rRJls=rRJ.readlines()
        rRJ.close()
        for rRJln in rRJls:
            rjFields=rRJln.strip('\n').split(" ")
            self.rJ[int(rjFields[0])]=int(rjFields[1])

def main(argv):
    try:
        baselineCall=FMB()
        rJf=argv[0]
        pJf=argv[1]
        testSetSize=argv[2]
        baselineCall.setJudgments(pJf,rJf)
        baselineCall.computeCost(argv[3],testSetSize) 

    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
