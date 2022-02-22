#!/bin/bash
#
# Use this script to tail a log file and summarise errors out to a log buffer file.
# Usage:
# taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance identifier>
#
DEFINSTANCE=$$
if [ "$1" == "" ]
then
 echo "No monitor file specified to monitor"
 echo "taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance ID>"
 exit 98
fi
if [ "$2" == "" ]
then
 echo "No include file specified to include"
 echo "taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance ID>"
 exit 98
fi
if [ "$3" == "" ]
then
 echo "No skip file specified to exclude patterns"
 echo "taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance ID>"
 exit 97
fi
if [ "$4" == "" ]
then
 echo "No buffer file specified to write to"
 echo "taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance ID>"
 exit 97
fi
if [ "$5" == "" ]
then
 echo "no instance ID specified"
 echo "taillog.sh <target log file for monitoring> <include pattern file> <skip pattern file> <log buffer file> <instance ID>"
 exit 97
fi
export MONLOGFILE=$1
export INCLOGFILE=$2
export SKPLOGFILE=$3
export BUFLOGFILE=$4
export INSTANCE=$5
if [[ ! -e $MONLOGFILE ]]
then
 echo "Monitored File does not exist"
 exit 2
else
 FSTOP=$(wc -l ${MONLOGFILE} |cut -d' ' -f1)
fi
if [[ ! -e $INCLOGFILE ]]
then
  echo "Include file does not exist"
  exit 2
fi
if [[ ! -e $SKPLOGFILE ]]
then
   echo "Exclude file does not exist"
   exit 2
fi
if [[ -e /tmp/taillogrunning_${INSTANCE} ]]
then
 INSTPID=`cat /tmp/taillogrunning_${INSTANCE}`
 if [[ $(ps -ef |grep ${INSTPID}|grep taillog|grep $INSTANCE| wc -l) -gt 0 ]]
 then
  echo "Script is already running"
  exit 99
 else
  touch /tmp/taillogrunning_${INSTANCE}
  echo $DEFINSTANCE>/tmp/taillogrunning_${INSTANCE}
  let FSTART=FSTOP+1
  tail -n +$FSTART -f $MONLOGFILE|egrep --line-buffered -f $INCLOGFILE |egrep --line-buffered -v -f $SKPLOGFILE |awk '{print ENVIRON["INSTANCE"]"|"strftime("%Y-%m-%d %H:%M:%S")"|"$0; fflush()}'|tee $BUFLOGFILE 2>&1
 fi
else
 touch /tmp/taillogrunning_${INSTANCE}
 echo $DEFINSTANCE >/tmp/taillogrunning_${INSTANCE}
 touch $BUFLOGFILE
 let FSTART=FSTOP+1
 tail -n +$FSTART -f $MONLOGFILE|egrep --line-buffered -f $INCLOGFILE |egrep --line-buffered -v -f $SKPLOGFILE |awk '{print ENVIRON["INSTANCE"]"|"strftime("%Y-%m-%d %H:%M:%S")"|"$0; fflush()}'|tee $BUFLOGFILE 2>&1
fi


