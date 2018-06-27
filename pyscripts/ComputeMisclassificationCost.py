
import sys
from CostMatrix import cm
import cPickle

class computeCm:
    def __init__(self):
        self.mcDocumentMatrix=[[0 for x in range(3)] for x in range(3)]
        self.relMat=[[0 for x in range(2)] for x in range(2)]
        self.priMat=[[0 for x in range(2)] for x in range(2)]
        self.mcAnnotationMatrix=[[0 for x in range(3)] for x in range(3)]
        self.relAnnotationMatrix=[[0 for x in range(2)] for x in range(2)]
        self.priAnnotationMatrix=[[0 for x in range(2)] for x in range(2)]

    def getProbaility_cP(self,rTup,pTup):
        """
        cP is the class of the responsive non-privileged documents, that should be Produced
        to the requesting party
        """
        return float(rTup[0] * (1.0 - pTup[0]))


    def getProbaility_cL(self,rTup,pTup):
        """
        cL is the class of the responsive privileged documents, that should be logged into the
        privilege Log
        """
        return float(rTup[0] * pTup[0])

    def getProbaility_cW(self,rTup,pTup):
        """
        cW is the class of the non-responsive documents, that should be Withheld by the producing party
        """
        return float((1.0-rTup[0]))

    def compute(self,mcdm,cm):
        m_cost=0.0
        for i in range(0,3):
            for j in range(0,3):
                m_cost=m_cost+((mcdm[i][j])*cm[i][j])
        return float(m_cost)

    def set_relAnnotationMatrix(self,relAMat):
        self.relAnnotationMatrix=cPickle.load(open(relAMat,'rb'))

    def set_priAnnotationMatrix(self,priAMat):
        self.priAnnotationMatrix=cPickle.load(open(priAMat,'rb'))

    def get_mcDocumentMatrix(self,kfoldCVtrainDatProbabilities,TrainIDSFile,rTrainLabelsFile,kfoldCVtrainDatpProbabilities, pTrainLabelsFile,cMatrix):
        with open(TrainIDSFile) as f:
            tids = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        IDS = [int(x.strip()) for x in tids]

        with open(rTrainLabelsFile) as fl:
            tlables = fl.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        tlabs = [int(x.strip()) for x in tlables]

        relTrainJ = dict(zip(IDS, tlables))

        relprobs=cPickle.load(open(kfoldCVtrainDatProbabilities,'rb'))
        priprobs=cPickle.load(open(kfoldCVtrainDatpProbabilities,'rb'))

        with open(pTrainLabelsFile) as fpl:
            plabs=fpl.readlines()
        pLAB=[int(x.strip()) for x in plabs]

        priTrainJ=dict(zip(IDS, pLAB))

        pdP={}
        pdL={}
        pdW={}
        DOCIDS=relTrainJ.keys()
        for docid in DOCIDS:
            cPVal=self.getProbaility_cP(relprobs[docid],priprobs[docid])
            cLVal=self.getProbaility_cL(relprobs[docid],priprobs[docid])
            cWVal=self.getProbaility_cW(relprobs[docid],priprobs[docid])
            pdP[docid]=cPVal
            pdL[docid]=cLVal
            pdW[docid]=cWVal

        class_D_P={}
        class_D_L={}
        class_D_W={}
        #(Summation [i,j in P,W,L ] lamda(ij) * Probability(c_j|d))
        for did in DOCIDS:
            hP_did=0.0
            hL_did=0.0
            hW_did=0.0
            i=0# i=0 ==> Predicted as Produce
            for j in range(0,3): #0==>P, 1==>L, 2==>W TRUTH
                if j==0:
                    hP_did=hP_did+cMatrix[i][j]* pdP[did]
                elif j==1:
                    hP_did=hP_did+cMatrix[i][j]* pdL[did]
                else:
                    hP_did=hP_did+cMatrix[i][j]* pdW[did]
            i=1 # i=1 ==> Predicted as Logged
            for j in range(0,3): #0==>P, 1==>L, 2==>W  TRUTH
                if j==0:
                    hL_did=hL_did+cMatrix[i][j]* pdP[did]
                elif j==1:
                    hL_did=hL_did+cMatrix[i][j]* pdL[did]
                else:
                    hL_did=hL_did+cMatrix[i][j]* pdW[did]
            i=2 # i=2 ==> Predicted as Withheld
            for j in range(0,3): #0==>P, 1==>L, 2==>W TRUTH
                if j==0:
                    hW_did=hW_did+cMatrix[i][j]* pdP[did]
                elif j==1:
                    hW_did=hW_did+cMatrix[i][j]* pdL[did]
                else:
                    hW_did=hW_did+cMatrix[i][j]* pdW[did]
            #argmin of the previous step
            frMC=min(hP_did,hL_did,hW_did)
            if frMC==hP_did:
                class_D_P[did]=hP_did
            elif frMC==hL_did:
                class_D_L[did]=hL_did
            else:
                class_D_W[did]=hW_did


        for rkey,rvalue in relTrainJ.iteritems():
            if rvalue==1 and priTrainJ[rkey]==-1: #TRUTH is Produce
                if class_D_P.__contains__(rkey):
                    self.mcDocumentMatrix[0][0]=(self.mcDocumentMatrix[0][0]+1)
                elif class_D_L.__contains__(rkey):
                    self.mcDocumentMatrix[1][0]=(self.mcDocumentMatrix[1][0]+1)
                elif class_D_W.__contains__(rkey):
                    self.mcDocumentMatrix[2][0]=(self.mcDocumentMatrix[2][0]+1)

            if rvalue==1 and priTrainJ[rkey]==1: #TRUTH is Log
                if class_D_P.__contains__(rkey):
                    self.mcDocumentMatrix[0][1]=(self.mcDocumentMatrix[0][1]+1)
                elif class_D_L.__contains__(rkey):
                    self.mcDocumentMatrix[1][1]=(self.mcDocumentMatrix[1][1]+1)
                elif class_D_W.__contains__(rkey):
                    self.mcDocumentMatrix[2][1]=(self.mcDocumentMatrix[2][1]+1)

            if rvalue==-1: #TRUTH is Withdraw
                if class_D_P.__contains__(rkey):
                    self.mcDocumentMatrix[0][2]=(self.mcDocumentMatrix[0][2]+1)
                elif class_D_L.__contains__(rkey):
                    self.mcDocumentMatrix[1][2]=(self.mcDocumentMatrix[1][2]+1)
                elif class_D_W.__contains__(rkey):
                    self.mcDocumentMatrix[2][2]=(self.mcDocumentMatrix[2][2]+1)

    def get_finalDocMatrix(self,estimation_factor):
        sum=0.0
        for i in range(0,3):
            for j in range(0,3):
                self.mcDocumentMatrix[i][j]=estimation_factor*self.mcDocumentMatrix[i][j]
                sum=self.mcDocumentMatrix[i][j] + sum
        print "Final Document matrix = ",self.mcDocumentMatrix
        print " Sum = ",sum
        return self.mcDocumentMatrix


def main(argv):
    try:
        workDirResponsive=argv[0]
        workDirPrivilege=argv[1]
        numTestInstances=argv[2]
        numTrainInstances=argv[3]
        estimation_factor=float(numTestInstances)/float(numTrainInstances)
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[4]),float(argv[5]),float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]))
        cMatrix.setAlpha(float(argv[10]))
        cmv=cMatrix.getCostMatrix()
        ccm=computeCm()


        ccm.get_mcDocumentMatrix(workDirResponsive+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTrainInstances)+'.p',workDirResponsive+'/trainf.count.lables.dat',workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTrainInstances)+'.p',workDirPrivilege+'/trainf.count.lables.dat',cmv)
        dMatrix=ccm.get_finalDocMatrix(estimation_factor)
        Misclassification_cost = ccm.compute(dMatrix,cmv)
        print "The misclassification cost is: ", Misclassification_cost
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])