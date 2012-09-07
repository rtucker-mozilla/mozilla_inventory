"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

test_yaml="""--- !ruby/object:Puppet::Node::Facts
  expiration: 2012-09-07 08:17:43.793806 -07:00
  name: fake-hostname2.vlan.dc.mozilla.com
  values: 
    memorytotal: &id001 3.74 GB
    hardwaremodel: &id002 x86_64
    kernelmajversion: "2.6"
    concat_basedir: /var/lib/puppet/concat
    processorcount: "2"
    ipaddress_lo: 127.0.0.1
    blocks_sda2: "41839616"
    memorysize: *id001
    uptime_hours: "1644"
    has_hp_array_controller: "false"
    partitions_sda: "sda1,sda2,sda3"
    sshdsakey: asdfasfasfasdfasdfasdfasdfasdfasfasdfsadfsdafsadfsadf
    sshrsakey: asdfasdfasdfasdfsadfasdadsfasdfaisdhfjkasdfhkjlasdhfkjla
    id: root
    serialnumber: VMware-99 99 99 99 99 99 99 99 99 99 99 99 99
    netmask_lo: 255.0.0.0
    netmask: 255.255.255.0
    processor0: Intel(R) Xeon(R) CPU           X5690  @ 3.47GHz
    physicalprocessorcount: "2"
    boardmanufacturer: Intel Corporation
    swapsize: 2.00 GB
    hostname: fake-hostname2
    macaddress: 00:50:56:B7:07:64
    kernelversion: 2.6.32
    fqdn: fake-hostname2.vlan.dc.mozilla.com
    clientcert: fake-hostname2.vlan.dc.mozilla.com
    ipaddress: 10.99.32.1
    iptables_version: 1.4.7
    augeasversion: 0.9.0
    !ruby/sym _timestamp: 2012-09-07 07:47:43.833130 -07:00
    memoryfree: 2.34 GB
    type: Other
    rubysitedir: /usr/lib/ruby/site_ruby/1.8
    datacenter: corp-phx1
    uptime_days: "68"
    netmask_eth0: 255.255.255.0
    path: /bin:/sbin:/usr/bin:/usr/sbin
    vmware_version: "5.0"
    timezone: PDT
    operatingsystem: RedHat
    swapfree: 1.97 GB
    blocks_sda1: "102400"
    facterversion: 1.6.11
    selinux: "false"
    puppetmaster: puppetmaster.fake.mozilla.com
    uptime: 68 days
    kernelrelease: 2.6.32-220.7.1.el6.x86_64
    productname: VMware Virtual Platform
    ipaddress_eth0: 10.99.32.3
    manufacturer: "VMware, Inc."
    hardwareisa: x86_64
    network_lo: 127.0.0.0
    is_virtual: "true"
    rubyversion: 1.8.7
    boardserialnumber: None
    blocks_sda3: "20971520"
    network_eth0: 10.99.32.0
    architecture: *id002
    ip6tables_version: 1.4.7
    ps: ps -ef
    puppet_vardir: /var/lib/puppet
    clientversion: &id003 2.7.19
    interfaces: "eth0,lo"
    puppetversion: *id003
    disks: sda
    blocks_sda: "62914560"
    boardproductname: 440BX Desktop Reference Platform
    processor1: Intel(R) Xeon(R) CPU           X5690  @ 3.47GHz
    osfamily: RedHat
    uniqueid: 140a1946
    root_home: /root
    operatingsystemrelease: "6.2"
    environment: production
    macaddress_eth0: 00:00:00:00:00:00
    kernel: Linux
    domain: vlan.dc.mozilla.com
    uptime_seconds: "5921778"
    needs_reboot_for_kernel: "false"
    virtual: vmware"""

class PageTests(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        self.url_prefix = '/en-US'
        self.index_url = "%s%s" % (
                self.url_prefix, reverse('puppet-collect-index'))
        self.client = Client()

    def test1_test_collector_page_loads_and_exists(self):
        self.assertTrue(self.index_url)
        resp = self.client.get(self.index_url)
        self.assertEqual(resp.status_code, 200)

    def test2_test_collector_accepts_post(self):
        data = {
                'fact': test_yaml
                }
        
        resp = self.client.post(self.index_url, data=data)
        self.assertEqual(resp.status_code, 200)

