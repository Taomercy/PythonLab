#!/usr/bin/env bash
compose_file="docker-compose-mysql.yml"
docker-compose -f ${compose_file} up -d