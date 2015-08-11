=====
Usage
=====

Derived Image
~~~~~~~~~~~~~

First usage scenario is when you build a derived image containing your
source (e.g. Ansible playbooks, etc.).  An example ``Dockerfile``::

    FROM gimoh/devops-utils

    ADD . /opt/app
    WORKDIR /opt/app

You may also want to add Ansible roles, or python modules, e.g.::

    FROM gimoh/devops-utils

    ADD reqs-*[lt] /opt/app/
    RUN ansible-galaxy install --role-file /opt/app/reqs-ansible.yml
    RUN pip install --requirement /opt/app/reqs-py.txt
    ADD . /opt/app
    WORKDIR /opt/app

Then to use::

    ansible-playbook -i hosts.ini your-playbook.yml
    # or
    fab -l

See also :ref:`usage-extending` which may be useful for derived images.


Development / Mounted Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second usage scenario is when you want to use your development
tree as source.  This may be done with either the original or derived
image::

    devops-utils ++dev ansible-playbook -i hosts.ini your-playbook.yml
    # or
    ansible-playbook ++dev -i hosts.ini your-playbook.yml

This will mount current working directory as ``/opt/app`` and set
``WORKDIR`` appropriately.

Notice that parameters to the runner itself start with ``+`` instead of
the usual ``-``, this is to make them easier to differentiate from
parameters to the program being run.


Running
~~~~~~~

You can use the image without installing the runner, but some features
will be unavailable (e.g. SSH agent socket, SSH key, SSH config).

The runner uses ``+`` as option prefix character to make it easier to
distinguish between options for the runner and options for the program
being run.  You can see usage help with::

    devops-utils ++help
    # likewise:
    fab ++help
    # will print the runner help message, vs
    fab --help
    # which will print Fabric's help message

The default options to ``docker run`` are: ``-i -t --rm``.

You can pass any docker option to ``docker run`` using the
``+O / ++docker-opt`` option::

    devops-utils +O privileged ++docker-opt net=host bash

As hinted above, ``++dev`` can be used to mount source in current
working directory in the container instead of using the one baked into
the image (required if not using a derived image).

When starting the container, the SSH agent socket will be passed in if
available, to enable SSH authentication using own keys.

Alternatively, you can use ``++key FILE`` option to pass a specific key
and it will be injected into the container as ``/root/.ssh/id_rsa`` at
runtime.

SSH config file ``~/.ssh/config`` is also injected into the container
if it exists so that any special configuration for particular hosts is
respected.

Finally, you can pass ``++debug`` option to see how options are
processed and how arguments to the programs are manipulated.

docker-machine
--------------

It is possible to run ``docker-machine`` commands within the image.
When using ``docker-machine``, it is important to pass the ``++dev``
option, otherwise any changes (like adding new machines) are lost.

``docker-machine`` saves configuration, like keys for servers, and
in fact the names of what servers are managed in a configuration
directory, in our image this defaults to ``/opt/app/.docker/machine``.

An example of using ``docker-machine`` is::

    devops-utils ++dev docker-machine upgrade fred

which would execute the ``docker-machine upgrade`` command on host
``fred``, with /opt/app mounted from current working directory.
Running the above command in your home directory would pick up any
previous ``docker-machine`` configuration, and would save anything
that you change for use at a later date.

.. _usage-extending:

Extending
~~~~~~~~~

Both the external runner and the init (startup) script can be extended
with plugins to support additional options and to modify the
environment and arguments of the utilities being run.

The plugins are simple Python files that will be executed in a context
containing mainly the decorators: :py:func:`devops_utils.init.initfunc`
for init plugins, and :py:func:`external_runner.argparse_builder` and
:py:func:`external_runner.docker_run_builder` for external runner.
They are used to mark functions to be executed at specific stages in
the startup process.

They should define functions decorated with the above with signatures
matching the ones described in API docs for each decorator.

See :ref:`api-modules` for details.

Once you have a plugin, in your derived image drop the files into
`/etc/devops-utils/init_plugins/` or
`/etc/devops-utils/runner_plugins/` directory for init or runner
respectively.
