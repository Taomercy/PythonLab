#!/bin/bash
#sudo apt-get install dos2unix
#dos2unix $0

#install vim
vim --version > /dev/null
if [ $? == 127 ];then
    sudo apt-get remove vim-common
    sudo apt-get install vim
    echo "set nu" > ~/.vimrc
    echo "set ts=4" >> ~/.vimrc
    echo "set expandtab" >> ~/.vimrc
fi

#install git
git --version > /dev/null
if [ $? == 127 ];then
    sudo apt install git
fi

#install rar 
rar -v > /dev/null
if [ $? == 127 ];then
    sudo apt-get install rar
fi

