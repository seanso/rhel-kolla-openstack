
# Openstack-Kolla-for-RHEL

## Getting Started 

### Before you run this build you should start with the following steps.  

* Make sure your machine have enough storage, at least 20Gb in /var (depends on how much containers you create) and 4Gb in /usr.

* Attach the right pool (you can use any pool that contains all of the repos from the next command) 

```
     subscription-manager attach --pool=8a85f98a61b259620161debd54665adb
```

* Enable the following repositories on your machine:  

```
subscription-manager repos --enable=rhel-7-server-rhceph-3-osd-rpms --enable=rhel-7-server-rhceph-3-mon-rpms --enable=rhel-7-server-rhceph-3-tools-rpms --enable=rhel-7-server-rpms --enable=rhel-7-server-openstack-13-rpms --enable=rhel-7-server-openstack-13-optools-rpms --enable=rhel-7-server-openstack-13-tools-rpms --enable=rhel-7-server-extras-rpms --enable=rhel-server-rhscl-7-rpms
```

* Install the necessary packages:
```
    $ yum install  python27-python-devel git gcc -y 
    $ yum install python27-python-pip -y
    $ scl enable python27 bash
    $ pip install --upgrade pip
    $ pip install tox
```
**If you're working with this repository(not making the changes yourself) clone this repo and skip to the Final section.**
     * Clone this repository:
```
     git clone https://github.com/seanso/rhel-kolla-openstack.git
```
----

## Fixing Openstack Kolla repository to work with RHEL images
* Clone kolla-openstack queens release repository:
```
git clone https://github.com/openstack/kolla.git --branch stable/queens
cd openstack-kolla-for-rhel/
```

### Fix Bugs
* **Bug fix /root/kolla/kolla/image/build.py**
``` diff
                image.status = STATUS_MATCHED

        skipped_images = SKIPPED_IMAGES.get('%s+%s' % (self.base,
                                                       self.install_type))
+        if skipped_images:
            for image in self.images:
                if image.name in skipped_images:
                    image.status = STATUS_UNMATCHED
```

### DockerFiles fix
We've included some changes in several docker files, each and everyone of the changes is written in the directory 'changes'([Go to changes here](changes)), Most of the changes are yum packages that do not exist for rhel, so you need to create a separated if condition for rhel and put there only the packages that exist. 
Here is an example of the changes we've made for 'neutron-server' Dockerfile:

* **docker/neutron/neutron-server/Dockerfile.j2**

Seperate rhel from Oracleinux and Centos because some packages have different names or do not exist at all.

```diff --git a/docker/neutron/neutron-server/Dockerfile.j2 b/docker/neutron/neutron-server/Dockerfile.j2
index 9694778..302b431 100644
a/docker/neutron/neutron-server/Dockerfile.j2
@@ -6,7 +6,13 @@ LABEL maintainer="{{ maintainer }}" name="{{ image_name }}" build-date="{{ build
 {% import "macros.j2" as macros with context %}
 
 {% if install_type == 'binary' %}
-    {% if base_distro in ['centos', 'oraclelinux', 'rhel'] %}
+    {% if base_distro in ['rhel'] %}
+
+        {% set neutron_server_packages = [
+            'openstack-neutron-lbaas',
+        ] %}
+
+    {% elif base_distro in ['centos', 'oraclelinux'] %}
 
         {% set neutron_server_packages = [
             'openstack-neutron-lbaas',
```

The DockerFiles we've changed:
- horizon
- kolla-toolbok
- neutron-base
- neutron-l3-agent
- neutron-server
- openstack-base

## Final

* Genrate config file
```
cd prod-kolla/
tox -e genconfig
```

* Install pip requirements
```
pip install -r requirements.txt
```

* Install and start Docker
```
yum install docker 
systemctl start docker
```

## Run the build command
```
python kolla/cmd/build.py nova glance horizon keystone neutron cinder heat barbican octavia keepalived kolla-toolbox haproxy cron chrony mariadb memcached rabbitmq openvswitch openvswitch-db-server openvswitch-vswitchd --base-arch x86_64 --base-image registry.access.redhat.com/rhel7 --base-tag 7.6 --type binary --tag 6.1.1 --threads 16  --base rhel
```
**In this build 2 images(neutron-bgp-dragent, nova-mksproxy) will fail because there are missing packages for RHEL.**

