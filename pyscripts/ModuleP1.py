
import cPickle

class phase1:
    def __init__(self):
        """
        """

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

    def classifyDocuments(self,workDir,pCrD_Filepath, pCpD_Filepath, totalTestInstances,costMatrix,reclassify=None,updatedDict=None,BT=None):
        ## EQUATION 8 ##
        respInsDPL=cPickle.load(open(pCrD_Filepath,'rb'))
        privInsDPL=cPickle.load(open(pCpD_Filepath,'rb'))

        dhrids=respInsDPL.keys()
        hrRCtr=0
        for d in dhrids:
            if respInsDPL[d][0]>0.5:
                hrRCtr=hrRCtr+1

        dhpids=privInsDPL.keys()
        hrPCtr=0
        for dp in dhpids:
            if privInsDPL[dp][0]>0.5:
                hrPCtr=hrPCtr+1


        print "Classifier Statistics: "
        print "Total #Docs that classifier h(r) classifies as Responsive = ",hrRCtr
        print "Total #Docs that classifier h(p) classifies as Privilege = ",hrPCtr


        if reclassify=="Phase2":
            for correctedDocID,probValue in updatedDict.iteritems():
                a = respInsDPL[correctedDocID]
                respInsDPL.pop(correctedDocID)
                b = list(a)
                b[0] = probValue
                a = tuple(b)
                respInsDPL[correctedDocID]=a


        if reclassify=="Phase3":
            if BT=='RR':
                updatedDictP2=cPickle.load(open(workDir+'/RR.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p','rb'))
                for correctedDocID,probValue in updatedDictP2.iteritems():
                    a = respInsDPL[correctedDocID]
                    respInsDPL.pop(correctedDocID)
                    b = list(a)
                    b[0] = probValue
                    a = tuple(b)
                    respInsDPL[correctedDocID]=a
            elif BT=='UR':
                updatedDictP2=cPickle.load(open(workDir+'/UR.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p','rb'))
                for correctedDocID,probValue in updatedDictP2.iteritems():
                    a = respInsDPL[correctedDocID]
                    respInsDPL.pop(correctedDocID)
                    b = list(a)
                    b[0] = probValue
                    a = tuple(b)
                    respInsDPL[correctedDocID]=a
            else:
                updatedDictP2=cPickle.load(open(workDir+'/RM.updtPrbDocuments.p2.'+str(totalTestInstances)+'.p','rb'))
                for correctedDocID,probValue in updatedDictP2.iteritems():
                    a = respInsDPL[correctedDocID]
                    respInsDPL.pop(correctedDocID)
                    b = list(a)
                    b[0] = probValue
                    a = tuple(b)
                    respInsDPL[correctedDocID]=a

            for correctedDocID,probValue in updatedDict.iteritems():
                a = privInsDPL[correctedDocID]
                privInsDPL.pop(correctedDocID)
                b = list(a)
                b[0] = probValue
                a = tuple(b)
                privInsDPL[correctedDocID]=a

        pdP={}
        pdL={}
        pdW={}
        docIDS=respInsDPL.keys()

        for docid in docIDS:
            cPVal=self.getProbaility_cP(respInsDPL[docid],privInsDPL[docid])
            cLVal=self.getProbaility_cL(respInsDPL[docid],privInsDPL[docid])
            cWVal=self.getProbaility_cW(respInsDPL[docid],privInsDPL[docid])
            pdP[docid]=cPVal
            pdL[docid]=cLVal
            pdW[docid]=cWVal

        if reclassify=="Phase2" and BT==None:
            cPickle.dump(respInsDPL,open(workDir+'/rAnnotated-ds-op-label.tuple.dictionary.p2.'+str(totalTestInstances)+'.p', "wb"))
            cPickle.dump(pdP,open(workDir+"/docid-cP-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/docid-cL-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/docid-cW-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
        elif reclassify=="Phase2" and BT=="RR":
            cPickle.dump(respInsDPL,open(workDir+'/RR-rAnnotated-ds-op-label.tuple.dictionary.p2.'+str(totalTestInstances)+'.p', "wb"))
            cPickle.dump(pdP,open(workDir+"/RR-docid-cP-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/RR-docid-cL-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/RR-docid-cW-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
        elif reclassify=="Phase2" and BT=="UR":
            cPickle.dump(respInsDPL,open(workDir+'/UR-rAnnotated-ds-op-label.tuple.dictionary.p2.'+str(totalTestInstances)+'.p', "wb"))
            cPickle.dump(pdP,open(workDir+"/UR-docid-cP-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/UR-docid-cL-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/UR-docid-cW-probValue.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
        elif reclassify=="Phase3" and BT==None:
            cPickle.dump(pdP,open(workDir+"/docid-cP-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/docid-cL-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/docid-cW-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
        elif reclassify=="Phase3" and BT=='RR':
            cPickle.dump(pdP,open(workDir+"/RR-docid-cP-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/RR-docid-cL-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/RR-docid-cW-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
        elif reclassify=="Phase3" and BT=='UR':
            cPickle.dump(pdP,open(workDir+"/UR-docid-cP-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/UR-docid-cL-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/UR-docid-cW-probValue.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
        else:
            cPickle.dump(pdP,open(workDir+"/docid-cP-probValue.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdL,open(workDir+"/docid-cL-probValue.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(pdW,open(workDir+"/docid-cW-probValue.dictionary."+str(totalTestInstances)+".p", "wb"))

        class_D_P={}
        class_D_L={}
        class_D_W={}

        R1dcP={}
        R1dcL={}
        R1dcW={}
        #(Summation [j in P,W,L ] lamda(ij) * Probability(c_j|d))
        for did in docIDS:
            hP_did=0.0
            hL_did=0.0
            hW_did=0.0
            i=0# i=0 ==> Predicted as Produce
            for j in range(0,3): #0==>P, 1==>L, 2==>W TRUTH
                if j==0:
                    hP_did=hP_did+costMatrix[i][j]* pdP[did]
                elif j==1:
                    hP_did=hP_did+costMatrix[i][j]* pdL[did]
                else:
                    hP_did=hP_did+costMatrix[i][j]* pdW[did]
                R1dcP[did]=hP_did
            i=1 # i=1 ==> Predicted as Logged
            for j in range(0,3): #0==>P, 1==>L, 2==>W  TRUTH
                if j==0:
                    hL_did=hL_did+costMatrix[i][j]* pdP[did]
                elif j==1:
                    hL_did=hL_did+costMatrix[i][j]* pdL[did]
                else:
                    hL_did=hL_did+costMatrix[i][j]* pdW[did]
                R1dcL[did]=hL_did
            i=2 # i=2 ==> Predicted as Withheld
            for j in range(0,3): #0==>P, 1==>L, 2==>W TRUTH
                if j==0:
                    hW_did=hW_did+costMatrix[i][j]* pdP[did]
                elif j==1:
                    hW_did=hW_did+costMatrix[i][j]* pdL[did]
                else:
                    hW_did=hW_did+costMatrix[i][j]* pdW[did]
                R1dcW[did]=hW_did
            #argmin of the previous step


            frMC=min(hP_did,hL_did,hW_did)
            if frMC==hP_did:
                class_D_P[did]=hP_did
            elif frMC==hL_did:
                class_D_L[did]=hL_did
            else:
                class_D_W[did]=hW_did


        if reclassify=="Phase2" and BT==None:
            cPickle.dump(R1dcP,open(workDir+"/R1dcP-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcL,open(workDir+"/R1dcL-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcW,open(workDir+"/R1dcW-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_P,open(workDir+"/docid-D_P-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/docid-D_L-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/docid-D_W-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 2:"
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        elif reclassify=="Phase2" and BT=='RR':
            cPickle.dump(class_D_P,open(workDir+"/RR.docid-D_P-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/RR.docid-D_L-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/RR.docid-D_W-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 2 RR Model:"
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        elif reclassify=="Phase2" and BT=='UR':
            cPickle.dump(class_D_P,open(workDir+"/UR.docid-D_P-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/UR.docid-D_L-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/UR.docid-D_W-risk.dictionary.p2."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 2 UR Model:"
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        elif reclassify=="Phase3" and BT==None:
            cPickle.dump(R1dcP,open(workDir+"/R1dcP-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcL,open(workDir+"/R1dcL-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcW,open(workDir+"/R1dcW-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_P,open(workDir+"/docid-D_P-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/docid-D_L-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/docid-D_W-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 3: "
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        elif reclassify=="Phase3" and BT=='RR':
            cPickle.dump(class_D_P,open(workDir+"/RR.docid-D_P-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/RR.docid-D_L-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/RR.docid-D_W-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 3 RR Model:"
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        elif reclassify=="Phase3" and BT=='UR':
            cPickle.dump(class_D_P,open(workDir+"/UR.docid-D_P-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/UR.docid-D_L-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/UR.docid-D_W-risk.dictionary.p3."+str(totalTestInstances)+".p", "wb"))
            print "In Phase 3 UR Model:"
            print "Total number of Documents to be Produced: ",len(class_D_P)
            print "Total number of Documents to be Logged: ",len(class_D_L)
            print "Total number of Documents to be Withdrawn: ",len(class_D_W)
        else:
            cPickle.dump(R1dcP,open(workDir+"/R1dcP-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcL,open(workDir+"/R1dcL-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(R1dcW,open(workDir+"/R1dcW-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_P,open(workDir+"/docid-D_P-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_L,open(workDir+"/docid-D_L-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            cPickle.dump(class_D_W,open(workDir+"/docid-D_W-risk.dictionary."+str(totalTestInstances)+".p", "wb"))
            print "In initial Classification Step:"
            print "Total number of Documents to be Produced:",len(class_D_P)
            print "Total number of Documents to be Logged:",len(class_D_L)
            print "Total number of Documents to be Withdrawn:",len(class_D_W)

