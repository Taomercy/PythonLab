#!/bin/bash -x
python GenerateErrorData.py -c

errorList=("cloneError" "netError" "complieError" "otherError")
jobList=('JNB1' 'JNB2' 'JNB3' 'JNB4' 'JNB5' 'JNB6')

function clone(){
    time=$(($RANDOM%10+1))
    error=${errorList[0]}
    jIndex=$(( $(($RANDOM%4+1)) - 1))
    jobname=${jobList[$jIndex]}
    
    rate="0.$(($RANDOM%20))"
    python GenerateErrorData.py -e $error -r $rate -j $jobname -t $time
}

function net(){
    time=$(($RANDOM%1000+1))
    error=${errorList[1]}
    jIndex=$(( $(($RANDOM%4+1)) - 2))
    jobname=${jobList[$jIndex]}

    rate="0.$(($RANDOM%30+10))"
    python GenerateErrorData.py -e $error -r $rate -j $jobname -t $time
}


function compile(){
    time=$(($RANDOM%1000+1))
    error=${errorList[2]}
    jIndex=$(( $(($RANDOM%4+1)) - 2))
    jobname=${jobList[$jIndex]}

    rate="0.$(($RANDOM%20+60))"
    python GenerateErrorData.py -e $error -r $rate -j $jobname -t $time
}

function noise(){
    eIndex=$(( $(($RANDOM%4+1)) - 1))
    error=${errorList[$eIndex]}

    jIndex=$(( $(($RANDOM%6+1)) - 1))
    jobname=${jobList[$jIndex]}
 
    time=$(($RANDOM%8000+1))
 
    rate="0.$(($RANDOM%100))"
    python GenerateErrorData.py -e $error -r $rate -j $jobname -t $time
}

for i in {1..10};
do 
    clone
    net
    compile
    noise
done;
