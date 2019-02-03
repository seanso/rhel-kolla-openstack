
# Openstack-Kolla-for-RHEL

## Getting Started 

Before you run this build you should start with the following steps.  

* Make sure your machine have enough storage, at least 20Gb in /var (depends on how much containers you create) and 4Gb in /usr.

* Attach the right pool (you can use any pool that contains all of the repos from the next command) 

```
     subscription-manager attach --pool=8a85f98a61b259620161debd54665adb
```

* Enable the repositorys on your machine:  

```
subscription-manager repos --enable=rhel-7-server-rhceph-3-osd-rpms --enable=rhel-7-server-rhceph-3-mon-rpms --enable=rhel-7-server-rhceph-3-tools-rpms --enable=rhel-7-server-rpms --enable=rhel-7-server-openstack-13-rpms --enable=rhel-7-server-openstack-13-optools-rpms --enable=rhel-7-server-openstack-13-tools-rpms --enable=rhel-7-server-extras-rpms
```

* Install the necessary packages:
```
    $ yum install  python-devel git gcc -y 
    $ yum install python-pip -y # choose your repo of choice to get pip installed 
    $ pip install -U pip
    $ pip install tox
```
!!! If you working with this repository skip to the Work with this repository section.

* Clone koll-openstack queens release repository:
```
git clone https://github.com/openstack/kolla.git --branch stable/queens
```
## Change the files

### bug fix /root/kolla/kolla/image/build.py
``` diff
                image.status = STATUS_MATCHED

        skipped_images = SKIPPED_IMAGES.get('%s+%s' % (self.base,
                                                       self.install_type))
+        if skipped_images:
            for image in self.images:
                if image.name in skipped_images:
                    image.status = STATUS_UNMATCHED
```

### Change the DockerFiles
We've included some changes in several docker files, each and everyone of the changes is written in the directory 'changes', here is an example in the neutron-server Dockerfile:

### docker/neutron/neutron-server/Dockerfile.j2

Again had to seperate rhel from oraclelinux and centos because some packages have diffrante names or does not exists

```diff --git a/docker/neutron/neutron-server/Dockerfile.j2 b/docker/neutron/neutron-server/Dockerfile.j2
index 9694778..302b431 100644
--- a/docker/neutron/neutron-server/Dockerfile.j2
+++ b/docker/neutron/neutron-server/Dockerfile.j2
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

