#!/bin/bash
ip="10.120.115.52"
port="8080"

while getopts "p:h" opt; do
        case ${opt} in
                p)
                        port="${OPTARG}" ;;
                h)
                        echo "web start: ${0} -p PORT"
                        exit 0;;
        esac
done

python3 manage.py runserver ${ip}:${port}

