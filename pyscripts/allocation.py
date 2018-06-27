import cPickle
import sys

class Allocate:
    def __init__(self):
        self.trainsetids=set()
        self.testsetids=set()
        self.Identifiers={} # key=Linenumber , value=Docid
        self.featureLabData={} #key=Docid, value = feature and content

    def readCatfile(self,combinedCatFilePath,dumpPath):
        f=open(combinedCatFilePath,'r')
        fDat = f.readlines()
        f.close()
        for catFileline in fDat:
            cflsplit = catFileline.split(" ",1)
            fcounter=int(cflsplit[0])
            cfl=cflsplit[1]
            self.featureLabData[fcounter]=cfl
        dumpOut = open(dumpPath, 'w')
        cPickle.dump(self.featureLabData, dumpOut)
        dumpOut.close()


    def allocateTrain(self,CatPickleFilePath,trainFilePath,tIdsf):
        fcatdat=cPickle.load(open(CatPickleFilePath,'rb'))
        f=open(tIdsf,'r')
        fDat = f.readlines()
        f.close()
        trainIDS=set()
        for fD in fDat:
            ids=int(fD.strip('\n'))
            trainIDS.add(ids)
        writeBuffer = open(trainFilePath,'a')
        for tid in trainIDS:
            if tid:
                writeBuffer.write(fcatdat[tid])
        f.close()


    def allocateTest(self,CatPickleFilePath,testFilePath,testIdsf,testInsCount):
        fcatdatTest=cPickle.load(open(CatPickleFilePath,'rb'))
        ftest=open(testIdsf,'r')
        fDatTest = ftest.readlines()
        ftest.close()
        testIDS=set()
        for fD in fDatTest:
            ids=int(fD.strip('\n'))
            testIDS.add(ids)
        writeBuffer = open(testFilePath,'a')
        for tid in testIDS:
            if tid:
                writeBuffer.write(fcatdatTest[tid])
        ftest.close()


def main(argv):
    try:
        allc=Allocate()
        skip=argv[0]
        if(skip=="true"):
            allc.allocateTrain(argv[2],argv[5],argv[3])
            allc.allocateTest(argv[2],argv[6],argv[4],argv[7])
        else:
            allc.readCatfile(argv[1], argv[2])
            allc.allocateTrain(argv[2],argv[5],argv[3])
            allc.allocateTest(argv[2],argv[6],argv[4],argv[7])
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
