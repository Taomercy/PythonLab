#!/bin/bash
container_id=`docker ps -a | grep "hwwuex_check_web" | awk '{print $1}'`
docker exec -it ${container_id} /bin/bash
