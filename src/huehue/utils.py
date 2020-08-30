import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)