#!/usr/bin/env python3

# Summary: basic flask template showing a static web page.
#   To go further, you should use the template folders
#   More info: http://flask.pocoo.org
#   Other flask examples: https://github.com/pallets/flask/tree/master/examples/

# pre-requesite:
pre_requesite = "sudo pip3 install flask ; sudo apt-get install wpasupplicant"

import argparse
import subprocess as s
from subprocess import CalledProcessError
import sys
import time

try:
    from flask import Flask, redirect, render_template, request, url_for, _app_ctx_stack
except ImportError:
    print("Please execute first:" + pre_requesite)
    sys.exit(1)

import logging as l
import os
import re
import subprocess as s
from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_object(__name__)

def network_status(timeout=1):
    address = ("bing.com", "google.com", "microsoft.com", "youtube.com")
    for i in range(timeout):    
        for site in address:
            print("site=" + site)
            for ping in range(0, 5):
                status=True
                try:
                    res = s.check_call( ("wget -P /tmp/ " +  site).split())
                except CalledProcessError as e:
                    status=False

                if status==True:
                    print("OK, network is reachable")
                    return status
                else:
                    print("Something wrong happened, please retry")
            if status:
                break
        time.sleep(1)
    
    return status

def network_setup():
    res = str(s.check_output("iwlist wlx74da3833d939 scan".split()))
    networks = []
    for item in res.split():
        if item.startswith("ESSID"):
            network = item.split('"')[1]
            if network in networks:
                continue
            networks.append(network)
    return render_template('network.html', networks=networks)

@app.route('/network_connect', methods=['GET', 'POST'])
def network_connect():
    network = request.form.get("network")
    password = request.form.get("password")
    res = s.check_output(("wpa_supplicant " + network + " " + password).split())
    home= os.environ["HOME"]
    os.mkdir(home + os.sep + ".mirror")
    os.chdir(home + os.sep + ".mirror")
    f = open("wpa.conf",'w')
    f.write(res)
    f.flush()
    f.close()
    
    
    
    network_status(5)
    #TODO if wrong password / SSID ??? Should retry again the setup
    return mirror()
    
def mirror():
    return render_template("mirror.html")
    

@app.route('/my_root', methods=['GET', 'POST'])
def my_root():

    if network_status()==False:
        l.info("Network is currently down, launching the setup")
        return network_setup()
    else:
        return "<html><body>Network is already OK</body></html>"

@app.route('/')
def root():
    return redirect(url_for('my_root'))


def log_path():
    script_filename = os.path.abspath(__file__)
    pos = script_filename.rfind(os.sep) + 1
    script_filename = script_filename[pos:]
    base_path = re.sub('\.py$', '', script_filename)
    base_path = re.sub('\.pyc$', '', base_path)
    assert base_path != script_filename, "can't find python .py extension"
    base_path = '.' + base_path
    base_path = "/home/pi" + os.sep + base_path
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return base_path + os.sep + 'log.txt'


def main(args):
    my_log_path = log_path()
    l.basicConfig(filename=my_log_path,
                  format='%(asctime)s %(message)s', level=args.log_level)
    if not args.silent_log:
        hdlr = l.StreamHandler(sys.stdout)
        l.root.addHandler(hdlr)
    l.debug("logs will be stored into " + my_log_path)
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="script description")
    DEFAULT_LOG_LEVEL = l.DEBUG
    parser.add_argument('-l', '--log_level', default=DEFAULT_LOG_LEVEL,
                        help="set the log level. Default: debug")
    parser.add_argument('-s', '--silent_log', action="store_true",
                        help="don't output log to stdout, only log it into: " +
                        log_path() +
                        ". Default is to log to both")
    args = parser.parse_args()
    main(args)
