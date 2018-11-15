#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
collect error,job name, build time, recent success rate to judge error type
'''
from TbOperator import *
import sys
import MySQLdb
import getopt
import DataBaseInfo

username = DataBaseInfo.username
password = DataBaseInfo.password
dbName = DataBaseInfo.dbName
errorFeatureTb = DataBaseInfo.errorFeatureTb
jobNameTb = DataBaseInfo.jobNameTb
errorTypeTb = DataBaseInfo.errorTypeTb


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


def table_truncate(db):
    truncate_table(db, errorFeatureTb)
    truncate_table(db, jobNameTb)
    truncate_table(db, errorTypeTb)


def table_drop(db):
    drop_table(db, errorFeatureTb)
    drop_table(db, jobNameTb)
    drop_table(db, errorTypeTb)


def error_collect(db, error, recent_success_rate, job_name, build_time):
    job_id = data_select(db, jobNameTb, 'JobName', job_name)[0][0]
    error_type = data_select(db, errorTypeTb, 'ErrorString', error)[0][0]
    collect_error_feature(db, errorFeatureTb, job_id, recent_success_rate, build_time, error_type)


def main():
    global conf
    conf = Configuration()
    db = DataBase(username, password, dbName)
    if conf.clean:
        table_drop(db)
        sys.exit(0)

    collect_job_name(db, jobNameTb, conf.jobName)
    collect_error_type(db, errorTypeTb, conf.error)
    error_collect(db, conf.error, conf.recentSuccessRate, conf.jobName, conf.buildTime)

    db.close()


if __name__ == '__main__':
    #main()
    pass
