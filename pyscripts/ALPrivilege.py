

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

class albP:
    def runRelevanceRanking(self,prbCpFile,wdts,totalTestInstances,kctr,iterctr,wd):
        prCp=cPickle.load(open(prbCpFile,'rb'))
        #prCpRanked=self.RankByRelevance(prCp,"DEC")
        prCpRanked=self.RankByRelevance(prCp)
        docs4retrainingp3=dict(prCpRanked.items()[:kctr])
        allc=allocation()
        allc.allocateTrainids(docs4retrainingp3.keys(),iterctr,wdts+'/traininsf_docids.dat',wdts+'/p3.traininsf.almRRdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p3.traininsf.almRRdids.dat')):
            os.remove(wd+'/p3.traininsf.almRRdids.dat')
        shutil.copy(wdts+'/p3.traininsf.almRRdids.iter'+str(iterctr)+'.dat',wd+'/p3.traininsf.almRRdids.dat')

        allc.allocateTestids(docs4retrainingp3.keys(),iterctr,wdts+'/testinsf_docids_'+totalTestInstances+'.dat',wdts+'/p3.testinsf.almRRdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p3.testinsf.almRRdids.dat')):
            os.remove(wd+'/p3.testinsf.almRRdids.dat')
        shutil.copy(wdts+'/p3.testinsf.almRRdids.iter'+str(iterctr)+'.dat',wd+'/p3.testinsf.almRRdids.dat')


    def runUncertainityRanking(self,prbCpFile,wdts,totalTestInstances,kctr,iterctr,wd):
        prCp=cPickle.load(open(prbCpFile,'rb'))
        prCpRanked=self.RankByUncertainity(prCp)
        docs4retrainingp3=dict(prCpRanked.items()[:kctr])
        allc=allocation()
        allc.allocateTrainids(docs4retrainingp3.keys(),iterctr,wdts+'/traininsf_docids.dat',wdts+'/p3.traininsf.almURdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p3.traininsf.almURdids.dat')):
            os.remove(wd+'/p3.traininsf.almURdids.dat')
        shutil.copy(wdts+'/p3.traininsf.almURdids.iter'+str(iterctr)+'.dat',wd+'/p3.traininsf.almURdids.dat')

        allc.allocateTestids(docs4retrainingp3.keys(),iterctr,wdts+'/testinsf_docids_'+totalTestInstances+'.dat',wdts+'/p3.testinsf.almURdids.iter'+str(iterctr)+'.dat')
        if(os.path.exists(wd+'/p3.testinsf.almURdids.dat')):
            os.remove(wd+'/p3.testinsf.almURdids.dat')
        shutil.copy(wdts+'/p3.testinsf.almURdids.iter'+str(iterctr)+'.dat',wd+'/p3.testinsf.almURdids.dat')


    def RankByUncertainity(self,values):
        dictVal={}
        for k,v in values.iteritems():
            dictVal[k]=abs(0.5 - v[0])
        rankedByUncertainity = OrderedDict(sorted(dictVal.items(), key=lambda k: k[1]))
        return rankedByUncertainity

    def RankByRelevance(self,dictVal):
        rankedDict={}
        for key,tup in dictVal.iteritems():
            rankedDict[key]=tup[0]
        rankedByPrb = OrderedDict(sorted(rankedDict.items(), key=lambda k: k[1]))
        return rankedByPrb

def main(argv):
    try:
        activeLearningPrivilege=albP()
        privilegeWD=argv[0]
        wd=argv[1]
        wdts=argv[2]
        numTestInstances=argv[3]
        kctr=argv[4]
        iterctr=argv[5]
        activeLearningPrivilege.runUncertainityRanking(privilegeWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',wdts,numTestInstances,int(kctr),int(iterctr),wd)
        activeLearningPrivilege.runRelevanceRanking(privilegeWD+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',wdts,numTestInstances,int(kctr),int(iterctr),wd)


    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
