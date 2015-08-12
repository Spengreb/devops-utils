.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Docker image containing a set of utilities handy in a devops style
environment.

Features
========

 - built in utilities:

   - Ansible_
   - Fabric_
   - docker-machine

 - external runner which wraps ``docker run`` to make it look like the
   utilities are installed on the host
 - extensible startup process allowing derived images to customise
   options and the runtime environment


.. _Ansible: http://www.ansible.com/
.. _Fabric: http://www.fabfile.org/
.. _docker-machine: http://www.docker.com

Contents:
=========

.. toctree::
   :maxdepth: 2

   installation
   usage
   api/modules

Feedback
========

If you have any suggestions or questions or encounter any errors or
problems with **devops-utils**, please let me know!  Open an Issue at
the GitHub http://github.com/gimoh/devops-utils main repository.
