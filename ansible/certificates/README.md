# Certificates
Your Greengrass certificates should be placed in this directory for
automatic deployment via Ansible.

ZIP the certificates as follows, assuming the RPI target hostname is 'energy-monitor'.

```
energy-monitor.zip
    - energy-monitor.private.key
    - energy-monitor.cert.pem
```

These will then be deployed within the `greengrass-certificates` ansible role.