
import sys

class cm:
    def __init__(self):
        self.lam_r=1.0 # this is the cost value for Lambda_r
        self.lam_p=5.0 # this is the cost value for Lambda_p
        self.costMatrix=[[0 for x in range(3)] for x in range(3)]

    def setCostMatrix(self,cm01,cm02,cm10,cm12,cm20,cm21):
        self.costMatrix[0][0] = 0   # this is the cost value for lamda(PP) user input
        self.costMatrix[0][1] = cm01  # this is the cost value for lamda(PL) user input
        self.costMatrix[0][2] = cm02  # this is the cost value for lamda(PW) user input
        self.costMatrix[1][0] = cm10 # this is the cost value for lamda(LP) user input
        self.costMatrix[1][1] = 0    # this is the cost value for lamda(LL) user input
        self.costMatrix[1][2] = cm12  # this is the cost value for lamda(LW) user input
        self.costMatrix[2][0] = cm20  # this is the cost value for lamda(WP) user input
        self.costMatrix[2][1] = cm21  # this is the cost value for lamda(WL) user input
        self.costMatrix[2][2] = 0 # this is the cost value for lamda(WW) user input

    def setAlpha(self, alpha):
        if not float(alpha)==1.0:
            for i in range(0,3):
                for j in range(0,3):
                    self.costMatrix[i][j]= float(alpha) * self.costMatrix[i][j]

    def getCellValue(self,row,column):
        return self.costMatrix[row][column]

    def getCostMatrix(self):
        return self.costMatrix

    def getLam_r(self):
        return self.lam_r

    def getLam_p(self):
        return self.lam_p

def main(argv):
    try:
        cmat=cm()
        cmat.setCostMatrix(float(argv[0]),float(argv[1]),float(argv[2]),float(argv[3]),float(argv[4]),float(argv[5]))
        cmat.setAlpha(argv[6])
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])

    