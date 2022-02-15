taillog
=======

* The taillog.sh script can be used to continuously monitor a text log file including/excluding text patterns of your choice. The eligible output is written to a specified file.

* An instance identifier is specifed to allow multiple instances of taillog.sh to run concurrently and hence multiple files to be monitored.

* Can be started via cron - if you put an entry to started every minutes it will check to see if it is already running and if so will exit.

Usage:

./taillog.sh \<target file for monitoring\> \<includefile\> \<excludefile\> \<target outputfile\> \<instance identifier\>

e.g. to monitor an oracle alert log

./taillog.sh /u01/app/oracle/diag/rdbms/mydb/MYDB/trace/alert_MYDB.log /home/oracle/scripts/monitoring/includefile /home/oracle/scripts/monitoring/skipfile /tmp/log.out oracleAlertLog

If the include file has the pattern ^ORA- the output captured to the target file will be like the following:

oracleAlertLog|2022-02-14 15:43:20|ORA-1654: unable to extend index PROD_REPO.STEP_FK1 by 128 in tablespace PROD_USER
oracleAlertLog|2022-02-14 15:44:20|ORA-1654: unable to extend index PROD_REPO.STEP_FK1 by 128 in tablespace PROD_USER
