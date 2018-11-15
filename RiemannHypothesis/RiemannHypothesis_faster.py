#!/usr/bin/env python
from __future__ import division
from optparse import OptionParser
import numpy as np
import sys
import time

class Configuration:
    def __init__(self):
        optParser = OptionParser()
        optParser.add_option('-c', '--column', action = 'store', type = "int")
        optParser.add_option('-r', '--row', action = 'store', type = "int")
        optParser.add_option('-n', '--numberlimit', action = 'store', type = "int")
        option, args = optParser.parse_args(sys.argv)
        if not option.column or not option.row:
            usage()
            sys.exit(0)
        self.column = option.column
        self.row = option.row
        if option.numberlimit:
            self.numberlimit = option.numberlimit
        else:
            self.numberlimit = 1000


def usage():
    print >>sys.stderr, """
Usage:
    python {0} filename [Option]
    Options:
    -c, --column        How many integers are there in a group
    -r, --row           How many integer groups
    -n, --numberlimit   Integer upper limit [default=1000]
""".format(sys.argv[0])


#def primeNum(num):
#    r_value = []
#    for i in range(2, num + 1):
#        for j in range(2, i):
#            if i % j == 0:
#                break
#        else:
#            r_value.append(i)
#    if not r_value:
#        r_value = [1]
#    return r_value


def primeNum(num):
    l = range(1, num+1)
    l[0] = 0
    for i in range(2, num+1):
        if l[i-1] != 0:
            for j in range(i*2, num + 1, i):
                l[j -1] = 0
    result = [ x for x in l if x != 0]
    return result

def primeFactorSolve(num, prime_list):
    for n in prime_list:
        if num % n == 0:
            return [n, num // n]


def primeDivisor(num):
    prime_range = primeNum(num)
    ret_value = []
    while num not in prime_range:
        factor_list = primeFactorSolve(num, prime_range)
        ret_value.append(factor_list[0])
        num = factor_list[1]
    else:
        ret_value.append(num)
    return ret_value


#def factorData(dataSet):
#    factor_array = []
#    for n in dataSet:
#        factor_list =  primeDivisor(n)
#        factor_array.append(factor_list)
#    return factor_array


#def judgeRelativelyPrime(factor_array):
#    total_factors = []
#    factors_num = 0
#    for f_list in factor_array:
#        factors_num += len(list(set(f_list)))
#        total_factors.extend(f_list)
#    total_factors = list(set(total_factors))
#    if factors_num == len(total_factors):
#       return True
#    else:
#        return False


def statistics(column, row, numLimit):
    if not numLimit:
        numLimit = 1000
    isRePrime_num = 0
    for i in range(row):
        dataSet =  np.random.random_integers(numLimit, size=(column,))
        print dataSet, 
        if judgeRelativelyPrime(dataSet):
            isRePrime_num += 1
            print "RP"
        else:
            print "Not RP"
        i += 1
    return isRePrime_num



def judgeRelativelyPrime(dataSet):
    max_num = np.max(dataSet)
    prime_list = primeNum(max_num)
    flag = 0
    for prime in prime_list:
        flag = 0
        for data in dataSet:
            if data % prime == 0:
                flag += 1
            if flag == 2:
                return False
    return True

def collect(column, row, isRePrime_num, ReciprocalProb, numberlimit, time):
    with open(statisticFile, "a") as fw:
        record = "column:{0}\t".format(column)
        record += "total:{0}\t".format(row)
        record += "RP:{0}\t".format(isRePrime_num)
        record += "prob:{0}\tzeta(s):{1}\t".format(ReciprocalProb, row / isRePrime_num)
        record += "numLimit:{0}\t".format(numberlimit)
        record += "time:{0}\n".format(time)
        fw.write(record)


try:
    statisticFile = sys.argv[1]
except:
    print "no filename"
    usage()
    sys.exit(0)
def main():
    global conf
    conf = Configuration()
    column = conf.column
    row = conf.row
    numberlimit = conf.numberlimit

    start = time.time()
    isRePrime_num =  statistics(column, row, numberlimit)
    ReciprocalProb = isRePrime_num / row if isRePrime_num else 0
    end = time.time()

    print "row:", row
    print "isRePrime_num:", isRePrime_num
    print "ReciprocalProb:", ReciprocalProb
    print "time:", end - start
    collect(column, row, isRePrime_num, ReciprocalProb, numberlimit, end - start)

if __name__ == '__main__':
    main()

