

import math
import cPickle
import sys

class Probabilities:
    def __init__(self):
        self.platt_params={}
        self.platt_params['GCAT']=(-3.4691414065263144,-0.13719639846313605)
        self.platt_params['CCAT']=(-3.0399279961917069,-0.13586854190852918)
        self.platt_params['MCAT']=(-3.4346707380440957,0.0056597239972020772)
        self.platt_params['GPOL']=(-3.3043099615863412,-0.023626049322927944)
        self.platt_params['GDIP']=(-3.7001228975833436,-0.06519881163203084)
        self.platt_params['ECAT']=(-3.0729808755097685,-0.16442790802646404)
        self.platt_params['M13']=(-3.8325713412889395,-0.0198909993191753)
        self.platt_params['E12']=(-4.0650833134760278,-0.68633035218266303)
        self.platt_params['GVIO']=(-3.792051111206038,0.037297997500889336)
        self.platt_params['C17']=(-4.1422811621308417,-0.59600893407513644)
        self.platt_params['C31']=(-3.7523624639979469,-0.77411204282009238)
        self.platt_params['C13']=(-4.0478070495611913,-0.95133693130283092)
        self.platt_params['M11']=(-4.2453880637618298,-0.23487307737447896)
        self.platt_params['M14']=(-4.0711395474374372,0.072713663644137963)
        self.platt_params['M141']=(-4.2819013713441745,0.46419151202184461)
        self.platt_params['E21']=(-4.0303754539482428,-0.41725097485305851)
        self.platt_params['C152']=(-3.5812800253559005,-0.38828577590501823)
        self.platt_params['C181']=(-3.9205275336188268,-0.32342386521600891)
        self.platt_params['M132']=(-4.2759711193437768,-0.17859977377460073)
        self.platt_params['C18']=(-4.0180414781638181,-0.39948084024543939)
        self.platt_params['C15']=(-3.5121899398954364,-0.30740639362988215)
        self.platt_params['M12']=(-4.0862239526504904,-0.043465232629513365)
        self.platt_params['GCRIM']=(-4.1594260006754418,-0.27437033886168316)
        self.platt_params['C24']=(-3.7947991655166629,-0.5123728243082516)
        self.platt_params['C21']=(-3.853826102287643,-0.53258391016398399)
        self.platt_params['E212']=(-4.9044046013016835,-0.84560247501774777)
        self.platt_params['C151']=(-3.8138461661499119,-0.3590765556830498)
        self.platt_params['M131']=(-3.892102006681772,0.047270358101764706)


    def getCaliberatedProbabilities(self,workDir,testSetSize,category,jcmtswd,tDfilepath,tLfilepath,itrctr):
        tInsDPL={}
        testInsProbabilities={}
        paramFields=self.platt_params[category]
        paramA=float(paramFields[0])
        paramB=float(paramFields[1])

        f = open(tDfilepath, 'r')
        lines=f.read().splitlines()
        f.close()

        tdocids=open(jcmtswd, 'r')
        tdocidlines=tdocids.read().splitlines()
        tdocids.close()

        predictions=[float(i) for i in lines]
        documentIDS=[int(i) for i in tdocidlines]

        testInsScores=dict(zip(documentIDS, predictions))


        for k,v in testInsScores.iteritems():
            plattProbability=(float(1.0)/float(1.0 + math.exp((v*paramA)+paramB)))
            testInsProbabilities[k]=plattProbability

        for k,v in testInsProbabilities.iteritems():
            dplTuple=(float(v),float(testInsScores[k]))
            tInsDPL[k]=dplTuple

        # trainSetDocSize=23149
        size=(23149+(10*itrctr))

        if itrctr>0:
            if testSetSize==size:
                cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".iter"+str(itrctr)+".p", "wb"))
            else:
                cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".iter"+str(itrctr)+".p", "wb"))
        else:
            if testSetSize==23149:
                cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".p", "wb"))
            else:
                cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary."+str(testSetSize)+".p", "wb"))

def main(argv):
    try:
        caliberatedProbabilities=Probabilities()
        # argv[0] = Path of Working Directory
        # argv[1] = Platt PARAMETERS
        # argv[2] = Prediction file path ; 
        # argv[3]= Truth Labels file path; 
        # argv[4] = No. of files in test-set
        # argv[5] = boolean value ; CV true or false
        # argv[6] = iteration counter non-zero number in case of ALB
        tup=caliberatedProbabilities.getCaliberatedProbabilities(argv[0],argv[5],argv[1],argv[2],argv[3],argv[4],int(argv[6]))
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
    