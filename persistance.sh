result=`ps aux | grep -i "python3 /falconshare/FalconBot/Falconbotv2.py" | grep -v "grep" | wc -l`
if [ $result -ge 1 ]
   then
        echo "script is running"
   else
        echo "script is not running"
	python3 /falconshare/FalconBot/Falconbotv2.py
fi
