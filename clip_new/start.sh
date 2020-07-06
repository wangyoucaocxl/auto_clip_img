#!/bin/bash

path='aidongone/my_data'
echo "start bash">>/home/$path/clip_new/log/running.log
#sleep 30
flag=`ps aux|grep "python3 /home/$path/clip_new/clip_auto_mul_video.py"|grep -v "grep"|wc -l`
while [ 1 ]
do
    if [ $flag == 0 ]
    then
        echo "start python"
        cd /home/$path/clip_new/
        python3 mul_video_new1.py
        echo "end python">>/home/$path/clip_new/log/running.log
    else
        echo "get_graph-data.py is running">>/home/$path/clip_new/log/running.log
    fi
    sleep 5
done
