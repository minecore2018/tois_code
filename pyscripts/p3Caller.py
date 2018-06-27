
from ModuleP3 import phase3
import sys
from CostMatrix import cm


def main(argv):
    try:
        p3=phase3()
        wd=argv[0] # Joint Cost Model's Working Directory (Resp and Priv Category )
        workDirResponsive=argv[1] # Responsive Category Working Directory'
        workDirPrivilege=argv[2] # Privilege Category Working Directory'
        numTestInstances=argv[3]
        pJFile=argv[4]
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[5]),float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]),float(argv[10]))
        cMatrix.setAlpha(float(argv[11]))
        cmv=cMatrix.getCostMatrix()
        lamP=cMatrix.getLam_p()
        p3.computeExpectation(wd,numTestInstances,cmv,lamP,workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p')
        p3.runphase3(workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',pJFile,wd,numTestInstances,0)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])