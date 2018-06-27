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
rC=$9
pC=${10}
alkcounter=10
trainInsCount=23149
alpha=1.0
iterationCtr=0
zero=0

declare -a catArr=($rC $pC)
declare -a RcatArr=($rC)

LYRL2004_b0testIDs=/../rootdirpath/Research/jvdofs/mfpadat/lyrl2004_tokens_test_set.dat
for rCategory in "${catArr[@]}"
do
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
  if [ ! -d "jcm-"$testsetSize ]; then
    mkdir jcm-$testsetSize
  fi
  cd jcm-$testsetSize
  wdnew=$(pwd)
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$rCategory
  wd=$(pwd)
  if [ ! -f $wdnew/testinsf_$testsetSize.dat ]
    then
      cp $wd/trainfile.dat $wdnew/trainfile.dat
      cp $wd/testinsf.781265.dat $wdnew/testinsf.781265.dat
      paste -d ' ' $LYRL2004_b0testIDs $wdnew/testinsf.781265.dat | shuf -n $testsetSize >> $wdnew/testinstances.$testsetSize.dat
      cut -d ' ' -f 1 $wdnew/testinstances.$testsetSize.dat >> $wdnew/testinsf_docids_$testsetSize.dat
      cut -d ' ' -f 2- $wdnew/testinstances.$testsetSize.dat >> $wdnew/testinsf_$testsetSize.dat
      cut -d' ' -f1 $wdnew/trainfile.dat >> $wdnew/trainf.count.lables.dat
      cut -d' ' -f1 $wdnew/testinsf_$testsetSize.dat >> $wdnew/testinsf.$testsetSize.count.lables.dat
      cp $wdnew/testinsf.$testsetSize.count.lables.dat $wd/testinsf.$testsetSize.count.lables.dat
      cp /../rootdirpath/Research/jvdofs/mfpadat/lyrl2004_tokens_train.dat $wdnew/traininsf_docids.dat
      cp $wdnew/testinsf_$testsetSize.dat $wd/testinsf.$testsetSize.dat
  fi
  cd /../rootdirpath/Research/svm_light
  ./svm_learn -v 3 $wd/trainfile.dat $wd/model.trainCount.$testsetSize.dat >> $wd/logFiles/svm.finaltrain.$testsetSize.log 2>&1
  ./svm_classify $wdnew/testinsf_$testsetSize.dat $wd/model.trainCount.$testsetSize.dat $wd/predictions/test/prediction.tCount.$testsetSize.dat >> $wd/logFiles/svm.finaltest.$testsetSize.log
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wd $rCategory $wdnew/testinsf_docids_$testsetSize.dat $wd/predictions/test/prediction.tCount.$testsetSize.dat $wdnew/testinsf.$testsetSize.count.lables.dat $testsetSize 0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ProbabilityCaliberation.py $wd $rCategory $wdnew/traininsf_docids.dat $wd/predictions/train/predictions4Platt.781265.dat $wd/trainf.count.lables.dat $trainInsCount 0
done

