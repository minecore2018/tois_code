#!/bin/bash

# For each category First create the featureFile and fileID pickles saperately.
# This is done prior for optimizing the speed.

lamPL=$1
lamPW=$2
lamLP=$3
lamLW=$4
lamWP=$5
lamWL=$6
testsetSize=$7
runID=$8
iterationCtr=$9
trainsetSize=${10}
pC=${11}

isRR=true
isUR=false

cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/jcm-$testsetSize
oldwd=$(pwd)
cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
if [ ! -d "alwdir" ]; then
  mkdir alwdir
fi
cd alwdir

declare -a catArr=($pC)

dfp=../rootdirpath/Research/jvdofs/mfpadat
rundir=../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir
for rCategory in "${catArr[@]}"
do
  wdcat=../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir
  if [ "$isRR" = true ] ; then
    if [ ! -d RRalb ]; then
      mkdir RRalb
    fi
    cd RRalb
    if [ ! -d $rCategory ]; then
      mkdir $rCategory
    fi
    cd $rCategory
    if [ ! -d "jcm-"$testsetSize ]; then
      mkdir jcm-$testsetSize
    fi
    if [ ! -d "logfiles" ]; then
      mkdir logfiles
    fi
    cd jcm-$testsetSize
    alwdnew=$(pwd)
    #Get all the iteration files
    mv $oldwd/p3.traininsf.almRRdids.iter$iterationCtr.dat $alwdnew/.
    mv $oldwd/p3.testinsf.almRRdids.iter$iterationCtr.dat $alwdnew/.
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/allocation.py true ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory/combined.$rCategory.datafile.temp.dat ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory/pickleFiles/combined.$rCategory.fdat.p $alwdnew/p3.traininsf.almRRdids.iter$iterationCtr.dat $alwdnew/p3.testinsf.almRRdids.iter$iterationCtr.dat  $alwdnew/trainfile.iter$iterationCtr.dat  $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat $testsetSize
    cut -d' ' -f1 $alwdnew/trainfile.iter$iterationCtr.dat  >> $alwdnew/trainf.count.lables.iter$iterationCtr.dat
    cut -d' ' -f1 $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat  >> $alwdnew/testinsf.$testsetSize.count.lables.iter$iterationCtr.dat
    cd ../rootdirpath/Research/svm_light
    ./svm_learn -v 3 $alwdnew/trainfile.iter$iterationCtr.dat $alwdnew/model.trainCount.$testsetSize.dat >> ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir/RRalb/$rCategory/logfiles/svm.finaltrain.$testsetSize.log 2>&1
    ./svm_classify $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat $alwdnew/model.trainCount.$testsetSize.dat $alwdnew/test.prediction.iter$iterationCtr.tCount.$testsetSize.dat >> ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir/RRalb/$rCategory/logfiles/svm.finaltest.$testsetSize.log
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wdcat $rCategory $alwdnew/p3.testinsf.almRRdids.iter$iterationCtr.dat $alwdnew/test.prediction.iter$iterationCtr.tCount.$testsetSize.dat $alwdnew/testinsf.$testsetSize.count.lables.iter$iterationCtr.dat $testsetSize $iterationCtr
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wdcat $rCategory $alwdnew/p3.traininsf.almRRdids.iter$iterationCtr.dat $wdcat/predictions/train/predictions4Platt.781265.dat $alwdnew/trainf.count.lables.iter$iterationCtr.dat $trainsetSize $iterationCtr
    # echo "STATUS: Completed Caliberating Probabilities"
    if [ -f $rundir/ds-op-label.tuple.dictionary.$testsetSize.RRalb.alp.p ] ; then
      rm $rundir/ds-op-label.tuple.dictionary.$testsetSize.RRalb.alp.p
    fi
    cp $wdcat/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.iter$iterationCtr.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.RRalb.alp.p
  fi
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir
  isUR=true
  if [ "$isUR" = true ] ; then
    if [ ! -d URalb ]; then
      mkdir URalb
    fi
    cd URalb
    if [ ! -d $rCategory ]; then
      mkdir $rCategory
    fi
    cd $rCategory
    if [ ! -d "jcm-"$testsetSize ]; then
      mkdir jcm-$testsetSize
    fi
    if [ ! -d "logfiles" ]; then
      mkdir logfiles
    fi
    cd jcm-$testsetSize
    alwdnew=$(pwd)
      #Get all the iteration files
    mv $oldwd/p3.traininsf.almURdids.iter$iterationCtr.dat $alwdnew/.
    mv $oldwd/p3.testinsf.almURdids.iter$iterationCtr.dat $alwdnew/.
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/allocation.py true ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory/combined.$rCategory.datafile.temp.dat ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory/pickleFiles/combined.$rCategory.fdat.p $alwdnew/p3.traininsf.almURdids.iter$iterationCtr.dat $alwdnew/p3.testinsf.almURdids.iter$iterationCtr.dat  $alwdnew/trainfile.iter$iterationCtr.dat  $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat $testsetSize
    cut -d' ' -f1 $alwdnew/trainfile.iter$iterationCtr.dat  >> $alwdnew/trainf.count.lables.iter$iterationCtr.dat
    cut -d' ' -f1 $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat  >> $alwdnew/testinsf.$testsetSize.count.lables.iter$iterationCtr.dat
    cd ../rootdirpath/Research/svm_light
    ./svm_learn -v 3 $alwdnew/trainfile.iter$iterationCtr.dat $alwdnew/model.trainCount.$testsetSize.dat >> ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir/URalb/$rCategory/logfiles/svm.finaltrain.$testsetSize.log 2>&1
    ./svm_classify $alwdnew/testinsf.$testsetSize.iter$iterationCtr.dat $alwdnew/model.trainCount.$testsetSize.dat $alwdnew/test.prediction.iter$iterationCtr.tCount.$testsetSize.dat >> ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir/URalb/$rCategory/logfiles/svm.finaltest.$testsetSize.log
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wdcat $rCategory $alwdnew/p3.testinsf.almURdids.iter$iterationCtr.dat $alwdnew/test.prediction.iter$iterationCtr.tCount.$testsetSize.dat $alwdnew/testinsf.$testsetSize.count.lables.iter$iterationCtr.dat $testsetSize $iterationCtr
    python ../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wdcat $rCategory $alwdnew/p3.traininsf.almURdids.iter$iterationCtr.dat $wdcat/predictions/train/predictions4Platt.781265.dat $alwdnew/trainf.count.lables.iter$iterationCtr.dat $trainsetSize $iterationCtr
    if [ -f $rundir/ds-op-label.tuple.dictionary.$testsetSize.URalb.alp.p ] ; then
      rm $rundir/ds-op-label.tuple.dictionary.$testsetSize.URalb.alp.p
    fi
    cp $wdcat/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.iter$iterationCtr.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.URalb.alp.p
  fi
done
