#!/bin/bash

function pip_install_model(){
    model_name=$1
    package_name=$2
    if [ -z $package_name ];then
        package_name=$model_name
    fi
    python -c "import $model_name" 2>/dev/null
    if [ $? != 0 ];then
        sudo pip install $package_name
    fi
    if [ $? != 0 ];then exit $?;fi
}

function apt_install_model(){
    model_name=$1
    package_name=$2
    if [ -z $package_name ];then
        package_name=$model_name
    fi
    python -c "import $model_name" 2>/dev/null
    if [ $? != 0 ];then
        sudo apt-get install $package_name -y
    fi
    if [ $? != 0 ];then exit $?;fi
}

python --version
if [ $? != 0 ];then exit 0; fi

pip --version  1>/dev/null
if [ $? == 127 ];then
    sudo apt-get install python-pip python-dev build-essential -y
    sudo apt-get install uwsgi uwsgi-plugin-python -y
    sudo apt-get install uwsgi-plugin-python3 -y
    sudo pip install --upgrade pip
fi
if [ $? != 0 ];then exit $?;fi

#model common
pip_install_model pandas
pip_install_model requests

#model data processing
pip_install_model numpy
pip_install_model scipy
pip_install_model matplotlib
pip_install_model sympy
pip_install_model sklearn

#model image processing
apt_install_model Image python-imaging
apt_install_model Tkinter python-tk

#model yaml
apt_install_model yaml python-yaml
pip_install_model ruamel.yaml

#model excel
pip_install_model xlrd
pip_install_model xlwt

#model mysql
pip_install_model MySQLdb MySQL-python
