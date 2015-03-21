# devops-utils

Docker image containing a set of utilities handy in a devops style
environment.  Currently these include: [Ansible](http://www.ansible.com/),
[Fabric](http://www.fabfile.org/).


## Installation

The image can be run directly, but also contains an external runner
program that wraps the `docker run` invocation to expose the utilities
directly.  Running the image with `install` parameter and a host
directory mounted on `/target` will install the runner and appropriate
links:

    docker run -v $HOME/.local/bin:/target --rm gimoh/devops-utils install

Replace `$HOME/.local/bin` with a directory where you want to place the
runner.  The result will be along those lines:

    devops-utils
    ansible-galaxy -> devops-utils
    ansible-doc -> devops-utils
    ansible-vault -> devops-utils
    ansible-playbook -> devops-utils
    fab -> devops-utils
    ansible -> devops-utils


## Usage
