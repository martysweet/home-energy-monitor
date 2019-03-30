# Certificates
Your Greengrass certificates should be placed in this directory for
automatic deployment via Ansible.

Add the files you downloaded from the AWS IoT console, using their normal file name, for example:

- 75e4768f1d-certificate.pem.crt
- 75e4768f1d-private.pem.key

These will then be deployed within the `greengrass-certificates` ansible role.