# -*- coding: utf-8 -*-
"""
minipylib.server.utils

Helpers functions for the server module.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-29 kchan
"""

from __future__ import (absolute_import, unicode_literals)


#######################################################################
# utility functions
# * adapted from django-cerise and django-cpserver
# ** http://xhtml.net/scripts/Django-CherryPy-server-DjangoCerise
# ** http://github.com/lincolnloop/django-cpserver
#######################################################################

def get_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    :Source: `http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/ <http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/>`_
    """
    import pwd, grp
    uid, default_grp = pwd.getpwnam(uid)[2:4]
    if gid is None:
        gid = default_grp
    else:
        try:
            gid = grp.getgrnam(gid)[2]
        except KeyError:
            gid = default_grp
    return (uid, gid)


def change_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    :Source: `http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/ <http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/>`_
    """
    import os
    if not os.geteuid() == 0:
        # Do not try to change the gid/uid if not root.
        return
    (uid, gid) = get_uid_gid(uid, gid)
    os.setgid(gid)
    os.setuid(uid)
