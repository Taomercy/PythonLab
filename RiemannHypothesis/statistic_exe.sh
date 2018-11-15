#!/bin/bash
filename=$1

function loop(){
    time=$1
    column=$2
    row=$3
    num=$4
    for ((i=1; i<=$time;i++));
    do
        python RiemannHypothesis_faster.py $filename -c $column -r $row  -n $num
    done    
}

function column_loop(){
    column=$1
    loop 10 $column 1000 1000
    loop 10 $column 1000 10000
    loop 10 $column 1000 100000
    loop 10 $column 1000 1000000
}

function statistic(){
    for ((i=2; i<=10; i++));
    do
        column_loop $i
    done
}

statistic
