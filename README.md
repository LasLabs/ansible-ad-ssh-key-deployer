[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

Active Directory SSH Key Deployer
=================================

Deploys SSH public keys stored in AD to a slew of hosts.

This automation requires specific setup in your Active Directory environment,
as described in the following blog posts:

* [Storing SSH Keys in Active Directory for Easy Deployment](https://blog.laslabs.com/2016/08/storing-ssh-keys-in-active-directory/)
* [Managing SSH Keys Storedd in Active Directory](https://blog.laslabs.com/2017/04/managing-ssh-keys-stored-in-active-directory/)

Requirements
------------

There are no prerequisites.

Role Variables
--------------

* `ldap_server` - The FQDN of the AD DC server.
* `ldap_bind_dn` - The user to bind to the directory with.
* `ldap_bind_pw` - The password for the bind user.
* `ldap_user_base` - The top level DN of your AD where users are stored.
* `ldap_filter` - The filter to use to get only valid Linux users

Dependencies
------------

There are no dependencies.

Example Playbook
----------------

``` yaml
    ---
    - hosts: servers
      become: true
      roles:
         - { role: ssh-key-deployer,
             ldap_server: "ldap://ex-dc-prod-vmw-01.corp.example.com",
             ldap_bind_dn: svc.ro-bind@corp.example.com,
             ldap_bind_pw: somepasswd,
             ldap_user_base: "OU=Example,DC=corp,DC=example,DC=com",
             ldap_filter: (uidNumber=*) }
```

Credits
=======

Contributors
------------

-   Ted Salmon &lt;<tsalmon@laslabs.com>&gt;
-   Dave Lasley &lt;<dave@laslabs.com>&gt;

Maintainer
----------

[![LasLabs Inc.](https://laslabs.com/logo.png)](https://laslabs.com)

This module is maintained by [LasLabs Inc.](https://laslabs.com)

* https://github.com/LasLabs/ansible-ad-ssh-key-deployer
