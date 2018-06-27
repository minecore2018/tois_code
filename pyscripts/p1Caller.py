
from ModuleP1 import phase1
import sys
from CostMatrix import cm


def main(argv):
    try:
        p1=phase1()
        wDir= argv[0] 
        workDirResponsive=argv[1] 
        workDirPrivilege=argv[2]  
        numTestInstances=argv[3]  
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[4]),float(argv[5]),float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]))
        cMatrix.setAlpha(float(argv[10]))
        cmv=cMatrix.getCostMatrix()
        p1.classifyDocuments(wDir,workDirResponsive+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',numTestInstances,cmv,reclassify=False)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])