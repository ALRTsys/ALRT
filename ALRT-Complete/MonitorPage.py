import flet as ft
from time import strftime
import threading
import cv2
import base64
import time
from process_video import ProcessVideo


class MainApp(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.url = "https://www.fesliyanstudios.com/soundeffects-download.php?id=4383"

        self.STOP = False
        self.MUTE_AUDIO_DELAY = 40  # mute alert for 6[second]
        self.MUTE_ALERT = False
        self.IS_VIDEO_THREAD_RUNNING = False
        self.IS_AUDIO_THREAD_RUNNING = False
        self.IS_AUDIO_PLAYING = False
        self.PLAY_AUDIO = False
        self.PLAY_VIDEO = False
        self.ALERT_MESSAGE = "Person Detected"
        self.dialog_is_open = False
        self.start_video_thread()
        self.start_alarm_thread()

    # // -------------------- Open Alert Dialog With Specific Msg ----------------------------------//
    def open_alert_dialog(self):
        if self.dialog_is_open or self.MUTE_ALERT:
            print(f"--- already dialog is open ")
        else:
            print(f"--- open  dialog")
            self.alert_text.value = self.ALERT_MESSAGE
            self.alert_dialog.visible = True
            self.dialog_is_open = True
            self.alert_dialog.update()

    def close_alert_dialog(self, e):
        print(f"--- close dialog ")
        self.alert_dialog.visible = False
        self.dialog_is_open = False
        self.alert_dialog.update()
        self.page.update()
    # // -------------------- Find and kill the thread ----------------------------------//
    def find_and_kill_thread(self, name):
        for thread in threading.enumerate():
            if thread.name == name:
                thread.join()
                print(f'Thread {name} stopped')
                return
        print(f'Thread {name} not found')
    # // -------------------- Process and Render Video in the screen --------------------//
    def display(self):
        process = ProcessVideo("TestVideo.avi")
        for data in process.start():
            if not self.PLAY_VIDEO:
                process.set_stop(True)
                break
            if data[1]:
                self.PLAY_AUDIO = True
                self.ALERT_MESSAGE = data[2]['type'] + f" Detected!!"
                if not self.dialog_is_open:
                    print(f"---dialog_is_open false")
                    print("Alarm is on")
                    self.open_alert_dialog()

            jpg_img = cv2.imencode('.jpg', data[0])
            b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
            self.image_box.src_base64 = b64_string
            if not self.STOP:
                # sometime trying to update when self.image_box obj
                # removed [this happened whe go help center btn clicked]
                # so we'll check before update
                self.image_box.update()
                self.page.update()

                # // -------------------- Control the Video ---------------------------------//

    def video(self):
        while True:
            if self.STOP:
                print("---- break video")
                break
            if self.PLAY_VIDEO:
                self.display()
                time.sleep(2)
    # // -------------------- Process Audio ---------------------------------//
    def audio_(self):
        time.sleep(6)  # This must add to wait until the audio created in GUI
        while True:
            if self.STOP:
                break
            if self.PLAY_AUDIO and not self.MUTE_ALERT:
                if self.IS_AUDIO_PLAYING:
                    self.audio.update()
                    time.sleep(2)
                    pass
                else:
                    self.audio.play()
                    self.IS_AUDIO_PLAYING = True
                    self.audio.update()
            else:
                self.audio.release()
                self.IS_AUDIO_PLAYING = False

    # // -------------------- Start Video Thread ------------------------------//
    def start_video_thread(self):
        if self.IS_VIDEO_THREAD_RUNNING:
            # the thread already running [return]
            return
            # Starting the video thread [to run video in other thread instead the main thread]
        video_thread = threading.Thread(target=self.video, name='video_thread')
        video_thread.daemon = True
        print("[*] VIDEO THREAD RUNNING")
        video_thread.start()

    # // -------------------- Start Audio Thread -------------------------------//
    def start_alarm_thread(self):
        if self.IS_AUDIO_THREAD_RUNNING:
            # the thread already running [return]
            return
            # Starting the video thread [to run audio in other thread instead the main thread]
        audio_thread = threading.Thread(target=self.audio_, name='audio_thread')
        audio_thread.daemon = True
        print("[*] AUDIO THREAD RUNNING")
        audio_thread.start()

    # // -------------------- Animate Button Color when Hover --------------------//
    def on_hover(self, e):
        e.control.bgcolor = "#A3A5AB" if e.data == "true" else "#22252E"
        e.control.update()

    # // -------------------- Date and Time -----------------------------------//
    def get_date(self):
        time_string = strftime('%H:%M %p  %x')
        return time_string

    # // -------------------- Text -----------------------------------//
    def get_text(self):
        text = " CCTV operator 1"
        return text

    # // -------------------- Audio Complete[play again] ----------------------------//
    def audio_complete(self, e):  # this function trigger when audio complete
        self.IS_AUDIO_PLAYING = False
        # // -------------------- Stop Alert for some second ----------------------------//

    def stop_alert(self):
        self.PLAY_AUDIO = False  # This var Controlled by process video func [change to True when detect Tailgating and piggybacking]
        self.MUTE_ALERT = True
        self.alert_dialog.visible = False
        print(f"--- close dialog_is_open ")
        self.alert_dialog.update()
        self.dialog_is_open = False
        self.page.update()
        time.sleep(self.MUTE_AUDIO_DELAY)  # Mute for some seconds
        self.MUTE_ALERT = False  # return to default

    # // ------------------ Handle Button Click Event ------------------------------//
    def button_clicked(self, e):
        data = e.control.data
        if data == 1:  # Monitor Button Clicked
            print("Monitor Button Clicked")
            self.PLAY_VIDEO = True  # Display Video in the screen
            self.page.update()


        elif data == 2:
            print("Close Alet Button Clicked")
            self.stop_alert()
        elif data == 3:
            print("Help Center Button Clicked")
            # // ---- Stopping -----//
            self.STOP = True
            self.PLAY_AUDIO = False
            self.PLAY_VIDEO = False

            # // ----- to insure that the thread has been stopped ---//

            self.find_and_kill_thread('video_thread')
            self.find_and_kill_thread('audio_thread')

            # // ----- Go to contact page ------------------------//

            self.page.route = "/contactCCTVopMonitor"
            self.page.update()

        elif data == 4:
            print("LogOut Button Clicked")

            # // ---- Stopping -----//

            self.STOP = True
            self.PLAY_AUDIO = False
            self.PLAY_VIDEO = False

            # // ----- to insure that the thread has been stopped ---//

            self.find_and_kill_thread('video_thread')
            self.find_and_kill_thread('audio_thread')

            # // ----- Return to login page ------------------------//
            self.page.session.set("login", False)
            self.page.route = "/login"
            self.page.update()

    # // -------------------- This Function for building GUI ------------------------//
    def build(self):
        # //------------- This is image container for next used to display video as series of images ---//
        self.b64_string = "None"
        self.image_box = ft.Image(src_base64=self.b64_string, width=800,
                                  height=490, fit=ft.ImageFit.FILL, )
        # // ----------- Alert Dialog --------------------------------------------//
        self.alert_text = ft.Text(self.ALERT_MESSAGE, size=18, color="red600", italic=True)
        self.alert_dialog = ft.Column(
            visible=False,
            bottom=140,  # for move to bottom
            right=-30,  # for mov from left to right
            controls=[ft.Container(
                #bgcolor="#ffffff",
                #padding=16,
                alignment=ft.alignment.center,
                margin=60,
                border_radius=ft.border_radius.all(7),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        self.alert_text,

                    ]),
                width=400)])

        # // ----------- Monitor Button ------------------------------------------//
        self.monitor_btn = ft.TextButton(
            width=100,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("Start Monitor", size=16, )),
            on_hover=self.on_hover,
            style=ft.ButtonStyle(shape=ft.CountinuosRectangleBorder(radius=20),
                                 color=ft.colors.WHITE
                                 ),
            on_click=self.button_clicked, data=1)

        # // -------- Alert Button -----------------------------------------------//
        self.close_alert_btn = ft.TextButton(
            width=100,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("Close Alert", size=16, )),
            on_hover=self.on_hover,
            style=ft.ButtonStyle(shape=ft.CountinuosRectangleBorder(radius=0),
                                 color=ft.colors.WHITE
                                 ),
            on_click=self.button_clicked, data=2)
        # // -------- Center Help Button -----------------------------------------------//
        self.help_center_btn = ft.TextButton(
            width=100,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("Help", size=16, )),
            on_hover=self.on_hover,
            style=ft.ButtonStyle(shape=ft.CountinuosRectangleBorder(radius=20),
                                 color=ft.colors.WHITE
                                 ),
            on_click=self.button_clicked, data=3)
        # // -------- LogOut Button -----------------------------------------------//
        self.log_out_btn = ft.TextButton(
            width=100,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("LogOut ", size=16, )),
            on_hover=self.on_hover,
            style=ft.ButtonStyle(shape=ft.CountinuosRectangleBorder(radius=0),
                                 color=ft.colors.WHITE
                                 ),
            on_click=self.button_clicked, data=4)


        # // -------- Audio -----------------------------------------------//
        self.audio = ft.Audio(
            src=self.url,  # audio for alarm
            autoplay=False,
            volume=1,
            balance=0,
            on_seek_complete=self.audio_complete,
        )


        # // -------- Video Container --------------------------------------//
        self.video_container = ft.Container(
            width=570,
            height=464,
            alignment=ft.alignment.center,
            content=self.image_box,
        )
        # // ---------- All Component in Stack Container -------------------//
        self.st = ft.Stack(
            [
                # //------ Audio ---------------//
                self.audio,
                # //------ Backgound Image -----//
                ft.Container(
                    content=ft.Image(
                        src=f"/images/monitor cctv.png",
                        width=1300,
                        height=700,
                        expand=1,
                        fit=ft.ImageFit.FILL,
                    ), alignment=ft.alignment.center, expand=True),
                # //------ Sidbar ---------------//
                ft.Column(
                    top=193,  # for move to bottom
                    left=120,  # for mov from left to right
                    controls=[
                        self.monitor_btn,
                        ft.Container(height=10),  # space between monitor and close alert
                        self.close_alert_btn,
                        ft.Container(height=15),  # space between close and help center
                        self.help_center_btn,
                        ft.Container(height=15),  # space between  help center and logOut
                        self.log_out_btn,
                    ]
                ),
                # //------ Date ---------------//
                ft.Row(controls=[
                    ft.Text(self.get_date(), size=18),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=1550,
                    top=150,  # used to space date in right place
                    left=270,  # used to space date in right place
                ),

                # // -------- Text --------------------------------------//
                ft.Row(controls=[
                    ft.Text(self.get_text(), size=18, style=ft.TextThemeStyle.TITLE_LARGE),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    top=220,  # used to space date in right place
                    right = 130,  # used to space date in right place
                ),
                # //------ Video Container ------//
                ft.Row(controls=[
                    self.video_container,
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=1200,
                    top=110,  # used to space video in right placecd ..
                    left=-50,  # used to space video in right place
                ),
                self.alert_dialog,
            ],
            width=1400,
        )
        return self.st

