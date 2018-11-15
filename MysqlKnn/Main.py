#!/usr/bin/python
# -*- coding: UTF-8 -*-

from TbOperator import *
import DataBaseInfo
from numpy import *
import knn
import getopt
import errorCollection
import sys

username = DataBaseInfo.username
password = DataBaseInfo.password
dbName = DataBaseInfo.dbName
jobNameTb = DataBaseInfo.jobNameTb
errorTypeTb = DataBaseInfo.errorTypeTb
errorFeatureTb = DataBaseInfo.errorFeatureTb
actionIDTb = DataBaseInfo.actionIDTb
actionTriggerResTb = DataBaseInfo.actionTriggerResTb


class Configuration:
    def __init__(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "-h-c-e:-j:-t:-r:",
                                       ["help", "clean", "error", "jobName", "buildTime", "recentSuccessRate"])
            if len(opts) == 0:
                print "Missing parameter"
                usage()
                sys.exit(1)
        except getopt.GetoptError, e:
            print >>sys.stderr, "Error:", e
            usage()
            sys.exit(1)

        self.clean = False
        self.error = None
        self.jobName = None
        self.buildTime = None
        self.recentSuccessRate = 0.00
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-c", "--clean"):
                self.clean = True
            if o in ("-e", "--error"):
                self.error = a
            if o in ("-j", "--jobName"):
                self.jobName = a
            if o in ("-t", "--buildTime"):
                self.buildTime = int(a)
            if o in ("-r", "--recentSuccessRate"):
                self.recentSuccessRate = float(a)


def usage():
    print >>sys.stderr, """
Usage:
    python [script.py] [Option]
    Options:
    -c, --clean                 Truncate mysql table default=[False]
    -e, --error                 Error string
    -j, --jobName               Job name
    -t, --buildTime             Build time when it failed
    -r, --recentSuccessRate
"""


def table_drop(db):
    drop_table(db, errorFeatureTb)
    drop_table(db, jobNameTb)
    drop_table(db, errorTypeTb)
    drop_table(db, actionIDTb)
    drop_table(db, actionTriggerResTb)


def error_prediction_by_knn(db, k):
    try:
        job_id_for_predict = data_select(db, jobNameTb, 'JobName', conf.jobName, 'id')[0][0]
    except:
        job_id_for_predict = data_select(db, jobNameTb, whatSelect='max(id)')[0][0] + 1
    inX = array([job_id_for_predict, conf.recentSuccessRate, conf.buildTime], dtype='float64')
    res = data_select(db, errorFeatureTb)
    dataSet, labels = knn.matrix_from_mysql(res)
    if len(dataSet) < k:
        print "There is not enough data to predict."
        return
    knn.plot_save(dataSet, labels, 'dataPlot.png', show=True)
    error_predict = knn.classify0(inX, dataSet, labels, k)
    print "I predict the error type is", data_select(db, errorTypeTb, 'id', error_predict, 'ErrorString')[0][0]
    print "The Error collected is", conf.error


def choose_action_by_knn(db, errorType, k):
    time = data_select(db, actionTriggerResTb, whatSelect='min(BuildTime)')[0][0]
    # in inX choose success and min time action for the error
    inX = array([errorType, 1, time])
    res = data_select(db, actionTriggerResTb)
    dataSet, labels = knn.matrix_from_mysql(res)
    actionID = knn.classify0(inX, dataSet, labels, k)
    return actionID


def count_recent_build(db, build_stat, job_name):
    if build_stat:
        sql_cmd = "update {0} set RecentBuild=0".format(jobNameTb)
    else:
        sql_cmd = "update {0} set RecentBuild=RecentBuild+1 where JobName='{1}'".format(jobNameTb, job_name)
    db.update(sql_cmd)


def trigger(actionID):
    import random
    result = random.choice([True, False])
    time = random.randint(0, 10000)
    stat = 1 if result else 0
    return stat, time


def main():
    global conf
    conf = Configuration()
    job_name = conf.jobName
    error = conf.error
    db = DataBase(username, password, dbName)
    if conf.clean:
        table_drop(db)
        sys.exit(0)

    # collect job, error
    collect_job_name(db, jobNameTb, job_name)
    collect_error_type(db, errorTypeTb, error)

    # error predict
    errorCollection.error_collect(db, conf.error, conf.recentSuccessRate, conf.jobName, conf.buildTime)
    error_prediction_by_knn(db, 3)

    # generate action list
    actionList = ["retrgger", "waittimes", "other"]
    prepare_action_type(db, actionIDTb, actionList)

    errorType = data_select(db, errorTypeTb, 'ErrorString', error, 'id')[0][0]
    res = data_select(db, actionTriggerResTb, "ErrorType", errorType)
    if not res:
        res = ()

    k, flag = 3, 0
    if len(res) < k:
        actions = data_select(db, actionIDTb, whatSelect='ActionString')
        for action in actions:
            flag = 0
            actionID = data_select(db, actionIDTb, 'ActionString', action[0], 'id')[0][0]

            stat, time = trigger(actionID)
            collect_action_trigger_res(db, actionTriggerResTb, errorType, stat, time, actionID)
            if stat:
                print "The error resolved."
                flag = 1
                break

        if not flag:
            print "No action can resolve it."
            sys.exit(0)

    else:
        # set the count limit
        recentBuild = data_select(db, jobNameTb, 'JobName', job_name, whatSelect='RecentBuild')[0][0]
        if recentBuild > 2:
            print "It's triggered three times and failed."
            sys.exit(0)

        # choose the action by knn
        actionID = choose_action_by_knn(db, errorType, k)
        print "Choose the action by knn:", data_select(db, actionIDTb, 'id', actionID, whatSelect='ActionString')[0][0]

        stat, time = trigger(actionID)
        collect_action_trigger_res(db, actionTriggerResTb, errorType, stat, time, actionID)
        if stat:
            print "The error resolved."
        else:
            print "The error unsolved"

        count_recent_build(db, stat, job_name)

    db.close()


if __name__ == '__main__':
    main()
