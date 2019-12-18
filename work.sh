/home/root/ip.sh &

sleep 1

/home/root/SmartRack &

sleep 2

kill -9 $(ps -aux|grep '[S]martRack'|awk '{print $2}')

sleep 1

nohup python /home/root/dgmini/app.py &

sleep 1

/home/root/forward &

exit 0