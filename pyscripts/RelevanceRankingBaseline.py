
## Relevance Ranking Baseline Model

import sys
import cPickle
from collections import OrderedDict
from ModuleP2 import phase2
from ModuleP3 import phase3
from CostMatrix import cm


class RelevanceRankingBaseline:
    def __init__(self):
        self.mcDocumentMatrix=[[0 for x in range(3)] for x in range(3)]

    def get_tauR(self,trval):
        tr=cPickle.load(open(trval,'rb'))
        return int(tr)

    def get_tauP(self,tpval):
        tp=cPickle.load(open(tpval,'rb'))
        return int(tp)

    def RankByProbability(self,dictVal,order):
        rankedDict={}
        for key,tup in dictVal.iteritems():
            rankedDict[key]=tup[0]
        if order=="DEC":
            rankedByPrb = OrderedDict(sorted(rankedDict.items(), key=lambda k: k[1], reverse=True))
        else:
            rankedByPrb = OrderedDict(sorted(rankedDict.items(), key=lambda k: k[1]))
        return rankedByPrb

    def run(self,prbCrFile,prbCpFile,wd,trf,tpf,rJf,pJf,totalTestInstances,cMatrix):
        prCr=cPickle.load(open(prbCrFile,'rb'))
        prCp=cPickle.load(open(prbCpFile,'rb'))
        prCrRanked=self.RankByProbability(prCr,"DEC")
        prCpRanked=self.RankByProbability(prCp,"DEC")

        Tau_r=self.get_tauR(trf)
        docids2Annotatep2=[]
        for docID,probVal in prCrRanked.items():
            if not Tau_r==0:
                docids2Annotatep2.append(docID)
                Tau_r=Tau_r-1
        cPickle.dump(docids2Annotatep2,open(wd+'/docs4map2RRBaseline.list.'+str(totalTestInstances)+'.p', 'wb'))
        p2=phase2()
        p2.cmv=cMatrix
        p2.runphase2(prbCrFile,prbCpFile,rJf,wd,totalTestInstances,self.get_tauR(trf),BaselineType='RR')

        Tau_p=self.get_tauP(tpf)
        docids2Annotatep3=[]
        for doID,pVal in prCpRanked.items():
            if not Tau_p==0:
                docids2Annotatep3.append(doID)
                Tau_p=Tau_p-1
        cPickle.dump(docids2Annotatep3,open(wd+'/docs4map3RRBaseline.list.'+str(totalTestInstances)+'.p', 'wb'))
        p3=phase3()
        p3.cmv=cMatrix
        p3.runphase3(prbCpFile,pJf,wd,totalTestInstances,self.get_tauP(tpf),BaselineType='RR')
        c_a=self.ComputeManualAnnotationCost(self.get_tauR(trf),self.get_tauP(tpf))
        print "Annotation Cost= ",c_a
        c_m=self.ComputeMisclassificationCost(wd,rJf,pJf,totalTestInstances,cMatrix)
        print "Misclassification Cost= ",c_m
        print "RESULTVALUE ",c_m
        print "Ending Relevance Ranking Baseline Model "

    def ComputeManualAnnotationCost(self,TAUr,TAUp):
        cmobj=cm()
        lam_r=cmobj.getLam_r()
        lam_p=cmobj.getLam_p()
        return (lam_r * TAUr + lam_p * TAUp)

    def ComputeMisclassificationCost(self,wd,rJudgmentsFile,pJudgmentsFile,totalTestInstances,cMatrix):
        rJ={}
        rRJ = open(rJudgmentsFile, "r")
        rRJls=rRJ.readlines()
        rRJ.close()
        for rRJln in rRJls:
            rjFields=rRJln.strip('\n').split(" ")
            rJ[int(rjFields[0])]=int(rjFields[1])
        pJ={}
        pRJ = open(pJudgmentsFile, "r")
        pRJls=pRJ.readlines()
        pRJ.close()
        for pRJln in pRJls:
            pjFields=pRJln.strip('\n').split(" ")
            pJ[int(pjFields[0])]=int(pjFields[1])

        cP=cPickle.load(open(wd+"/RR.docid-D_P-risk.dictionary.p3."+str(totalTestInstances)+".p",'rb'))
        cL=cPickle.load(open(wd+"/RR.docid-D_L-risk.dictionary.p3."+str(totalTestInstances)+".p",'rb'))
        cW=cPickle.load(open(wd+"/RR.docid-D_W-risk.dictionary.p3."+str(totalTestInstances)+".p",'rb'))
        docids=rJ.keys()

        for docid in docids:
            if rJ[docid] == 1 and pJ[docid] == -1: # truth is Produce
                if not cP.__contains__(docid):
                    if cL.__contains__(docid):
                        self.mcDocumentMatrix[1][0]=self.mcDocumentMatrix[1][0]+1
                    if cW.__contains__(docid):
                        self.mcDocumentMatrix[2][0]=self.mcDocumentMatrix[2][0]+1
                else:
                    self.mcDocumentMatrix[0][0]=self.mcDocumentMatrix[0][0]+1
            elif rJ[docid] == 1 and pJ[docid] == 1: # truth is Log
                if not cL.__contains__(docid):
                    if cP.__contains__(docid):
                        self.mcDocumentMatrix[0][1]=self.mcDocumentMatrix[0][1]+1
                    if cW.__contains__(docid):
                        self.mcDocumentMatrix[2][1]=self.mcDocumentMatrix[2][1]+1
                else:
                    self.mcDocumentMatrix[1][1]=self.mcDocumentMatrix[1][1]+1
            elif rJ[docid] == -1: # truth is Withdraw
                if cP.__contains__(docid):
                    self.mcDocumentMatrix[0][2]=self.mcDocumentMatrix[0][2]+1
                elif cL.__contains__(docid):
                    self.mcDocumentMatrix[1][2]=self.mcDocumentMatrix[1][2]+1
                elif cW.__contains__(docid):
                    self.mcDocumentMatrix[2][2]=self.mcDocumentMatrix[2][2]+1

        print "Relevance Ranking Controlled Condition"
        print self.mcDocumentMatrix

        m_cost=0.0
        for i in range(0,3):
            for j in range(0,3):
                m_cost=m_cost+((self.mcDocumentMatrix[i][j])*cMatrix[i][j])

        return float(m_cost)

def main(argv):
    try:
        rrbaseline=RelevanceRankingBaseline()
        responsiveWD=argv[0]
        privilegeWD=argv[1]
        wd=argv[2]
        rJf=argv[3]
        pJf=argv[4]
        numTestInstances=argv[5]
        print "Starting Relevance Ranking Baseline Model "
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]),float(argv[10]),float(argv[11]))
        cMatrix.setAlpha(float(argv[12]))
        cmv=cMatrix.getCostMatrix()
        rrbaseline.run(responsiveWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',privilegeWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',wd, wd+'/tauR_value.'+str(numTestInstances)+'.p',wd+'/tauP_value.'+str(numTestInstances)+'.p',rJf,pJf, numTestInstances,cmv)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
