###############
**
  This is a brief explaination for 
  how to test your code via docker container
  how to deploy new docker container
**
###############



1. Use container_start_test.sh
   
   This script used for a local testing with client and server.

   1.1 bash container_start_test.sh or ./container_start_test.sh
  
   1.2 root@seliius27524:/# cd /home

   1.3 root@seliius27524:/home# ls
       hwwuex_check  logging_enhancement  server
      
       (PLease double check here the "logging_enhancement" is mount to your local path folder.)

   1.4 root@seliius27524:/home# cd logging_enhancement/

   1.5 Start server

       root@seliius27524:/home/logging_enhancement# python3 application/server/server.py -p 5008
       2021-06-29 08:07:01,666 DEBUG [server.py <module> 66 139900374095680]: server start.

           
       (YOu can indicate the port with -p for any value inner limitation)

   1.6 Start client

       Open another timinal and login in the TG, the port should be align with the server
       ehaiwsn@seliius27524[10:09][/home/ehaiwsn]$ client -p 5008
       please input HELP to get usage
       > 

   1.7 Your changes in server will be update here:
       > help
       ================Help Information================
          stability_check $path all,applog,memory
          upgrade_check
          case_path_list
          properties save_properties rm_properties
       ================================================
       >

  1.8 Ater testing remove the container
      docker rm container_id
      or 
      bash container_start_test.sh -d
  

2. How to deploy new docker server
   
   2.1 Make sure your code has been megred
   
   2.2 Start deploy script
        cd /home/ehaiwsn/4g_work/logging_enhancement/
       ./server_deploy.sh



3. How to connect mysql
   cmd: mysql -h 10.120.115.52 -u root -p hc_db
   password: admin123
   backup:
   script /var/backups/mysql_backup.sh will be run once a week
   backup_path: /var/backups/mysql

4. Replace LR to CRLF
   cmd: ls -l | grep ^-*.*.sh | awk '{print $9}' | xargs sed -i 's/\r//g'
