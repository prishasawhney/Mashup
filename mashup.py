from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import zipfile
from dotenv import load_dotenv
load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS") 
email_password = os.getenv('EMAIL_PASSWORD')

def get_urls(Singer, num):
    Singer = Singer.replace(" ", "+") + "+songs"
    videosSearch = VideosSearch(Singer, limit = num)
    result = videosSearch.result()['result']
    links = []
    for i in range(num):
        links.append(result[i]['link'])
    return links

def extract_audio(links, Singer):
    mp3_files = []
    current_directory = os.getcwd().replace("\\", "/")
    for i,link in enumerate(links, start=1):
        yt = YouTube(link)
        audio = yt.streams.filter(only_audio=True).first()
        file_name = "{} song {}.mp3".format(Singer, i)
        file_path = current_directory + "/" + file_name
        audio.download(filename=file_name)
        mp3_files.append(file_path)
        print("Downloaded: ", yt.title)
    return mp3_files

def cut_duration(mp3_files, seconds):
    cut_paths=[]
    for song in mp3_files:
        input_name = f"\"{song}\""
        file_name = song.replace(".mp3","")
        output_name = f"\"{file_name}_cut" + ".mp3\""
        command1 = f"ffmpeg -i {input_name} -t {seconds} {output_name}"
        # print(command)
        try:
            os.system(command1)
            os.remove(song)
            cut_paths.append(output_name)
            print(f"{song} cut successfully.")
        except Exception as e:
            print(f"Error occurred while cutting {song}: {e}")
    return cut_paths

def merge_audio(mp3_files, output_filename):
    input_files = "|".join(mp3_files).replace("\"|\"", "|")
    cwd = os.getcwd().replace("\\", "/")
    output_name = cwd + "/" + output_filename
    output_name = f"\"{output_name}\""
    command = f"ffmpeg -i concat:{input_files} -c copy {output_name}"
    print(command)
    try:
        os.system(command)
        print("Audio files merged successfully.")
        for song in mp3_files:
            print(song)
            os.remove(song.replace("\"", ""))
    except Exception as e:
        print(f"Error occurred while merging audio files: {e}")

def zip_file(input_filename, output_filename):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        zipf.write(input_filename, arcname=input_filename)

def send_mail(to, filename):
    msg = MIMEMultipart()
    msg['Subject'] = "Mashup File"
    msg['From'] = email_address
    msg['To'] = to 

    with open(filename,'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name='102116052-output.zip'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    
if __name__=="__main__":
    n= len(sys.argv)
    if (n<5):
        print(n)
        print("Number of Arguments did not match!")
        sys.exit(1)
    Singer = sys.argv[1]
    num = int(sys.argv[2])
    if (num<10):
        print("Number of songs should be greater than 10")
        sys.exit(1)
    seconds = int(sys.argv[3])
    if (seconds<20):
        print("Duration should be greater than 20 seconds")
        sys.exit(1)
    output_mp3 = sys.argv[4]
    output_zip = output_mp3.replace(".mp3", ".zip")
    links = get_urls(Singer, num)
    mp3_files = extract_audio(links, Singer)
    cut_paths = cut_duration(mp3_files, seconds)
    merge_audio(cut_paths, output_mp3)
    
    if (n==6):
        zip_file(output_mp3, output_zip)
        send_mail(sys.argv[5], output_zip)