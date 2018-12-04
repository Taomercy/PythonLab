#!/bin/bash

function pip_install_model(){
    model_name=$1
    package_name=$2
    if [ -z $package_name ];then
        package_name=$model_name
    fi
    python -c "import $model_name"
    if [ $? != 0 ];then
        sudo pip install $package_name
    fi
}

function apt_install_model(){
    model_name=$1
    package_name=$2
    if [ -z $package_name ];then
        package_name=$model_name
    fi
    python -c "import $model_name"
    if [ $? != 0 ];then
        sudo apt-get install $package_name
    fi
}

python --version
if [ $? != 0 ];then exit 0; fi

pip --version > /dev/null
if [ $? == 127 ];then
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
fi

#model common
pip_install_model pandas
pip_install_model requests

#model about data processing
pip_install_model numpy
pip_install_model scipy
pip_install_model matplotlib
pip_install_model sympy
pip_install_model sklearn


apt_install_model Image python-imaging
apt_install_model yaml python-yaml
pip_install_model ruamel.yaml
apt_install_model Tkinter python-tk

#model about excel
pip_install_model xlrd
pip_install_model xlwt

