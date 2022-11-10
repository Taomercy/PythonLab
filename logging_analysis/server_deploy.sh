#!/bin/bash
compose_file="docker-compose-server.yml"

project_path=${1}
if [[ -z "${project_path}" ]]; then
	project_path=`pwd`
fi	
container_id=`docker ps -a | grep "hc_server" | awk '{print $1}'`

pushd ${project_path}
    docker-compose -f ${compose_file} down
    image_id=`docker images | grep "hwwuex_check_server" | awk '{print $3}'`
    if [[ ! -z ${image_id} ]];then
        docker rmi ${image_id}
    fi
    git pull
    if [[ $? != 0 ]];then
        exit 0
    fi	
    docker-compose -f ${compose_file} build
    docker-compose -f ${compose_file} up -d
popd

# remove container image
docker container prune -f
docker image prune -a -f