for responsiveCategory in "${RcatArr[@]}"
do
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
  cd $responsiveCategory
  respWD=$(pwd)
  if [ ! -d "jcmFiles" ]; then
    mkdir jcmFiles
  fi
  echo "STATUS: Running PHASE1 Hybrid Cost Estimation; RC=$responsiveCategory, PC=$pC"
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
  cd $pC
  privWD=$(pwd)
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$responsiveCategory/jcmFiles
  if [ ! -d "$pC" ]; then
    mkdir $pC
    cd $pC
    mkdir pickleFiles
  else
    cd $pC
  fi
  jcmWD=$(pwd)
  cd /../rootdirpath/Research/jvdofs
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/CostMatrix.py $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  SECONDS=0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/p1Caller.py $jcmWD $respWD $privWD $testsetSize $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  rJP=/../rootdirpath/Research/jvdofs/mfpadat/rcv1v2.$responsiveCategory.labids.txt
  echo " STATUS: Hybrid Model ; RC=$responsiveCategory , PC=$pC"
  wd=../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$responsiveCategory/jcmFiles/$pC
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/p2Caller.py $wd $respWD $privWD $testsetSize $rJP $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  pJP=/../rootdirpath/Research/jvdofs/mfpadat/rcv1v2.$pC.labids.txt
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/p3Caller.py $wd $respWD $privWD $testsetSize $pJP $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ComputeAnnotatorCost.py $wd $testsetSize $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ComputeMisclassificationCostControlled.py $jcmWD $testsetSize $rJP $pJP $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha false
  MINECOREduration=$SECONDS
  echo "DURATION-IN-MINS: MINECORE = $(($MINECOREduration / 60)) minutes and $(($MINECOREduration % 60)) seconds elapsed."
  


  echo "STATUS: Running Fully Automated Baseline and Fully Manual Baseline"
  SECONDS=0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/FullyAutomatedBaseline.py $wd $rJP $pJP $testsetSize $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  FAduration=$SECONDS
  echo "DURATION-IN-MINS: FA = $(($FAduration / 60)) minutes and $(($FAduration % 60)) seconds elapsed."
  
  
  SECONDS=0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/FullyManualBaseline.py $rJP $pJP $testsetSize $wdnew/testinsf_docids_$testsetSize.dat
  FMduration=$SECONDS
  echo "DURATION-IN-MINS: FM = $(($FMduration / 60)) minutes and $(($FMduration % 60)) seconds elapsed."
  
  echo "STATUS: Now Running Relevance Ranking Baseline Model"
  SECONDS=0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/RelevanceRankingBaseline.py $respWD $privWD $jcmWD $rJP $pJP $testsetSize $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  RRduration=$SECONDS
  echo "DURATION-IN-MINS: RR = $(($RRduration / 60)) minutes and $(($RRduration % 60)) seconds elapsed."

  echo "STATUS: Now Running Uncertainity Ranking Baseline Model"
  SECONDS=0
  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/UncertainityRankingBaseline.py $respWD $privWD $jcmWD $rJP $pJP $testsetSize $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha
  URduration=$SECONDS
  echo "DURATION-IN-MINS: UR = $(($URduration / 60)) minutes and $(($URduration % 60)) seconds elapsed."

  echo "STATUS: Now Running Active Learning Models"
  SECONDS=0
  source "../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$responsiveCategory/jcmFiles/$pC/tauR.$testsetSize.txt"
  source "../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/$responsiveCategory/jcmFiles/$pC/tauP.$testsetSize.txt"
  echo "Tau_r value: $TAUR"
  echo "Tau_p value: $TAUP"
  wdts="../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/jcm-$testsetSize"
  kcounter=1000
  iterationCtr=1

  tri1=`expr $TAUR / $kcounter`
  if [ `expr $TAUR % $kcounter` == 0 ]; then
    ftri=`expr $TAUR / $kcounter`
  else
    ftri=`expr $tri1 + 1`
  fi

  echo "Total R iterations: $ftri"
  while [ "$iterationCtr" -le "$ftri" ]; do
    echo "iteration: $iterationCtr"
    if [ $kcounter -le $TAUR ]; then
      python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ALResponsiveness.py $respWD $jcmWD $wdts $testsetSize $kcounter $iterationCtr
      trainsetSize=`expr $trainInsCount + $kcounter`
      echo $trainsetSize
      cd /../rootdirpath/Research/jvdofs/Fall2016
      sh ./rmactiveRelevance.sh $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $testsetSize $runID $iterationCtr $trainsetSize $rC
    else
      python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ALResponsiveness.py $respWD $jcmWD $wdts $testsetSize $TAUR $iterationCtr
      trainsetSize=`expr $trainInsCount + $TAUR`
      echo $trainsetSize
      cd /../rootdirpath/Research/jvdofs/Fall2016
      sh ./rmactiveRelevance.sh $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $testsetSize $runID $iterationCtr $trainsetSize $rC
    fi
    kcounter=`expr $kcounter + 1000`
    iterationCtr=$(($iterationCtr + 1))
  done

  kpcounter=1000
  piterationCtr=1
  tpi1=`expr $TAUP / $kpcounter`
  if [ `expr $TAUP % $kpcounter` == 0 ]; then
    ftpi=`expr $TAUP / $kpcounter`
  else
    ftpi=`expr $tpi1 + 1`
  fi
  echo "Total P iterations: $ftpi"

  while [ "$piterationCtr" -le "$ftpi" ]; do
    echo "iteration: $piterationCtr"
    if [ $kpcounter -le $TAUP ]; then
      python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ALPrivilege.py $privWD $jcmWD $wdts $testsetSize $kpcounter $piterationCtr
      trainsetSize=`expr $trainInsCount + $kpcounter`
      echo $trainsetSize
      cd /../rootdirpath/Research/jvdofs/Fall2016
      sh ./rmactivePrivilege.sh $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $testsetSize $runID $piterationCtr $trainsetSize $pC
    else
      python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ALPrivilege.py $privWD $jcmWD $wdts $testsetSize $TAUP $piterationCtr
      trainsetSize=`expr $trainInsCount + $TAUP`
      echo $trainsetSize
      cd /../rootdirpath/Research/jvdofs/Fall2016
      sh ./rmactivePrivilege.sh $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $testsetSize $runID $piterationCtr $trainsetSize $pC
    fi
    kpcounter=`expr $kpcounter + 1000`
    piterationCtr=$(($piterationCtr + 1))
  done
  ALduration=$SECONDS
  echo "DURATION-IN-MINS: AL = $(($ALduration / 60)) minutes and $(($ALduration % 60)) seconds elapsed."

  echo "STAUTS: Computing costs for Active Learning Baselines"
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
  if [ ! -d "alwdir" ]; then
    mkdir alwdir
  fi
  cd -

  rundir=../rootdirpath/jvdofs/expDir/eruns/$runID-wdir/alwdir
  if [ $TAUR -eq $zero ]; then
    echo "Value of Tau r is zero"
    cp $respWD/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.RRalb.alr.p
    cp $respWD/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.URalb.alr.p
  fi
  if [ $TAUP -eq $zero ]; then
    echo "Value of Tau p is zero"
    cp $privWD/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.RRalb.alp.p
    cp $privWD/pickleFiles/ds-op-label.tuple.dictionary.$testsetSize.p $rundir/ds-op-label.tuple.dictionary.$testsetSize.URalb.alp.p
  fi

  python /../rootdirpath/Research/jvdofs/Fall2016/scripts/ComputeMisclassificationCostControlled.py $rundir $testsetSize $rJP $pJP $lamPL $lamPW $lamLP $lamLW $lamWP $lamWL $alpha true
  
  
  echo "STATUS: All done"
done
