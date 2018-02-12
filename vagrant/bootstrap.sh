#!/bin/bash

apt-get update
apt-get install -y docker docker-compose

systemctl enable docker
