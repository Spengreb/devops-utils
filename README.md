[![Build Status](https://travis-ci.org/gimoh/devops-utils.svg?branch=master)](https://travis-ci.org/gimoh/devops-utils) [![Coverage Status](https://coveralls.io/repos/gimoh/devops-utils/badge.svg?branch=master)](https://coveralls.io/r/gimoh/devops-utils?branch=master) [![Documentation Status](https://readthedocs.org/projects/devops-utils/badge/?version=latest)](https://readthedocs.org/projects/devops-utils/?badge=latest)

# devops-utils

Docker image containing a set of utilities handy in a devops style
environment.

Full documentation can be found on [RTFD](http://devops-utils.rtfd.org/).


## Features

 - built in utilities:
   - [Ansible](http://www.ansible.com/)
   - [Fabric](http://www.fabfile.org/)
 - external runner which wraps `docker run` to make it look like the
   utilities are installed on the host
 - extensible startup process allowing derived images to customise
   options and the runtime environment


## Installation

The image can be run directly, but also contains an external runner
program that wraps the `docker run` invocation to expose the utilities
directly.  Running the image with `install` parameter and a host
directory mounted on `/target` will install the runner and appropriate
links:

    docker run -v $HOME/.local/bin:/target --rm gimoh/devops-utils install

Replace `$HOME/.local/bin` with a directory where you want to place the
runner.

See [docs](http://devops-utils.rtfd.org/en/latest/installation.html)
for more details.


## Usage

First usage scenario is when you build a derived image containing your
source (e.g. Ansible playbooks, etc.).  An example `Dockerfile`:

    FROM gimoh/devops-utils

    ADD . /opt/app
    WORKDIR /opt/app

The second usage scenario is when you want to use your development
tree as source.  This may be done with either the original or derived
image:

    devops-utils ++dev ansible-playbook -i hosts.ini your-playbook.yml
    # or
    ansible-playbook ++dev -i hosts.ini your-playbook.yml

Check all available runner options with:

    devops-utils ++help

When using a derived image, the options, environment and startup
process can be customised.

See [docs](http://devops-utils.rtfd.org/en/latest/usage.html) for more
details.
