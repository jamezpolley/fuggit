#!/usr/bin/env python
# encoding: utf-8

import errno
import logging
import os
import os.path

from fabric.api import local, warn_only
import begin


def get_top_dir(path):
    if not os.path.dirname(path):
        return path, os.sep
    else:
        top_dir, rest = get_top_dir(os.path.dirname(path))
        return top_dir, os.path.join(rest, os.path.basename(path))


@begin.subcommand
def add(local_filename):
    """Adds LOCAL_FILENAME from the remote system.

    LOCAL_FILENAME has the format: remote.hostname/path/to/remote/file

    This will pull /path/to/remote/file from the host named remoted.hostname
    and place it in remote.hostname/path/to/remote/file under $PWD

    The file is then added to git and committed.

    LOCAL_FILENAME must not yet exist."""

    if os.path.exists(local_filename):
        raise OSError(errno.EEXIST, "%s already exists" % local_filename)
    logging.debug("local: %s", local_filename)
    hostname, remote_path = get_top_dir(local_filename)
    logging.debug("hn: %s remote: %s", hostname, remote_path)
    local("scp %s:%s %s" % (hostname, remote_path, local_filename))
    with warn_only():
        local("git add %s" % local_filename)
        local("git commit -m 'Added %s from remote' %s" % (local_filename,
                                                           local_filename))


@begin.subcommand
def pull(local_filename):
    """Pulls the remote copy of LOCAL_FILENAME"""
    logging.debug("local: %s", local_filename)
    hostname, remote_path = get_top_dir(local_filename)
    logging.debug("hn: %s remote: %s", hostname, remote_path)
    local("git stash")
    local("scp %s:%s %s" % (hostname, remote_path, local_filename))
    with warn_only():
        local("git commit -m 'Pull from remote' %s" % local_filename)
        local("git stash pop")


@begin.subcommand
def vimdiff(local_filename):
    """Opens vimdiff on LOCAL_FILENAME and its remote counterpart"""
    hostname, remote_path = get_top_dir(local_filename)
    local("vimdiff %s scp://%s/%s" % (local_filename, hostname, remote_path))


@begin.start
@begin.logging
def run():
    """Fuggit: for when you want to put that file in git, but you can't be f

    You know the feeling. You're looking for a"""
    pass
