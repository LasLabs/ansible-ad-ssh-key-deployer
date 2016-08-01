#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
import base64
from contextlib import contextmanager
import ldap
import subprocess
import os
from shutil import copytree

SERVER = '{{ ldap_server }}'
BIND_USER = '{{ ldap_bind_dn }}'
BIND_PW = '{{ ldap_bind_pw }}'
BASE = '{{ ldap_user_base }}'
FILTER = '{{ ldap_filter }}'
ATTRS = ('sshPublicKeys', 'sAMAccountName', 'uidNumber', 'gidNumber')
RESULTS = []


def get_ip_addresses():
    ip_addrs = []
    result = subprocess.check_output(
        "ip addr | grep inet | awk '{print $2}'", shell=True)
    for line in result.split('\n'):
        ip_parts = line.split('/')  # Remove CIDR
        ip_addrs.append(ip_parts[0])
    return ip_addrs


@contextmanager
def ldap_initialize(uri):
    conn = ldap.initialize(uri)
    yield conn
    conn.unbind()


with ldap_initialize(SERVER) as ldap_conn:
    ldap_conn.set_option(ldap.OPT_REFERRALS, 0)
    ldap_conn.simple_bind_s(BIND_USER, BIND_PW)
    r = ldap_conn.search_s(BASE, ldap.SCOPE_SUBTREE, FILTER, ATTRS)
    RESULTS = [entry for dn, entry in r if isinstance(entry, dict)]

machine_ips = get_ip_addresses()
for user in RESULTS:
    ssh_keys = user.get('sshPublicKeys')
    if ssh_keys:
        machine_keys = []
        homedir = '/home/%s' % user['sAMAccountName'][0]
        auth_key_file = '%s/.ssh/authorized_keys' % homedir
        uid = int(user['uidNumber'][0])
        gid = int(user['gidNumber'][0])

        if not os.path.exists(homedir):
            copytree('/etc/skel', homedir)
            os.chown(homedir, uid, gid)

        if not os.path.exists('%s/.ssh' % homedir):
            os.mkdir('%s/.ssh' % homedir, 0700)

        for d in os.listdir(homedir):
           os.chown('%s/%s' % (homedir, d), uid, gid)
        
        # Find the keys for this machine or the master key
        for data in ssh_keys:
            ip_addr, key = data.split(':')
            if ip_addr == '*' or ip_addr in machine_ips:
                machine_keys.append(key)

        # Write out the authorized keys file if it doesn't exist
        if not os.path.exists(auth_key_file):
            with open(auth_key_file, 'a') as fh:
                fh.writelines(machine_keys)
            os.chown(auth_key_file, uid, gid)