#!/usr/bin/env python
# encoding: utf-8

import os
import os.path

from fabric.api import lcd, local, warn_only
import begin


def get_top_dir(path):
    if not os.path.dirname(path):
        return path, os.sep
    else:
        top_dir, rest = get_top_dir(os.path.dirname(path))
        return top_dir, os.path.join(rest, os.path.basename(path))


@begin.subcommand
def pull(local_filename):
    """Pulls the remote copy of LOCAL_FILENAME"""
    hostname, remote_path = get_top_dir(local_filename)
    basedir = local("git root", capture=True)
    with lcd(basedir):
        local("git stash")
        local("scp %s:%s %s" % (hostname, remote_path, local_filename))
        with warn_only():
            local("git commit -m 'Pull from remote' %s" % local_filename)
            local("git stash pop")


@begin.start
def run():
    pass
