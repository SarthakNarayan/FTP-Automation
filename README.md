# Objective of the Project
This project is used to automate the process of 
- Downloading A Youtube Video 
- Converting the video to an audio file
- Changing the playback speed of the audio file
- Uploading the video to an FTP server running on a cell phone  

# Why Did I build this project
So that I can listen to YouTube videos as podcasts anywhere.

# Description
- Downloading the YouTube Video <br>
For downloading the YouTube video I used yt-dlp package. [Link](https://github.com/yt-dlp/yt-dlp) to GitHub.

- Converting the video to audio file and changing its playback <br>
This was done using ffmpeg

- Uploading the video to a FTP server running on a cell phone <br>
App used for creating a FTP server on a cell phone (Android Phone) -> WiFi FTP Server
Python's FTP library was used for transferring audio to the FTP server

# Other Information
- The cell phone running the FTP server and the linux machine should be on the same internal network.
- Python's FTP library couldn't work properly on mac due to some permission issues.
- It is better to have a static IP for the cellphone running your FTP server so that you don't have to change the target in your python code.
- Run download.sh script with the link to video as the first argument. Example
```
./download.sh https://www.youtube.com/watch?v=j9XXsdE59-o 
```
```
./download.sh https://www.youtube.com/watch?v=j9XXsdE59-o 1.0
```
If you want normal playback speed. By default the playback speed is set to 1.5. You can change it in the download.sh file.
- The code has logging at different levels. So if you ever face a problem just go to /logs directory. It will be created if you run the script atleast once.

## Logging
- logging.log file contains all the information about the steps taken by the FTP library for sending the file to the server. If you have any connection issues you can come here and take a look.
- dowload.log file contains logs generated while downloading the video. So if you are unable to download the video you can come here to see what is the problem.
- conversion.log file contains logs generated while changing the playback speed of the audio.
