

import sys
import pandas as pd

class writer:
    def write(self,inputfilepath):
        with open(inputfilepath) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip().split(' ') for x in content]

        taur=float(content[0][2])
        taup=float(content[1][2])
        AnnotationCost=float(content[2][2])
        hymisscost=float(content[3][2])
        hytotal=AnnotationCost+hymisscost

        FullyAutomated=float(content[4][2])
        FAD=((FullyAutomated-hytotal)/hytotal)

        FullyManual=float(content[5][2])
        FMD=((FullyManual-hytotal)/hytotal)

        RRmisscost=float(content[6][2])
        RRTotal=AnnotationCost+RRmisscost
        RRD= ((RRTotal-hytotal)/hytotal)

        URmisscost=float(content[7][2])
        URTotal=AnnotationCost+URmisscost
        URD= ((URTotal-hytotal)/hytotal)

        ALRRmisscost=float(content[8][2])
        ALRRTotal=AnnotationCost+ALRRmisscost
        ALRRD= ((ALRRTotal-hytotal)/hytotal)

        ALURmisscost=float(content[9][2])
        ALURTotal=AnnotationCost+ALURmisscost
        ALURD= ((ALURTotal-hytotal)/hytotal)


        print taur,taup,FullyAutomated,FAD, FullyManual, FMD,AnnotationCost,URmisscost,URTotal,URD,AnnotationCost,RRmisscost,RRTotal,RRD,AnnotationCost,ALURmisscost,ALURTotal,ALURD, AnnotationCost,ALRRmisscost,ALRRTotal,ALRRD,AnnotationCost,hymisscost,hytotal


def main(argv):
    try:
        w=writer()
        w.write('Path/to/result/csv')
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
    