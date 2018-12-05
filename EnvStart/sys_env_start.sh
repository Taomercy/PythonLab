#!/bin/bash
#sudo apt-get install dos2unix
#dos2unix $0

#install vim
vim --help 1>/dev/null 2>/dev/null
if [ $? == 127 ];then
    sudo apt-get remove vim-common -y
    sudo apt-get install vim -y
    echo "set nu" > ~/.vimrc
    echo "set ts=4" >> ~/.vimrc
    echo "set expandtab" >> ~/.vimrc
fi
if [ $? != 0 ];then exit $?;fi

#install git
git --help 1>/dev/null 2>/dev/null
if [ $? == 127 ];then
    sudo apt install git -y
fi
if [ $? != 0 ];then exit $?;fi

#install curl
curl --help 1>/dev/null 2>/dev/null
if [ $? == 127 ];then
    sudo apt install curl -y
fi
if [ $? != 0 ];then exit $?;fi

#install rar 
rar -v 1>/dev/null 2>/dev/null
if [ $? == 127 ];then
    sudo apt-get install rar -y
fi
if [ $? != 0 ];then exit $?;fi

#install tmux
tmux -h 2>/dev/null
if [ $? == 127 ];then
    sudo apt-get install tmux -y
fi
if [ $? != 0 ];then exit $?;fi

#install mysql
#tips:when installing need config root password
mysql 2>/dev/null
if [ $? == 127 ];then
    sudo apt-get install mysql-server -y
    sudo apt-get isntall mysql-client -y
    sudo apt-get install libmysqlclient-dev -y
    sudo netstat -tap | grep mysql
    sed 's/^bind-address/#&/g' /etc/mysql/mysql.conf.d/mysqld.cnf
    #then config your account into mysql by the command "mysql -u root -p"
    #input your root password
    #input the command in mysql
    #>>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'your password' WITH GRANT OPTION;
    #>>flush privileges;
    #exit
    #service mysql restart
fi
if [ $? != 0 ];then exit $?;fi

sudo apt-get upgrade -y
#sudo reboot
