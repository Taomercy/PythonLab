#!/bin/bash
compose_file="docker-compose-web.yml"
project_path=${HOME}/logging_enhancement/
container_id=`docker ps -a | grep "hc_web" | awk '{print $1}'`

pushd ${project_path}
    docker-compose -f ${compose_file} down
    image_id=`docker images | grep "hwwuex_check_web" | awk '{print $3}'`
        if [[ ! -z ${image_id} ]];then
        docker rmi ${image_id}
    fi
    #git reset --hard HEAD^ && git clean -xdf && git pull
    docker-compose -f ${compose_file} build
    docker-compose -f ${compose_file} up -d
popd

# remove image
# y|docker system prune
