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
root.iconbitmap('./img/angelplayer.ico') # icon 지정

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
    down_notification.place(x=100, y=210)

    # 다운로드 파일명
    global down_filename
    down_filename_style = tkFont.Font(family="Arial", size=7)
    down_filename = Label(root, text='', bg="white", anchor="center", width = 48, height = 1, font=down_filename_style)
    down_filename.place(x=54, y=235)

    # load youtube url
    global url
    url = Entry(width = 41, relief="solid")
    url.place(x=54, y=310)  
    global url_alert
    url_alert = Label(root, text='', bg="white", fg='red')
    url_alert.place(x=54, y=333)
    
    # load download path
    global download_path
    # download_path = os.path.dirname(os.path.realpath(__file__))
    download_path = ''
    btn = Button(root, text="Find...", command=search_path, bg="white", width = 40).place(x=54, y=402)
    path = Label(root, text='버튼 클릭 후 취소 시 프로그램 폴더에 다운로드', bg="white", anchor='w', width = 40, height = 1)
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

    # outtmpl 설정
    if download_path != '': # 사용자가 경로 지정 시
        print('download_path not ""', download_path)
        ydl_opts['outtmpl'] = download_path + '/%(title)s.%(ext)s' # dowonload 경로 지정
    else: # 사용자가 경로를 지정하지 않을 시
        print('download_path', download_path)
        ydl_opts['outtmpl'] = '/%(title)s.%(ext)s'

    # download with youtube_dl
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            fn = ydl.prepare_filename(info_dict)
            
            if download_option == 'audio':
                for i in range(len(fn)-1, -1, -1):
                    if fn[i] == '.':
                        fn = fn[:i]
                        fn += '.mp3'
                        break
            # print('Audio fn : ', fn)
            
            # 113 Line으로 대체
            # ydl.download([youtube_url])

            down_notification.configure(text="Download successful!", fg='blue')
            down_filename.configure(text=f"File Name : {fn}")
            
    except Exception as e:
        print('error', e)
        down_notification.configure(text="Failed to download...", fg='red')
        down_filename.configure(text=f"File Name : {fn}")


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
