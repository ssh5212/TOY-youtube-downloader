from email.mime import audio
import os
import youtube_dl
from tkinter import * 
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import tkinter.font as tkFont


# Initialization tkinter 
root = Tk()
root.title("Youtube Downloader") 
root.geometry("400x690") # windows 크기 조정
root.resizable(False, False) # windows 크기 고정

W_canvas = 400
H_canvas = 690

mainframe = Frame(root, padx = 6, pady = 6).grid()


# Main Page
def main():
    def search_path():
        root.dirName=filedialog.askdirectory()
        print(root.dirName)
        path.configure(text="Path : " + root.dirName)
        global download_path
        download_path = root.dirName

    # create Main Page Canvas
    main_page = Canvas(mainframe, width = W_canvas, height = H_canvas)
    main_page.grid(row=1, column=1, rowspan=6, columnspan=6)
    bg_img = ImageTk.PhotoImage(Image.open("./img/main_page.png"))
    root.bg_img = bg_img
    main_page.create_image(0, 0, image=bg_img, anchor="nw")

    # 다운로드 알림
    font_style = tkFont.Font(family="Arial", size=15, weight="bold")
    global down_notification
    down_notification = Label(root, text='', bg="white", fg='red', font=font_style)
    down_notification.place(x=100, y=220)

    # load youtube url
    global url
    url = Entry(width = 41, relief="solid")
    url.place(x=54, y=310)  
    global url_alert
    url_alert = Label(root, text='', bg="white", fg='red')
    url_alert.place(x=54, y=333)
    
    # load download path
    global download_path
    download_path = os.path.dirname(os.path.realpath(__file__))
    btn = Button(root, text="Find...", command=search_path, bg="white", width = 40).place(x=54, y=402)
    path = Label(root, text='경로 미선택 시 프로그램 저장 위치에 다운로드 진행', bg = "white")
    path.place(x=54, y=434)
    
    # audio button function
    audio_button = Canvas(main_page, width = 287, height = 46)
    audio_button.place(x=54, y=480)   
    audio_img = ImageTk.PhotoImage(Image.open("./img/audio_button.png"))
    audio_button.audio_img = audio_img
    audio_button.create_image(0, 0, image=audio_img, anchor="nw")
    audio_button.bind('<Button-1>', extraction_audio)

    # video button function
    video_button = Canvas(main_page, width = 287, height = 46)
    video_button.place(x=54, y=540)   
    video_img = ImageTk.PhotoImage(Image.open("./img/video_button.png"))
    video_button.video_img = video_img
    video_button.create_image(0, 0, image=video_img, anchor="nw")
    video_button.bind('<Button-1>', extraction_video)
    

# Download Page
def extraction():
    if download_option == 'audio':
        ydl_opts = { 
            'format': 'bestaudio/best', # audio quality
            'postprocessors': [{
                'key': 'FFmpegExtractAudio', # extraction video to audio
                'preferredcodec': 'mp3', # audio codec
                'preferredquality': '320',
            }],
        }   

    else:
        ydl_opts = {
            'format': 'best/best',  # video quality
            # 'writethumbnail': 'best',  # video thumbnail download
        }

    # 사용자 경로 지정 시 사용
    if download_path != '':
        ydl_opts['outtmpl'] = download_path + '/%(id)s-%(title)s.%(ext)s' # dowonload 경로 지정
    print(ydl_opts)

    # download with youtube_dl
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            down_notification.configure(text="Download successful!", fg='blue')
            ydl.download([youtube_url])
    except Exception as e:
        print('error', e)
        down_notification.configure(text="Failed to download...", fg='red')



# path ckeck (audio)
def extraction_audio(self):
    global youtube_url
    youtube_url = url.get()
    print('youtube_url : ', youtube_url)

    if youtube_url == '':
        url_alert.configure(text="path is empty")

    else:
        url_alert.configure(text="")

        global download_option
        download_option = 'audio'

        extraction()


# path ckeck (video)
def extraction_video(self):
    global youtube_url
    youtube_url = url.get()
    print('youtube_url : ', youtube_url)

    if youtube_url == '':
        url_alert.configure(text="path is empty")

    else:
        url_alert.configure(text="")

        global download_option
        download_option = 'video'
    extraction()

# Run
main()
root.mainloop()
