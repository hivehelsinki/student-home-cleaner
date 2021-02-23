#!/bin/zsh

# __author__  = 42 (42.fr)

if [ "$#" -ne 2 ]
then
	echo "Usage: $0 HOMEPATH LOGIN" >&2
	exit 1
fi

LOGIN=$2
LOGIN_DT=$(echo $LOGIN | sed 's/-/--/g')
BASEIQN="iqn.2016-08.fr.42.homedirs"
IQN="$BASEIQN:$LOGIN"
IETCONF="/etc/iet/ietd.conf"
IETCONFDIR="/etc/iet/homeconfs"
HOMEPATH=$1

IMG=`find $HOMEPATH -name "$LOGIN.img"`

grep -A 2 $IQN /proc/net/iet/session | grep -q 'ip:'

if [ $? -eq 0 ]
then
	IP=`grep -A 2 $IQN /proc/net/iet/session | grep 'ip:' | awk -F'[ :]' '{ print $4 }'`
	echo "There is an iSCSI session running for $LOGIN from IP $IP"
	echo "Aborting"
	exit 2
fi

grep -qE "$IQN\$" /proc/net/iet/volume
if [ $? -ne 0 ]
then
	echo "iSCSI target does not exist for $LOGIN"
else
	TID=`grep $IQN /proc/net/iet/volume | awk -F'[: ]' '{ print $2 }'`
	echo "Deleting iSCSI LUN for $LOGIN"
	sudo ietadm --op delete --tid=$TID --lun 0
	echo "done"
	echo "Deleting iSCSI target for $LOGIN"
	sudo ietadm --op delete --tid=$TID
	echo "done"
fi

if [ -f $IMG ]
then
	echo "Deleting home image for $LOGIN"
	sudo rm -f $IMG
	echo "done"
fi

if [ -f $IETCONFDIR/$LOGIN.conf ]
then
	echo "Deleting iet config for $LOGIN"
	sudo rm $IETCONFDIR/$LOGIN.conf
	echo "Regenerating iet config"
	cat $IETCONFDIR/*.conf | sudo tee $IETCONF > /dev/null
	echo "done"
fi