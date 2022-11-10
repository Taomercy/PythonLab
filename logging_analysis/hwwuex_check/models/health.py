#!/usr/bin/env python
# -*- coding:utf-8 -*-
import stat
import xml.etree.ElementTree as ET
import argparse
import filecmp
from hwwuex_check.utils.utils import *
from application.server.object import Properties

# global summary_log


def read_health_check_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def get_rules(filename, rulesName):
    root = read_health_check_file(filename)
    failed_rules_node = root.find(rulesName)
    rules = failed_rules_node.findall("HcRule")
    failed_rules_list = dict()
    i = 0
    for rule in rules:
        i = i + 1
        attrib = rule.attrib
        failed_rules = attrib.get("id") + ":" + rule.find("Description").text + " Reason: " + rule.find("Reason").text
        failed_rules_list[attrib.get("id")] = failed_rules
    return failed_rules_list

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action='store', default=None,
                        help="Path of test log", dest="path")
    parser.add_argument("-o", "--output", action='store', default=None,
                        help="Output path, example: /tmp/collection_of_health_check.log", dest="output")
    args = parser.parse_args()
    return args

def extra_failed_rules_log(rules_list, tar_file, output):
    path = Properties().path
    tmp_folder = os.path.join(path, "tmp_hc_rules")
    if os.path.exists(tar_file) and rules_list:
        un_tar(tar_file, tmp_folder)
        if "PRE" in tar_file:
            save_path = os.path.join(output, "rules_PRE")
        if "POST" in tar_file:
            save_path = os.path.join(output, "rules_POST")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for f in rules_list:
            source_file = os.path.join(tmp_folder, f + ".log")
            try:
                shutil.copy(source_file, save_path)
                target_file = os.path.join(save_path, f + ".log")
                os.chmod(target_file, stat.S_IRWXU+stat.S_IRWXO+stat.S_IRWXG)
            except IOError as e:
                print("Unable to copy file %s. %s"%(source_file, e))
            except:
                print("unexpected error when copying %s"%source_file)
        remove_dir(tmp_folder)


@calculator_execute_time
def check(case_path, output, **kwargs):
    context = ""
    code = "SUCCESS"
    if not os.path.exists(output):
        os.mkdir(output)
    log_file = os.path.join(output, "health.log")
    summary_log = init_log(log_file, console=False, level=logging.INFO)
    hc_files = search_files_deeply(case_path, r'^.*_man$')
    pre_failed_rules = dict()
    post_failed_rules = dict()
    if not hc_files:
        code = "ERROR"
        context = "Cannot find any health check result"
        return code, context
    for hc_file in hc_files:
        if "PRE" in hc_file:
            pre_failed_rules = get_rules(hc_file, "FailedRules")
            if pre_failed_rules:
                extra_failed_rules_log(pre_failed_rules.keys(), hc_file + ".tar.gz", output)
        elif "POST" in hc_file:
            post_failed_rules = get_rules(hc_file, "FailedRules")
            if post_failed_rules:
                extra_failed_rules_log(post_failed_rules.keys(), hc_file + ".tar.gz", output)
    #to_remove = []
    if pre_failed_rules and post_failed_rules:
        failed_rules_all = set(pre_failed_rules.keys()) & set(post_failed_rules.keys())
        #print("Failed rules in pre&post:" + str(failed_rules_all))
        pre_save_path = os.path.join(output, "rules_PRE")
        post_save_path = os.path.join(output, "rules_POST")
        for failed_rule_file in failed_rules_all:
            if filecmp.cmp(os.path.join(pre_save_path, failed_rule_file + ".log"), os.path.join(post_save_path, failed_rule_file + ".log"), shallow=False):
               #to_remove.append(failed_rule_file)
                del pre_failed_rules[failed_rule_file]
                del post_failed_rules[failed_rule_file]
    if pre_failed_rules:
        code = "FAILED"
        context += "\nPRE Failed Rules:\n"
        summary_log.info("PRE Failed Rules:")
        summary_log.info("\n".join(pre_failed_rules.values()))
        context += "\n".join(pre_failed_rules.values())
    if post_failed_rules:
        code = "FAILED"
        context += "\n\nPOST Failed Rules:\n"
        summary_log.info("POST Failed Rules:")
        summary_log.info("\n".join(post_failed_rules.values()))
        context += "\n".join(post_failed_rules.values())
    result_file=os.path.join(output,"health.log")

    summary_log = kwargs["summary_log"]
    summary_log.info("Check Health Result	: " + code)
#    if code == "FAILED":
#        summary_log.error("	Find some rules failed, check detail in health.log")

    return code, result_file

if __name__ == '__main__':
    parameters = parse_arguments()
    case_path = parameters.path
    code, context = health_check_result(case_path)
