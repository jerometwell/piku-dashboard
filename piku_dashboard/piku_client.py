import logging
import os

import subprocess
from dataclasses import dataclass
import re
import glob

logger = logging.getLogger(__name__)

PIKU_BIN = "/home/piku/piku.py"
PIKU_ROOT = os.environ.get("PIKU_ROOT", os.path.join(os.environ["HOME"], ".piku"))
LOG_ROOT = os.path.abspath(os.path.join(PIKU_ROOT, "logs"))


@dataclass
class PikuApp:
    active: bool
    id: str

class PikuError(RuntimeError):
    pass


def piku_run(args):
    cmd = subprocess.run([PIKU_BIN, *args], stdout=subprocess.PIPE)
    result = cmd.stdout.decode().strip()
    if result.startswith("Error:"):
        raise PikuError(result)

    return result


def all_apps():
    data = piku_run(["apps"]).split("\n")
    logger.debug("cmd output: %s", data)
    apps = []
    for item in data:
        match = re.match(r"\s*(\*)?\s*(.+)\s*", item)
        if not match:
            continue

        active = match[1] is not None

        app = PikuApp(active=active, id=match[2])
        apps.append(app)

    return apps


def logs(appid):
    logfiles = glob.glob(os.path.join(LOG_ROOT, appid, "*" + ".*.log"))

    if len(logfiles) < 1:
        raise ValueError("No log files found, likely bad appid")

    logger.debug("found logfiles for %s: %s", appid, logfiles)

    logcontent = {}
    for logfilename in logfiles:
        logcontent[os.path.basename(logfilename)] = open(
            logfilename, "r", encoding="utf-8", errors="ignore"
        ).readlines()[-100:]

    return logcontent


def ps(appid):
    data = piku_run(["ps", appid])


def config(appid):
    config_lines = piku_run(["config", appid]).split("\n")
    config_entries = [x.split("=") for x in config_lines]
    return {k: v for k, v in config_entries}

def set_config(appid, configs):
    config_args = [f"{k}={v}" for k, v in configs.items()]
    result = piku_run(["config:set", appid, *config_args])
    logger.info("Set %d configs for %s", len(configs), appid)

def deploy_app(appid):
    result = piku_run(["deploy", appid])
    logger.info("started %s: %s", appid, result)


def stop_app(appid):
    result = piku_run(["stop", appid])
    logger.info("stopped %s: %s", appid, result)


def restart_app(appid):
    result = piku_run(["restart", appid])
    logger.info("stopped %s: %s", appid, result)


def destroy_app(appid):
    result = piku_run(["destroy", appid])
    logger.info("stopped %s: %s", appid, result)
