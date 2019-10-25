#!/bin/bash

if [ "x$1" == "x" ]
then
  echo "usage:"
  echo "   $0 [check|execute] <prefix>.txt"
  exit 0
fi

case $1 in
  check )
    echo "Check only, do not apply changes!"
    ;;
  execute )
    echo "Executing 'chgrp' on $2.txt"
    ;;
  * )
    echo "Unknown command $1"
    echo "Acceptable options: check execute"
    exit 0
    ;;
esac

if [ ! -f $2.txt ]
then
  echo "usage:"
  echo "   $0 [check|execute] <prefix>.txt"
  echo "filelist $2.txt is missing!"
  exit 0
fi

if [ -f $2.out ] || [ -f $2.err ]
then
  echo "Have you ran this before?"
  echo "Move $2.out &/or $2.err out of the way and try again"
fi

while IFS= read -r line
do
  GRP=`echo $line | awk -F \/ '{print $3}'`
  VALID="1"
  getent group ${GRP} > /dev/null 2>&1 || echo VALID="0"
  if [ $VALID == "1" ]
  then
    chgrp -vh ${GRP} "$line" >> $2.out 2>> $2.err
  else
    echo "Invalid group ${GRP} on $line" 2>> $2.err
  fi
done < $2.txt

exit 0
