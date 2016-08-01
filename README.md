.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Active Directory SSH Key Deployer
=================================

Deploys SSH public keys stored in AD to a slew of hosts

Requirements
------------

There are no prerequisites.

Role Variables
--------------
ldap_server - The FQDN of the AD DC server.
ldap_bind_dn - The user to bind to the directory with.
ldap_bind_pw - The password for the bind user.
ldap_user_base - The top level DN of your AD where users are stored.
ldap_filter - The filter to use to get only valid Linux users

Dependencies
------------

There are no dependencies.

Example Playbook
----------------
```
    - hosts: servers
      roles:
         - { role: ssh-key-deployer,
             ldap_server: ex-dc-prod-vmw-01.corp.example.com,
             ldap_bind_dn: svc.ro-bind@corp.example.com,
             ldap_bind_pw: somepasswd,
             ldap_user_base: OU=Example,DC=corp,DC=example,DC=com,
             ldap_filter: (uidNumber=*) }
```

License
=======

AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

Images
------

* LasLabs: `Icon <https://repo.laslabs.com/projects/TEM/repos/odoo-module_template/browse/module_name/static/description/icon.svg?raw>`_.

Contributors
------------

* Ted Salmon <tsalmon@laslabs.com> LasLabs, Inc.

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.