#!/bin/bash
user=`whoami`
container_name="${user}_server_verify"
code_path=`pwd`
image=`docker images | grep "hwwuex_check_server" | awk '{print $3}'`
delete="False"

while getopts "dh" opt; do
    case ${opt} in
        d)
            delete="True" ;;
        h)
            echo "delete container: ${0} -d"
            exit 0;;
    esac
done

function create_container(){
    echo "Go to new container ==>"
    docker run -it --network=host --name ${container_name} --env PYTHONPATH=:/home -v ${code_path}:/home/logging_enhancement -v /hcs:/hcs -w /home/logging_enhancement ${image} /bin/bash
}

function delete_container(){
    container_id=`docker ps -a | grep "${container_name}" | awk '{print $1}'`
    docker rm -f ${container_id} > /dev/null
    echo "The old container has been deleted!"
    echo "Clean up unused image..."
    docker image prune -a -f > /dev/null
}

if [[ ${delete} == "True" ]];then
    delete_container
    exit 0
fi

container_id=`docker ps -a | grep "${container_name}" | awk '{print $1}'`
if [[ -z ${container_id} ]];then
    create_container
else
    docker exec -it ${container_id} /bin/bash
    if [[ $? != 0 ]];then
        delete_container
        create_container
    else
        exit 0
    fi
fi
