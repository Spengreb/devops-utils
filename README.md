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

By default the runner will invoke `docker run` with `gimoh/devops-utils`
image, if you want to use another name, e.g. when working with a derived
image, you can override it:

    docker run -v $HOME/.local/bin:/target --rm gimoh/devops-utils \
      install --image-name=$USER/devops-utils


## Usage

### Derived Image

First usage scenario is when you build a derived image containing your
source (e.g. Ansible playbooks, etc.).  An example `Dockerfile`:

    FROM gimoh/devops-utils

    ADD . /opt/app
    WORKDIR /opt/app

You may also want to add Ansible roles, or python modules, e.g.:

    FROM gimoh/devops-utils

    ADD reqs-*[lt] /opt/app/
    RUN ansible-galaxy install --role-file /opt/app/reqs-ansible.yml
    RUN pip install --requirement /opt/app/reqs-py.txt
    ADD . /opt/app
    WORKDIR /opt/app

Then to use:

    ansible-playbook -i hosts.ini your-playbook.yml
    # or
    fab -l
