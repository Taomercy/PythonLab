import os
import time

import requests
import json
import sys
import re
from github import Github

host_group = os.environ['host_group'].splitlines()
repo_list = os.environ['repo_list'].splitlines()

jenkins_user = os.environ['JENKINS_USER']
jenkins_pwd = os.environ['JENKINS_PWD']

JOB_STATUS = []
AUTH = (jenkins_user, jenkins_pwd)
BUILD_STATUS = True


class Build(object):
    url = None
    auth = None
    api_data = None

    @staticmethod
    def get_python_api(url):
        return url + '/api/python?pretty=true'

    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def get_api_data(self):
        api = self.get_python_api(self.url)
        response = requests.get(api, auth=self.auth)
        code = response.status_code
        if code != 200:
            print("[%s] error code" % self.url, code)
            return None
        json_text = response.text.replace("None", "\"None\"").replace("False", "\"False\"").replace("True", "\"True\"")
        data = json.loads(json_text)
        self.api_data = data
        return data


def check_status(job_url):
    """
    :param job_url:
    :return: True -> complete; False -> building
    """
    job = Build(job_url, AUTH)
    job_data = job.get_api_data()
    lastBuild = str(job_data["lastBuild"]["number"])
    lastCompletedBuild = str(job_data["lastCompletedBuild"]["number"])
    inQueue = job_data["inQueue"]

    build_url = job_url + f"/{lastBuild}"
    build = Build(build_url, AUTH)
    build_data = build.get_api_data()
    building = build_data["building"]

    for job in JOB_STATUS:
        if job["jobUrl"] == job_url:
            job_status = {"jobUrl": job_url, "inQueue": inQueue, "lastBuild": lastBuild,
                          "lastCompletedBuild": lastCompletedBuild, "building": building}
            if job_status != job:
                JOB_STATUS.append(job_status)
                JOB_STATUS.remove(job)
                print("[Update data]: ")
                print(f"{job} -> \n{job_status}")

    build_url = job_url + f"/{lastBuild}"
    build = Build(build_url, AUTH)
    build_data = build.get_api_data()
    building = build_data["building"]

    if job_data["inQueue"] == "False" and building == "False":
        if build_data["result"] != "SUCCESS":
            BUILD_STATUS = False
            print("[Build failed]", job_url)
        return True
    else:
        return False


def main():
    # Init Job status
    for host in host_group:
        for repo in repo_list:
            if not repo:
                continue
            job_name = repo.replace("/", "_").replace("-", "_").split(",")
            job_name = job_name[0] + "_" + job_name[-1]
            job_url = f'http://{host}:8080/job/{job_name}'
            job = Build(job_url, AUTH)
            job_data = job.get_api_data()
            inQueue = job_data["inQueue"]
            lastBuild = str(job_data["lastBuild"]["number"])
            lastCompletedBuild = str(job_data["lastCompletedBuild"]["number"])

            build_url = job_url + f"/{lastBuild}"
            build = Build(build_url, AUTH)
            build_data = build.get_api_data()
            building = build_data["building"]

            JOB_STATUS.append(
                {"jobUrl": job_url, "inQueue": inQueue, "lastBuild": lastBuild,
                 "lastCompletedBuild": lastCompletedBuild,
                 "building": building})

    for job in JOB_STATUS:
        print("[Init data]", job)

    # Monitor job status
    while JOB_STATUS:
        for job in JOB_STATUS:
            if check_status(job["jobUrl"]):
                try:
                    JOB_STATUS.remove(job)
                except:
                    continue
                print("[Build complete]", job)

    if BUILD_STATUS is False:
        sys.exit(1)


if __name__ == '__main__':
    print("Waiting 20 seconds for jenkins job start...")
    time.sleep(20)
    main()
