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

error_links = []

cmd("mkdir -p logs")
cmd("mkdir -p Downloads")
print("Checking if FTP server is UP...")

while links != []:
    link = links[0]
    try:
        print()
        print(10 * "-")
        print("⬇️  Starting Video Download...")
        status_code = cmd(
            f"yt-dlp -x --restrict-filenames -o '%(title)s.%(ext)s' {link} 2>>./logs/download.log"
        ).returncode

        if status_code != 0:
            print(
                f"Some error has occured while downloading the video {link} refer download logs"
            )
            raise Exception
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
            raise Exception

        audio_file = audio_file.replace("\n", "")
        converted_audio_file = f"{audio_file}_converted_{AUDIO_RATE}.mp3"

        print(f"📋 Name of the video: {audio_file}")
        print("🔊 Video download complete changing the rate of the audio file.")
        cmd(
            f'ffmpeg -loglevel error -i {audio_file} -filter:a "atempo={AUDIO_RATE}" -vn {converted_audio_file} >/dev/null 2>>./logs/conversion.log'
        )
        print("⬆️  Audio converision complete. Starting upload...")
        status_code = cmd(f"mv {converted_audio_file} ./recordings").returncode
        if status_code != 0:
            print(
                "Some error occurred while transferring the file, please check logs, cleaning up"
            )
            cmd(f"rm {audio_file}")
            raise Exception

        print("🗑️  File successfully moved file to Downloads, doing cleanup")
        cmd(f"rm {audio_file}")
        links.pop(0)
    except Exception as e:
        print(f"Exception: {e}")
        cmd("trash *.part *.ytdl", check=False)

cmd("echo '' > links.txt")
cmd(
    "mv ./recordings/* '/Users/sarthaknarayan/Library/Mobile Documents/com~apple~CloudDocs/Recordings/'"
)
