
import sys
import cPickle
import shutil
import os
from collections import OrderedDict

class allocation:
    def allocateTrainids(self,docs4retraining,itercount,filepath,wdtsfp):
        f=open(filepath,'r')
        fDat = f.readlines()
        f.close()
        trainIDS=set()
        for fD in fDat:
            ids=int(fD.strip('\n'))
            trainIDS.add(ids)
        for i in docs4retraining:
            trainIDS.add(i)
        writeBuffer = open(wdtsfp,'a')
        for tid in trainIDS:
            writeBuffer.write("%s\n" % tid)
        writeBuffer.close()


    def allocateTestids(self,docs4retraining,itercount,filepath,wdtsfp):
        f=open(filepath,'r')
        fDat = f.readlines()
        f.close()
        testIDs=set()
        for fD in fDat:
            ids=int(fD.strip('\n'))
            testIDs.add(ids)
        for i in docs4retraining:
            if i in testIDs:
                testIDs.remove(i)
        writeBuffer = open(wdtsfp,'a')

        for tid in testIDs:
            writeBuffer.write("%s\n" % tid)
        writeBuffer.close()

class albR:
    def runRelevanceRanking(self,prbCrFile,wdts,totalTestInstances,kctr,iterctr,wd):
        prCr=cPickle.load(open(prbCrFile,'rb'))
        prCrRanked=self.RankByRelevance(prCr,"DEC")
        docs4retrainingp2=dict(prCrRanked.items()[:kctr])
        allc=allocation()
        allc.allocateTrainids(docs4retrainingp2.keys(),iterctr,wdts+'/traininsf_docids.dat',wdts+'/p2.traininsf.almRRdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p2.traininsf.almRRdids.dat')):
            os.remove(wd+'/p2.traininsf.almRRdids.dat')
        shutil.copy(wdts+'/p2.traininsf.almRRdids.iter'+str(iterctr)+'.dat',wd+'/p2.traininsf.almRRdids.dat')

        allc.allocateTestids(docs4retrainingp2.keys(),iterctr,wdts+'/testinsf_docids_'+totalTestInstances+'.dat',wdts+'/p2.testinsf.almRRdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p2.testinsf.almRRdids.dat')):
            os.remove(wd+'/p2.testinsf.almRRdids.dat')
        shutil.copy(wdts+'/p2.testinsf.almRRdids.iter'+str(iterctr)+'.dat',wd+'/p2.testinsf.almRRdids.dat')


    def runUncertainityRanking(self,prbCrFile,wdts,totalTestInstances,kctr,iterctr,wd):
        prCr=cPickle.load(open(prbCrFile,'rb'))
        prCrRanked=self.RankByUncertainity(prCr)
        docs4retrainingp2=dict(prCrRanked.items()[:kctr])

        allc=allocation()
        allc.allocateTrainids(docs4retrainingp2.keys(),iterctr,wdts+'/traininsf_docids.dat',wdts+'/p2.traininsf.almURdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p2.traininsf.almURdids.dat')):
            os.remove(wd+'/p2.traininsf.almURdids.dat')
        shutil.copy(wdts+'/p2.traininsf.almURdids.iter'+str(iterctr)+'.dat',wd+'/p2.traininsf.almURdids.dat')

        allc.allocateTestids(docs4retrainingp2.keys(),iterctr,wdts+'/testinsf_docids_'+totalTestInstances+'.dat',wdts+'/p2.testinsf.almURdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p2.testinsf.almURdids.dat')):
            os.remove(wd+'/p2.testinsf.almURdids.dat')
        shutil.copy(wdts+'/p2.testinsf.almURdids.iter'+str(iterctr)+'.dat',wd+'/p2.testinsf.almURdids.dat')

    def RankByUncertainity(self,values):
        dictVal={}
        for k,v in values.iteritems():
            dictVal[k]=abs(0.5 - v[0])
        rankedByUncertainity = OrderedDict(sorted(dictVal.items(), key=lambda k: k[1]))
        return rankedByUncertainity

    def RankByRelevance(self,dictVal,order):
        rankedDict={}
        for key,tup in dictVal.iteritems():
            rankedDict[key]=tup[0]
        if order=="DEC":
            rankedByPrb = OrderedDict(sorted(rankedDict.items(), key=lambda k: k[1], reverse=True))
        else:
            rankedByPrb = OrderedDict(sorted(rankedDict.items(), key=lambda k: k[1]))
        return rankedByPrb

def main(argv):
    try:
        activeLearningRelevance=albR()
        responsiveWD=argv[0]
        wd=argv[1]
        wdts=argv[2]
        numTestInstances=argv[3]
        kctr=argv[4]
        iterctr=argv[5]
        activeLearningRelevance.runUncertainityRanking(responsiveWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',wdts,numTestInstances,int(kctr),int(iterctr),wd)
        activeLearningRelevance.runRelevanceRanking(responsiveWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',wdts,numTestInstances,int(kctr),int(iterctr),wd)
    except:
        raise


if __name__ == "__main__":
    main(sys.argv[1:])