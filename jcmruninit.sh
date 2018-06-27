#!/bin/bash

# For each category First create the featureFile and fileID pickles saperately.
# This is done prior for optimizing the speed.

lamPL=$1
lamPW=$2
lamLP=$3
lamLW=$4
lamWP=$5
lamWL=$6
testsetSize=781265
runID=$8
rC=$9
pC=${10}

cd ../rootdirpath/jvdofs/expDir/eruns
mkdir $runID-wdir
temporaryFilePath=../rootdirpath/jvdofs/tempwd
cd $temporaryFilePath
trainInsCount=23149
rm -rf *
doCV=true
alpha=1.0


declare -a catArr=($rC $pC)
dfp=../rootdirpath/Research/jvdofs/mfpadat
SECONDS=0
for rCategory in "${catArr[@]}"
do
  echo "Category is $rCategory"
  if [ ! -d "$temporaryFilePath/$rCategory" ]; then
    cd $temporaryFilePath
    mkdir $rCategory
    cd $rCateogory
  fi
  cd ../rootdirpath/jvdofs/expDir/eruns/$runID-wdir
  if [ ! -d "$rCategory" ]; then
    mkdir $rCategory
  fi
  cd $rCategory
  wd=$(pwd)
  #echo "The working dir is: $wd"
  if [ ! -d "$wd/pickleFiles" ]; then
    mkdir pickleFiles
  fi
  if [ ! -d "$wd/logFiles" ]; then
    mkdir logFiles
  fi
  if [ ! -d "$wd/predictions" ]; then
    mkdir predictions
    cd predictions
    mkdir test
    mkdir train
  fi

  cd ../rootdirpath/Research/jvdofs/
  if [ ! -f $wd/combined.$rCategory.datafile.temp.dat ]
    then
      paste -d ' ' $dfp/lyrl2004_tokens.txt $dfp/rcv1_$rCategory.txt $dfp/rcv1_features.txt  >> $wd/combined.$rCategory.datafile.temp.dat
      paste -d ' ' $dfp/lyrl2004_tokens.txt $dfp/rcv1_$rCategory.txt  >> $wd/rcv1v2.$rCategory.labids.txt
  fi
  cp $wd/rcv1v2.$rCategory.labids.txt ../rootdirpath/Research/jvdofs/mfpadat/rcv1v2.$rCategory.labids.txt
  chmod 774 ../rootdirpath/Research/jvdofs/mfpadat/rcv1v2.$rCategory.labids.txt
  LYRL2004_trainIDs=../rootdirpath/Research/jvdofs/mfpadat/lyrl2004_tokens_train.dat
  LYRL2004_b0testIDs=../rootdirpath/Research/jvdofs/mfpadat/lyrl2004_tokens_test_set.dat
  # Python call here to allocate train and test files
  python ../rootdirpath/Research/jvdofs/Fall2016/scripts/allocation.py false $wd/combined.$rCategory.datafile.temp.dat $wd/pickleFiles/combined.$rCategory.fdat.p $LYRL2004_trainIDs $LYRL2004_b0testIDs $wd/trainfile.dat $wd/testinsf.$testsetSize.dat $testsetSize
  cut -d' ' -f1 $wd/trainfile.dat >> $wd/trainf.count.lables.dat
  cut -d' ' -f1 $wd/testinsf.$testsetSize.dat >> $wd/testinsf.$testsetSize.count.lables.dat
  if [ "$doCV" = true ] ;
  then
    #echo "STATUS: Starting CV. This will be done only once." # since the training set does not change
    # CV required for doing PlattCaliberation
    #Copy the training instances to scratch to perform 10-fold Cross Validation
    cp $wd/trainfile.dat $temporaryFilePath/$rCategory/trainfile.dat
    # Set-up for 10-fold Cross validation
    binctr=`echo $((23140/10))`
    bin1=$temporaryFilePath/$rCategory/trainfile.bin1.dat
    bin2=$temporaryFilePath/$rCategory/trainfile.bin2.dat
    bin3=$temporaryFilePath/$rCategory/trainfile.bin3.dat
    bin4=$temporaryFilePath/$rCategory/trainfile.bin4.dat
    bin5=$temporaryFilePath/$rCategory/trainfile.bin5.dat
    bin6=$temporaryFilePath/$rCategory/trainfile.bin6.dat
    bin7=$temporaryFilePath/$rCategory/trainfile.bin7.dat
    bin8=$temporaryFilePath/$rCategory/trainfile.bin8.dat
    bin9=$temporaryFilePath/$rCategory/trainfile.bin9.dat
    bin10=$temporaryFilePath/$rCategory/trainfile.bin10.dat

    head -n $binctr $temporaryFilePath/$rCategory/trainfile.dat >> $bin1
    bst=`echo $(($binctr*1+1))`
    bend=`echo $(($binctr*2))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin2
    bst=`echo $(($binctr*2+1))`
    bend=`echo $(($binctr*3))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin3
    bst=`echo $(($binctr*3+1))`
    bend=`echo $(($binctr*4))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin4
    bst=`echo $(($binctr*4+1))`
    bend=`echo $(($binctr*5))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin5
    bst=`echo $(($binctr*5+1))`
    bend=`echo $(($binctr*6))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin6
    bst=`echo $(($binctr*6+1))`
    bend=`echo $(($binctr*7))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin7
    bst=`echo $(($binctr*7+1))`
    bend=`echo $(($binctr*8))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin8
    bst=`echo $(($binctr*8+1))`
    bend=`echo $(($binctr*9))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin9
    bst=`echo $(($binctr*9+1))`
    bend=`echo $(($binctr*10 +9))`
    sed -n "$bst, $bend p" $temporaryFilePath/$rCategory/trainfile.dat >> $bin10

    #echo "STATUS: Starting to Run SVM on training-set using 10-fold Cross Validation"
    for (( i=1; i <=10; i++ ))
    do
     if [ $i -eq 1 ]
     then
      # bin1 is the held-out test set. For SVMs, the test-set instances are present in the training set without lables
      cp $bin1 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin2 $bin3 $bin4 $bin5 $bin6 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
      ./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed Training and Testing : test count $testsetSize , iteration $i, with wd $wd"
     elif [ $i -eq 2 ]
     then
     	cp $bin2 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin3 $bin4 $bin5 $bin6 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed Training and Testing : test count $testsetSize , iteration $i "
     elif [ $i -eq 3 ]
     then
     	cp $bin3 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin4 $bin5 $bin6 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 4 ]
     then
     	cp $bin4 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin5 $bin6 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 5 ]
     then
     	cp $bin5 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin6 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 6 ]
     then
     	cp $bin6 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin5 $bin7 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 7 ]
     then
     	cp $bin7 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin5 $bin6 $bin8 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 8 ]
     then
     	cp $bin8 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin5 $bin6 $bin7 $bin9 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     elif [ $i -eq 9 ]
     then
     	cp $bin9 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin5 $bin6 $bin7 $bin8 $bin10 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     else
     	cp $bin10 $wd/testfile4CV.$testsetSize.iter$i.dat
    	cat $bin1 $bin2 $bin3 $bin4 $bin5 $bin6 $bin7 $bin8 $bin9 >> $wd/trainingfile4CV.$testsetSize.iter$i.dat
    	cd ../rootdirpath/Research/svm_light
     	./svm_learn -v 3 $wd/trainingfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.log 2>&1
     	./svm_classify $wd/testfile4CV.$testsetSize.iter$i.dat $wd/model.$testsetSize.iter$i.dat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/logFiles/svm.cv.$testsetSize.iter$i.result.log
     # 	echo "STATUS: Completed CV for test-size $testsetSize ; iteration $i"
     fi
    done
    # Merge all the 10-fold CV prediction results to get a  predictions on all the $testsetSize instances; then get Platt Parameters
    for (( i=1; i <=10; i++ ))
    do
      cat $wd/predictions/train/cvp.$testsetSize.iter$i.dat >> $wd/predictions/train/predictions4Platt.$testsetSize.dat
      cat $wd/testfile4CV.$testsetSize.iter$i.dat >> $wd/test4Platt.$testsetSize.dat
    done
    cut -d' ' -f1 $wd/test4Platt.$testsetSize.dat >> $wd/test4Platt.$testsetSize.count.lables.dat

    trainFileLineCount=`cat $wd/trainfile.dat | wc -l`

    negCtr=0
    while read -r line
    do
        if [[ $line =~ '-' ]]; then
          negCtr=$((negCtr+1))
        fi
    done < "$wd/trainf.count.lables.dat"

    # echo "Total Number of Training samples: $trainFileLineCount"
    # echo "Total Number of negative samples in Train-set: $negCtr"
    posCtr=$(expr $trainFileLineCount - $negCtr)
    # echo "Total Number of positive samples in Train-set: $posCtr"
    plattPrameters=$(python ../rootdirpath/Research/jvdofs/Fall2016/scripts/PlattCaliberation.py $wd/test4Platt.$testsetSize.count.lables.dat $wd/predictions/train/predictions4Platt.$testsetSize.dat 2> $wd/logFiles/PlattCaliberation.$testsetSize.log)
    PARAMETERS="$(echo -e "${plattPrameters}" | tr -d '[[:space:]]')"
    echo "STATUS: Platt caliberation Completed, $PARAMETERS"
  fi
done
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

