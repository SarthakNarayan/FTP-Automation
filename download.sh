#!/bin/bash

[ -z $1 ] && echo "No video link given, please give a video link" && exit 1

echo "Checking If the FTP server is UP"
python3 /home/sarthaknarayan/youtube-dl/code/CheckFtpConnection.py
if [ $? -eq 1 ]; then
    echo "FTP server is down please try again after restarting the server"
    exit 1
fi

echo "FTP server is up downloading the video"
echo -e "--------------------------------------------------------- \n [`date`]" >> ./logs/download.log
yt-dlp -x --restrict-filenames --no-progress -o '%(title)s.%(ext)s' $1 &>> ./logs/download.log
echo -e "--------------------------------------------------------- \n" >> ./logs/download.log

audio_file=`ls | grep .opus`

if [ -z $audio_file ]; then
    echo "Some error occurred while downloading the file, please check the downloader or the download link"
    exit 1
fi

echo "Video successfully downloaded"

if [ -z $2 ]; then
    echo "No audio conversion value provided defaulting to 1.5"
    audio_rate='1.5'
else
    echo "Audio conversion rate is $2"
    audio_rate=$2
fi

converted_audio_file=${audio_file}_converted_${audio_rate}.opus
echo -e "Duration of the original video \n `ffmpeg -i $audio_file 2>&1 | grep Duration`"
echo -e "--------------------------------------------------------- \n [`date`]" >> ./logs/conversion.log
ffmpeg -i $audio_file -filter:a "atempo=${audio_rate}" -vn $converted_audio_file &>> ./logs/conversion.log
echo -e "--------------------------------------------------------- \n" >> ./logs/conversion.log
echo -e "Duration of the converted video \n `ffmpeg -i $converted_audio_file 2>&1 | grep Duration`"

echo "Audio converision complete"

python3 /home/sarthaknarayan/youtube-dl/code/Uploader.py --file $converted_audio_file

if [ $? -eq 1 ]; then
    echo "Some error occurred while transferring the file, please check logs"
    echo "cleaning up"
    rm $audio_file
    exit 1
fi

echo "file successfully uploaded, doing cleanup"
rm $audio_file $converted_audio_file