#!/bin/bash
#sudo apt-get install dos2unix
#dos2unix $0
sudo apt-get autoremove open-vm-tools -y
sudo apt-get install open-vm-tools-desktop -y

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

sudo apt install expect

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

#install python3.7.4
sudo apt-get install -y zlib*
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
tar -zcvf Python-3.7.4.tgz
mkdir -p /usr/local/python3
pushd Python-3.7.4
./configure  --with-ssl --prefix=/usr/local/python3
make && make install
popd
rm -rf Python-3.7.4


sudo apt-get install python-pip python-dev build-essential -y
sudo pip install --upgrade pip
sudo apt-get install libsasl2-dev -y
sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev libldap2-dev -y
sudo apt-get install uwsgi-uwsgi-plugin-python -y
sudo apt-get install uwsgi-plugin-python3 -y



sudo apt-get upgrade -y
#sudo reboot
