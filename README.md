# devops-utils

Docker image containing a set of utilities handy in a devops style
environment.


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

See also [extending](#extending) which may be useful for derived
images.


### Development / Mounted Source

The second usage scenario is when you want to use your development
tree as source.  This may be done with either the original or derived
image:

    devops-utils ++dev ansible-playbook -i hosts.ini your-playbook.yml
    # or
    ansible-playbook ++dev -i hosts.ini your-playbook.yml

Notice that parameters to the runner itself start with `+` instead of
the usual `-`, this is to make them easier to differentiate from
parameters to the program being run.


### Running

You can use the image without installing the runner, but some features
will be unavailable (e.g. SSH agent socket,

The runner uses `+` as option prefix character to make it easier to
distinguish between options for the runner and options for the program
being run.  You can see usage help with:

    devops-utils ++help
    # likewise:
    fab ++help
    # will print the runner help message, vs
    fab --help
    # which will print Fabric's help message

The default options to `docker run` are: `-i -t --rm`.

You can pass any docker option to `docker run` using the
`+O / ++docker-opt` option:

    devops-utils +O privileged ++docker-opt net=host bash

As hinted above, `++dev` can be used to mount source in current working
directory in the container instead of using the one baked into the
image (required if not using a derived image).

When starting the container, the SSH agent socket will be passed in if
available, to enable SSH authentication using own keys.

Alternatively, you can use `++key FILE` option to pass a specific key
and it will be injected into the container as `/root/.ssh/id_rsa` at
runtime.

SSH config file `~/.ssh/config` is also injected into the container if
it exists so that any special configuration for particular hosts is
respected.

Finally, you can pass `++debug` option to see how options are processed
and how arguments to the programs are manipulated.


### Extending

Both the external runner and the init (startup) script can be extended
with plugins to support additional options and to modify the
environment and arguments of the utilities being run.

The plugins are simple Python files that will be executed in a context
containing mainly the decorators: `initfunc` for init plugins, and
`argparse_builder` and `docker_run_builder` for external runner.  They
are used to mark functions to be executed at specific stages in the
startup process.

<!---
@todo: link to API docs
should define ...
-->

Once you have a plugin, in your derived image drop the files into
`/etc/devops-utils/init_plugins/` or
`/etc/devops-utils/runner_plugins/` directory for init or runner
respectively.
