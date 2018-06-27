
from ModuleP2 import phase2
import sys
from CostMatrix import cm


def main(argv):
    try:
        p2=phase2()
        wd= argv[0] # Joint Cost Model's Working Directory (Resp and Priv Category )
        workDirResponsive=argv[1] # Responsive Category Working Directory '
        workDirPrivilege=argv[2] # Privilege Category Working Directory '
        numTestInstances=argv[3] 
        rJFile=argv[4]
        cMatrix=cm()
        cMatrix.setCostMatrix(float(argv[5]),float(argv[6]),float(argv[7]),float(argv[8]),float(argv[9]),float(argv[10]))
        cMatrix.setAlpha(float(argv[11]))
        cmv=cMatrix.getCostMatrix()
        lamR=cMatrix.getLam_r()
        p2.computeExpectation(wd,numTestInstances,cmv,lamR,workDirResponsive+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p')
        tau_rValue=p2.runphase2(workDirResponsive+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary.'+str(numTestInstances)+'.p',rJFile,wd,numTestInstances,0)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])