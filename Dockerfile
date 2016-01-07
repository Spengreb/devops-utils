# Copyright 2015 gimoh
#
# This file is part of devops-utils.
#
# devops-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# devops-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with devops-utils.  If not, see <http://www.gnu.org/licenses/>.

FROM ubuntu:14.04
MAINTAINER gimoh <gimoh@bitmessage.ch>

RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
        --no-install-recommends \
        git openssh-client python-pip python-yaml python-paramiko \
        python-keyczar rsync && \
    apt-get clean && rm -rf /var/lib/apt/lists
RUN pip install --upgrade pip

# docker and docker-machine installation
ADD ["https://get.docker.com/builds/Linux/x86_64/docker-latest", \
     "/usr/local/bin/docker"]
ADD ["https://github.com/docker/machine/releases/download/v0.5.5/docker-machine_linux-amd64", \
     "/usr/local/bin/docker-machine"]
RUN chmod +x /usr/local/bin/docker*
ENV MACHINE_STORAGE_PATH=/opt/app/.docker/machine

RUN pip install ansible docker-compose Fabric ipython konch ptpython
RUN mkdir /etc/ansible && \
    echo '[local]\nlocalhost  ansible_connection=local' > /etc/ansible/hosts

RUN install -d -o root -g root -m 700 /root/.ssh
RUN mkdir /etc/devops-utils
ADD . /opt/devops-utils
RUN cd /opt/devops-utils && pip install . && \
    cp -r init_plugins runner_plugins /etc/devops-utils/

WORKDIR /opt/devops-utils
ENTRYPOINT ["/usr/bin/ssh-agent", "/usr/local/bin/docker-init"]
