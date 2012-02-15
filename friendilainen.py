#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# friendilainen
#
# Detect changes in your Facebook friends list.
#
# Authors: Konrad Markus <konker@gmail.com>
#


import os
import urllib2
from datetime import datetime

import pathhack
from lib import json
from pyvcs import VCS, OK

BASE_URL = 'https://graph.facebook.com'
FRIENDS_URL = '%s/me/friends?access_token=' % BASE_URL
HERE = os.path.dirname(os.path.realpath(__file__))
ACCESS_TOKEN_TXT = os.path.join(HERE, 'access_token.txt')
DATA = os.path.join(HERE, 'data')
DATA_JSON = os.path.join(DATA, 'friends.json')


def main():
    vcs = VCS(DATA)

    # get the contents of url.txt
    with open(ACCESS_TOKEN_TXT, 'r') as f:
        access_token = f.read()

    # fetch the url
    url = "%s%s" % (FRIENDS_URL, access_token)
    json = urllib2.urlopen(url).read()

    # split the json up into lines
    json = json.replace('[{', "[\n{")
    json = json.replace('},', "},\n")
    json = json.replace('}],', "}\n]")

    # write json to data/friends.json
    with open(DATA_JSON, 'w') as f:
        f.write(json)

    # git diff -> send email if not empty
    diff = vcs.diff()
    if diff != []:
        # filter out rows which aren't friend data
        diff = filter(lambda x: x[1] == '{', diff)
        print format_changes(diff)
    else:
        print "friendilainen: nothing happened"

    # git add/commit
    message = "friendilainen: %s" % datetime.now().isoformat()
    code, ret = vcs.commit_all(message)
    if code != OK:
        print "ERROR with commit: %s" % ret


# helpers
def format_changes(diff):
    s = "friendilainen: %s\n" % datetime.now().isoformat()
    s += "========================================\n"
    s += "Friends removed:\n"
    s += "----------------\n"
    for d in filter(lambda x: x[0] == '-', diff):
        s += _format_line(d)

    s += "\n"
    s += "Friends added:\n"
    s += "----------------\n"
    for d in filter(lambda x: x[0] == '+', diff):
        s += _format_line(d)

    s += "\n"
    return s

def _format_line(d):
    d = json.loads(d[1:-1])
    s = d['name'] + ": "
    s += "%s/%s" % (BASE_URL, d['id']) + "\n"
    return s

if __name__ == '__main__':
    main()
