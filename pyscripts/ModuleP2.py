
import cPickle
from ModuleP1 import phase1
from CostMatrix import cm

class phase2:
    def __init__(self):
        self.cmv=[[0 for x in range(3)] for x in range(3)]

    def get_PrcP4d(self, Prcr4d,Prcp4d):
        v1=Prcr4d*(1.0-Prcp4d)
        v2=1.0*(1.0-Prcp4d) # if Prcr4d==1.0
        v3=0.0*(1.0-Prcp4d) # if Prcr4d==0.0
        return (v1,v2,v3)

    def get_PrcL4d(self, Prcr4d,Prcp4d):
        v1=Prcr4d*Prcp4d
        v2=1.0*Prcp4d # if Prcr4d==1.0
        v3=0.0*Prcp4d # if Prcr4d==0.0
        return (v1,v2,v3)

    def get_PrcW4d(self, Prcr4d):
        v1=1.0-Prcr4d
        v2=1.0-1.0 # if Prcr4d==1.0
        v3=1.0-0.0 # if Prcr4d==0.0
        return (v1,v2,v3)

    def get_RdcP(self,cmvalue,prcp4dVal,prcl4dVal,prcw4dVal):
        v1= ((cmvalue[0][0]* prcp4dVal[0]) + (cmvalue[0][1]*prcl4dVal[0]) +(cmvalue[0][2]*prcw4dVal[0]))
        v2= ((cmvalue[0][0]* prcp4dVal[1]) + (cmvalue[0][1]*prcl4dVal[1]) +(cmvalue[0][2]*prcw4dVal[1]))
        v3= ((cmvalue[0][0]* prcp4dVal[2]) + (cmvalue[0][1]*prcl4dVal[2]) +(cmvalue[0][2]*prcw4dVal[2]))
        return(v1,v2,v3)

    def get_RdcL(self,cmvalue,prcp4dVal,prcl4dVal,prcw4dVal):
        v1= ((cmvalue[1][0]* prcp4dVal[0]) + (cmvalue[1][1]*prcl4dVal[0]) +(cmvalue[1][2]*prcw4dVal[0]))
        v2= ((cmvalue[1][0]* prcp4dVal[1]) + (cmvalue[1][1]*prcl4dVal[1]) +(cmvalue[1][2]*prcw4dVal[1]))
        v3= ((cmvalue[1][0]* prcp4dVal[2]) + (cmvalue[1][1]*prcl4dVal[2]) +(cmvalue[1][2]*prcw4dVal[2]))
        return(v1,v2,v3)

    def get_RdcW(self,cmvalue,prcp4dVal,prcl4dVal,prcw4dVal):
        v1= ((cmvalue[2][0]* prcp4dVal[0]) + (cmvalue[2][1]*prcl4dVal[0]) +(cmvalue[2][2]*prcw4dVal[0]))
        v2= ((cmvalue[2][0]* prcp4dVal[1]) + (cmvalue[2][1]*prcl4dVal[1]) +(cmvalue[2][2]*prcw4dVal[1]))
        v3= ((cmvalue[2][0]* prcp4dVal[2]) + (cmvalue[2][1]*prcl4dVal[2]) +(cmvalue[2][2]*prcw4dVal[2]))
        return(v1,v2,v3)

    def get_minRd_cik(self,RdcPVal,RdcLVal,RdcWVal):
        v1=min(RdcPVal[0],RdcLVal[0],RdcWVal[0])
        v2=min(RdcPVal[1],RdcLVal[1],RdcWVal[1])
        v3=min(RdcPVal[2],RdcLVal[2],RdcWVal[2])
        return(v1,v2,v3)

    def get_expectationDelta(self,minRd_cikVal,respInsDPLVal):
        exp_minRd=(minRd_cikVal[1]*respInsDPLVal[0])+(minRd_cikVal[2]*(1-respInsDPLVal[0]))
        return(exp_minRd-minRd_cikVal[0])

    def computeExpectation(self,wd,totalTestInstances,cmvalue,lamR,pCrD_Filepath,pCpD_Filepath):
        self.cmv=cmvalue
        respInsDPL=cPickle.load(open(pCrD_Filepath,'rb'))
        privInsDPL=cPickle.load(open(pCpD_Filepath,'rb'))
        docIDS=respInsDPL.keys()
        prcp4d={}
        prcl4d={}
        prcw4d={}
        for docid in docIDS:
            prcp4d[docid]=self.get_PrcP4d(respInsDPL[docid][0],privInsDPL[docid][0])
            prcl4d[docid]=self.get_PrcL4d(respInsDPL[docid][0],privInsDPL[docid][0])
            prcw4d[docid]=self.get_PrcW4d(respInsDPL[docid][0])

        RdcP={}
        RdcL={}
        RdcW={}
        for docid in docIDS:
            RdcP[docid]=self.get_RdcP(cmvalue,prcp4d[docid],prcl4d[docid],prcw4d[docid])
            RdcL[docid]=self.get_RdcL(cmvalue,prcp4d[docid],prcl4d[docid],prcw4d[docid])
            RdcW[docid]=self.get_RdcW(cmvalue,prcp4d[docid],prcl4d[docid],prcw4d[docid])
        minRd_cik={}
        for docid in docIDS:
            minRd_cik[docid]=self.get_minRd_cik(RdcP[docid],RdcL[docid],RdcW[docid])
        cPickle.dump(minRd_cik,open(wd+'/minRd_cik.dictionary.p2.'+str(totalTestInstances)+'.p', 'wb'))
        expectation_Deltaord={}
        for docid in docIDS:
            expectation_Deltaord[docid]=self.get_expectationDelta(minRd_cik[docid], respInsDPL[docid])
        cPickle.dump(expectation_Deltaord,open(wd+'/expectation.deltaord.dictionary.'+str(totalTestInstances)+'.p', 'wb'))
        docids2Annotate=[]
        for docid in docIDS:
            if ((expectation_Deltaord[docid]+lamR) < 0.0): # less than or equal to
                docids2Annotate.append(docid)
        cPickle.dump(docids2Annotate,open(wd+'/docs_to_annotate_p2.list.'+str(totalTestInstances)+'.p', 'wb'))

    def runphase2(self,pCrD_Filepath,pCpD_Filepath,rJFile,wd,totalTestInstances,Tau_rValue,BaselineType=None):
        tau_r=0
        if BaselineType=='RR':
            docs2annotate=cPickle.load(open(wd+'/docs4map2RRBaseline.list.'+str(totalTestInstances)+'.p','rb'))
            rJ={}
            rRJ = open(rJFile, "r")
            rRJls=rRJ.readlines()
            rRJ.close()
            for rRJln in rRJls:
                rjFields=rRJln.strip('\n').split(" ")
                rJ[int(rjFields[0])]=int(rjFields[1])
            updtPrbcr={}
            tau_r=Tau_rValue
            for documentid in docs2annotate:
                if tau_r>0:
                    tau_r=tau_r-1
                    if rJ[documentid]==1: # Truth is Document with ID=key is responsive; annotator marks as responsive
                        updtPrbcr[documentid]=1.0
                    else:  # Truth is Document with ID=key is  not responsive
                        updtPrbcr[documentid]=0.0
            cPickle.dump(updtPrbcr,open(wd+'/RR.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p', 'wb'))
            self.reclassify(pCrD_Filepath, pCpD_Filepath,updtPrbcr,wd,totalTestInstances,BType=BaselineType)
        elif BaselineType=='UR':
            docs2annotate=cPickle.load(open(wd+'/docs4map2URBaseline.list.'+str(totalTestInstances)+'.p','rb'))
            rJ={}
            rRJ = open(rJFile, "r")
            rRJls=rRJ.readlines()
            rRJ.close()
            for rRJln in rRJls:
                rjFields=rRJln.strip('\n').split(" ")
                rJ[int(rjFields[0])]=int(rjFields[1])
            updtPrbcr={}
            tau_r=Tau_rValue
            for documentid in docs2annotate:
                if tau_r>0:
                    tau_r=tau_r-1
                    if rJ[documentid]==1: # Truth is Document with ID=key is responsive; annotator marks as responsive
                        updtPrbcr[documentid]=1.0
                    else:  # Truth is Document with ID=key is  not responsive
                        updtPrbcr[documentid]=0.0
            cPickle.dump(updtPrbcr,open(wd+'/UR.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p', 'wb'))
            self.reclassify(pCrD_Filepath, pCpD_Filepath,updtPrbcr,wd,totalTestInstances,BType=BaselineType)
        else:
            docs2annotate=cPickle.load(open(wd+'/docs_to_annotate_p2.list.'+str(totalTestInstances)+'.p','rb'))
            rJ={}
            rRJ = open(rJFile, "r")
            rRJls=rRJ.readlines()
            rRJ.close()
            for rRJln in rRJls:
                rjFields=rRJln.strip('\n').split(" ")
                rJ[int(rjFields[0])]=int(rjFields[1])
            updtPrb_cr={}
            tau_r=Tau_rValue
            for documentid in docs2annotate:
                tau_r=tau_r+1 # Responsiveness annotation counter
                if rJ[documentid]==1: # Truth is Document with ID=key is responsive; annotator marks as responsive
                    updtPrb_cr[documentid]=1.0
                else:  # Truth is Document with ID=key is  not responsive
                    updtPrb_cr[documentid]=0.0
            cPickle.dump(updtPrb_cr,open(wd+'/RM.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p', 'wb'))
            self.reclassify(pCrD_Filepath, pCpD_Filepath,updtPrb_cr,wd,totalTestInstances,BType=BaselineType)
            cPickle.dump(tau_r,open(wd+'/tauR_value.'+str(totalTestInstances)+'.p', 'wb'))
            print "Value of Tau_r = ",tau_r
            print "RESULTVALUE ",tau_r
            file = open(wd+'/tauR.'+str(totalTestInstances)+'.txt', 'w')
            file.write("TAUR="+str(tau_r))
            file.close()

    def reclassify(self,pCrD_Filepath, pCpD_Filepath,updtPrb_cr,wd,totalTestInstances,BType=None):
        """ Reclassify documents into the P, L, W classes based on the manual correction step.
        Based on Equation 8 --> re-use code in ModuleP1
        """
        p1=phase1()
        p1.classifyDocuments(wd,pCrD_Filepath, pCpD_Filepath,totalTestInstances,self.cmv,reclassify="Phase2",updatedDict=updtPrb_cr,BT=BType)







