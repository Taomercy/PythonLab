#!/bin/bash

yum install docker-ce  -y
systemctl start docker && systemctl enable docker.service

touch /etc/docker/daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors":["https://t9wy9d0y.mirror.aliyuncs.com","https://registry.docker-cn.com"],
  "exec-opts": ["native.cgroupdriver=systemd"]
} 
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
systemctl status docker
