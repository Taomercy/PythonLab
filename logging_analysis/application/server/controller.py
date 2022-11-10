import re
import shutil
import subprocess
from application.server.object import ServerLogger, Properties, Configuration
from application.server.settings import *
from hwwuex_check.utils.utils import search_files_deeply

help_information = """================Help Information================
    stability_check $path all,applog,memory,alarm
    upgrade_check
    case_path_list
    properties_list_now properties_list properties_save rm_properties_remove
================================================"""


def get_my_check_result_list():
    my_check = []
    result_path = os.path.join(RESULT_ROOT, Properties().user)
    paths = os.listdir(result_path)
    for path in paths:
        my_check.append(path)
    return my_check


def answer(message):
    response = None
    assert type(message) is str
    message = message.strip()
    # TODO: usage and workflow design
    logger = ServerLogger().logger
    if not STORAGE_PATH:
        return "Cannot connect to log path"

    if message.lower() == "help" or message == "?":
        response = help_information

    if message == "who":
        config = Configuration()
        response = config.who

    # dynamic module reflection
    command_list = message.split(" ")
    res = re.match(r"^(.*)_check", command_list[0])
    if res:
        module_name = res.group(1)
        func_name = "check"
        args = command_list[1:]
        log_path = args[0]
        log_path = os.path.join(CASE_ROOT, log_path)
        if module_name == "hss":
            if "CACC" in log_path:
                module_name = "accuracy"
            elif "CROB" in log_path:
                module_name = "robustness"
            elif "CSTAB" in log_path:
                module_name = "stability"
            else:
                return "Can not find check type."

        logger.info("module_name: %s, func_name: %s" % (module_name, func_name))

        if func_name == "check":
            try:
                mod_list = args[1].split(",")
            except IndexError:
                mod_list = ["all"]

            # import module and search func
            try:
                module = __import__("hwwuex_check.test_case." + module_name, fromlist=True)
                if hasattr(module, func_name):
                    check_func = getattr(module, func_name)
                    response = check_func(log_path, module_name, mod_list)

            except ModuleNotFoundError as e:
                try:
                    # deploy path
                    models_path = os.path.join(hwwuex_check, "models")
                    model_files = os.listdir(models_path)
                except:
                    # test path
                    models_path = os.path.join(os.getcwd(), "hwwuex_check", "models")
                    model_files = os.listdir(models_path)
                models = [m.split(".")[0] for m in model_files]
                del models[models.index("__init__")]
                try:
                    del models[models.index("__pycache__")]
                except:
                    pass
                response = "%s\nModule list: %s" % (e, str(models))
            except Exception as e:
                response = e

    if message.startswith("chmod"):
        (status, output) = subprocess.getstatusoutput(message)
        response = output

    if message.startswith("cat"):
        (status, output) = subprocess.getstatusoutput(message)
        response = output

    if message.startswith("check_result_clean"):
        result_path = os.path.join(RESULT_ROOT, Properties().user)
        try:
            result_folder = message.split(" ")[-1]
            if len(message.split(" ")) == 1:
                result_folder = None
        except IndexError:
            result_folder = None

        if result_folder:
            p = os.path.join(result_path, result_folder)
            shutil.rmtree(p)
            response = "removed"
        else:
            results = get_my_check_result_list()
            response = []
            for result in results:
                p = os.path.join(result_path, result)
                try:
                    shutil.rmtree(p)
                except:
                    response.append("%s is protected, cannot remove." % p)

    if message == "check_result_list":
        response = get_my_check_result_list()

    if message.startswith("summary"):
        response = []
        result_path = os.path.join(RESULT_ROOT, Properties().user)
        results = get_my_check_result_list()
        for result in results:
            p = os.path.join(result_path, result)
            summary = os.path.join(p, "summary.log")
            if os.path.exists(summary):
                cmd = "cat %s" % summary
                (status, output) = subprocess.getstatusoutput(cmd)
                response.append("=" * 40 + result + "=" * 40)
                response.append("storage path: %s\n" % summary)
                response.append(output)
                response.append("\n\n")

    if message == "case_path_list":
        pathes = []
        for p in os.listdir(CASE_ROOT):
            if p.startswith("TC-") and os.path.isdir(os.path.join(CASE_ROOT, p)):
                    pathes.append(p)
        response = pathes

    if message.startswith("cat "):
        filename = message.split(" ")[1]
        file = search_files_deeply(Configuration().path, filename)[0]
        cmd = "cat %s" % file
        (status, output) = subprocess.getstatusoutput(cmd)
        response = output

    if message.startswith("properties_list"):
        files = []
        for f in os.listdir(Configuration().path):
            if f == "config.yaml":
                continue
            pattern = re.compile(".*.yaml")
            ret = pattern.search(f)
            if ret:
                files.append(f)
        response = files

    if message.startswith("properties_show"):
        try:
            properties_file = message.split(" ")[1]
            properties_file = search_files_deeply(Configuration().path, properties_file)[0]
        except IndexError as e:
            properties_file = Properties().file
        cmd = "cat %s" % properties_file
        (status, output) = subprocess.getstatusoutput(cmd)
        response = output

    if message.startswith("properties_save"):
        Properties().save()
        response = "save success"

    if message.startswith("properties_remove"):
        filename = message.split(" ")[1]
        files = search_files_deeply(Configuration().path, filename)
        for f in files:
            os.remove(f)
        response = "removed"

    if message.startswith("properties_copy"):
        filename = message.split(" ")[1]
        Properties().copy(filename)
        response = "copy success"

    if message.startswith("properties_update"):
        parameter = {}
        text = message.split(" ")[1]
        arg = text.split(",")
        for a in arg:
            key = a.split("=")[0]
            value = a.split("=")[1]
            parameter.update({key: value})
        Properties().add_or_update(**parameter)
        response = "update success"

    if message.startswith("properties_delete"):
        keys = message.split(" ")[1].split(",")
        Properties().delete(keys)
        response = "delete success"

    if message.startswith("rm "):
        object = message.split(" ")[1]
        # TODO: search object and remove
        response = "remove " + object

    logger.debug(response)
    return "\n".join(response) if type(response) is list else response
