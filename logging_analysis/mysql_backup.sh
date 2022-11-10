#!/bin/bash
# docker exec ${container_name} ${mysql_cmd} -u${user} -p${passsword} ${database_name} >/< ${sql_file}
# backup cmd: docker exec hc_db mysqldump -uroot -padmin123 hc_db > backup.sql
# restore cmd: docker exec hc_db mysql -uroot -padmin123 hc_db < backup.sql
backup_path=${HOME}
mysqldump_date=`date +%Y%m%d_%H%M%S`
docker exec hc_db mysqldump -uroot -padmin123 hc_db > ${backup_path}/${mysqldump_date}.sql

