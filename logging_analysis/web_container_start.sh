#!/bin/bash
user=`whoami`
container_name="${user}_web_verify"
code_path=`pwd`
image=`docker images | grep "hwwuex_check_web" | awk '{print $3}'`
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
	docker run -it --network=host --name ${container_name} --env PYTHONPATH=:/home -v ${code_path}:/home/logging_enhancement -v /hcs:/hcs -w /home/logging_enhancement/Web ${image} /bin/bash
}

if [[ ${delete} == "True" ]];then
	container_id=`docker ps -a | grep "${container_name}" | awk '{print $1}'`
	docker rm -f ${container_id}
	echo "container deleted"
	exit 0
fi

container_id=`docker ps -a | grep "${container_name}" | awk '{print $1}'`
if [[ -z ${container_id} ]];then
    create_container
else
	docker exec -it ${container_id} /bin/bash
	if [[ $? != 0 ]];then
		docker rm -f ${container_id}
		echo "delete container and create new one!"
		create_container
	fi
fi
