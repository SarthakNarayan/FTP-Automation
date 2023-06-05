import subprocess
import sys
import time

AUDIO_RATE = 1.5


def cmd(command: str, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True):
    return subprocess.run(
        command, shell=True, check=check, stdout=stdout, stderr=stderr, text=True
    )


# Reading the links
with open("links.txt", "r") as file:
    lines = file.readlines()

links = []
for line in lines:
    links.append(line.strip())

if links == []:
    print("links.txt is empty exiting")
    sys.exit(1)

cmd("mkdir -p logs")
print("Checking if FTP server is UP...")

status_code = cmd("python3 code/CheckFtpConnection.py").returncode
if status_code != 0:
    print("FTP server is down please try again after restarting the server")
    sys.exit(1)

print("⬆️ FTP server is up downloading the videos")
for link in links:
    print()
    status_code = cmd(
        f"yt-dlp -x --restrict-filenames -o '%(title)s.%(ext)s' {link} 2>>./logs/download.log"
    ).returncode

    if status_code != 0:
        print(
            f"Some error has occured while downloading the video {link} refer download logs"
        )
        sys.exit(1)
    time.sleep(3)

    audio_file = cmd(
        "ls | grep .opus || ls | grep .mp3 || ls | grep .mp4 || ls | grep .m4a",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout

    if audio_file == "":
        print(
            "Variable audio_file is empty, this may be due to unknown audio format. Please remove the downloaded video"
        )
        sys.exit(1)

    audio_file = audio_file.replace("\n", "")
    converted_audio_file = f"{audio_file}_converted_{AUDIO_RATE}.opus"

    cmd(
        f'ffmpeg -loglevel error -i {audio_file} -filter:a "atempo={AUDIO_RATE}" -vn {converted_audio_file} >/dev/null 2>>./logs/conversion.log'
    )
    print("Audio converision complete. Starting upload...")
    status_code = cmd(
        f"python3 code/Uploader.py --file {converted_audio_file}"
    ).returncode
    if status_code != 0:
        print(
            "Some error occurred while transferring the file, please check logs, cleaning up"
        )
        cmd(f"rm {audio_file}")
        sys.exit(1)

    print("File successfully uploaded, doing cleanup")
    cmd(f"rm {audio_file} {converted_audio_file}")
