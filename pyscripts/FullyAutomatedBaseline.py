
import sys
import cPickle
from CostMatrix import cm

class FAB:
    def __init__(self):
        self.DPR={}
        self.DLR={}
        self.DWR={}
        self.pJ={}
        self.rJ={}


    def compute_cost(self,dprFile,dlrFile,dwrFile,costMatrix):
        self.DPR=cPickle.load(open(dprFile,'rb'))
        self.DLR=cPickle.load(open(dlrFile,'rb'))
        self.DWR=cPickle.load(open(dwrFile,'rb'))

        cPP=0
        cPL=0
        cPW=0
        cLP=0
        cLL=0
        cLW=0
        cWP=0
        cWL=0
        cWW=0

        alldid=self.DPR.keys() + self.DLR.keys() + self.DWR.keys()
        for did in alldid:
            if self.DPR.__contains__(did): # Classified as R and NP
                if self.rJ[did] == 1 and self.pJ[did]==-1:
                    cPP=cPP+1
                elif self.rJ[did] == 1 and self.pJ[did]==1:
                    cPL=cPL+1      # count of Documents in PL
                elif self.rJ[did] == -1:
                    cPW=cPW+1   # count of Documents in PW
            if self.DLR.__contains__(did):  # Classified as R and P
                if self.rJ[did] == 1 and self.pJ[did]==-1:
                    cLP=cLP+1
                elif self.rJ[did] == 1 and self.pJ[did]==1:
                    cLL=cLL+1
                elif self.rJ[did] == -1:
                    cLW=cLW+1
            if self.DWR.__contains__(did):  # Classified as NR
                if self.rJ[did] == 1 and self.pJ[did]==-1:
                    cWP=cWP+1
                elif self.rJ[did] == 1 and self.pJ[did]==1:
                    cWL=cWL+1
                elif self.rJ[did] == -1:
                    cWW=cWW+1

        fac = (costMatrix[0][0]*cPP)+ (costMatrix[0][1]*cPL)+ (costMatrix[0][2]*cPW) +(costMatrix[1][0]*cLP)+(costMatrix[1][1]*cLL)+(costMatrix[1][2]*cLW)+(costMatrix[2][0]*cWP)+(costMatrix[2][1]*cWL)+(costMatrix[2][2]*cWW)

        errors=[]
        errors.append(cPP)
        errors.append(cPL)
        errors.append(cPW)
        errors.append(cLP)
        errors.append(cLL)
        errors.append(cLW)
        errors.append(cWP)
        errors.append(cWL)
        errors.append(cWW)

        print "Fully Automated Model Stats below: "
        print "Produce = ",len(self.DPR)
        print "Log = ",len(self.DLR)
        print "Withdraw = ",len(self.DWR)
        print "[PP, PL, PW, LP, LL, LW, WP, WL, WW]"
        print "[current cost matrix]= ", costMatrix
        print "[doc error count]= ", errors
        print "Fully-Automated Cost= ",fac
        print "RESULTVALUE ",fac
        print "Fully Automated Model Complete"

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
        wd=argv[0]
        rJf=argv[1]
        pJf=argv[2]
        testSetSize=argv[3]
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[4]),float(argv[5]),float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]))
        cMatrix.setAlpha(float(argv[10]))
        cmv=cMatrix.getCostMatrix()
        baselineCall=FAB()
        baselineCall.setJudgments(pJf,rJf)
        baselineCall.compute_cost(wd+'/docid-D_P-risk.dictionary.'+str(testSetSize)+'.p',wd+'/docid-D_L-risk.dictionary.'+str(testSetSize)+'.p',wd+'/docid-D_W-risk.dictionary.'+str(testSetSize)+'.p',cmv)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])

