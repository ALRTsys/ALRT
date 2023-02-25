import flet as ft
from flet import icons
import time
import mysql.connector
from flet.auth import user

mydb = mysql.connector.connect(
    host= 'localhost',
    user= 'usually its root but if you changed it, put yours',
    password= 'put your own password',
    port= '3306',
    database= 'log_in'
)

# Login Page
class AdminLoginApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.FAILED_TIMES = 1
        self.MAX_TRY_TIMES = 3
        self.WAITE_TIMES = 60
        try:
            self.log = open('log.txt', "a")
        except:
            print("Cannot open log file")

    def go_contact(self, e):
        self.page.route = "/contactAdminLogin"
        self.page.update()

    def go_about(self, e):
        self.page.route = "/aboutAdmin"
        self.page.update()

    def go_LoginForCCTVop(self, e):
        self.page.route = "/LoginForCCTVop"
        self.page.update()

    def verify(self, e):
        # user entry
        email_value= self.email.value
        password_value= self.password.value
        # connect with database
        mycursor = mydb.cursor()
        sql = "SELECT * FROM cctv_operator WHERE BINARY Username ='%s' AND BINARY Password =sha1('%s')" % (email_value, password_value)
        mycursor.execute(sql)
        if mycursor.fetchone():
            if email_value == 'Admin':
                #go to admin monitor page
                print("---- login success ---")

                self.page.session.set("login", True)
                self.page.session.set("user" , user)
                self.page.route = "/AdminMonitorPage"
                self.log.write(time.strftime('%H:%M:%S %p  %x') + ' Admin Login ' + '\n')#log the login information in the text file
                self.page.update()
            elif email_value != 'Admin':
                #user enter incorrect information
                self.FAILED_TIMES += 1
                self.email.error_text = "Incorrect Username"
                self.email.value = ""
                self.password.error_text = "Incorrect Password"
                self.password.value = ""
                self.email.update()
                self.password.update()
                if self.FAILED_TIMES == self.MAX_TRY_TIMES:
                    print("----disable some seconds ----")
                    self.email.disabled = True
                    self.password.disabled = True
                    time.sleep(self.WAITE_TIMES)
                    print("--- disable time ends ----")
                    self.FAILED_TIMES = 0
                    self.email.disabled = False
                    self.password.disabled = False
                    self.email.update()
                    self.password.update()
        else:
            #user enter incorrect information
            self.FAILED_TIMES += 1
            self.email.error_text = "Incorrect Username"
            self.email.value = ""
            self.password.error_text = "Incorrect Password"
            self.password.value = ""
            self.email.update()
            self.password.update()
            if self.FAILED_TIMES == self.MAX_TRY_TIMES:
                print("----disable some seconds ----")
                self.email.disabled = True
                self.password.disabled = True
                time.sleep(self.WAITE_TIMES)
                print("--- disable time ends ----")
                self.FAILED_TIMES = 0
                self.email.disabled = False
                self.password.disabled = False
                self.email.update()
                self.password.update()
        self.log.flush()
        self.log.close()

    def build(self):

            self.password= ft.TextField(
                label="",
                hint_text="Password",
                password=True,
                can_reveal_password=True,
                cursor_color=ft.colors.BLACK,
                color=ft.colors.BLACK,
                bgcolor="#cccccc",

            focused_color=ft.colors.BLACK,
            focused_bgcolor="#cccccc",
            border_radius=30,
            border_color="#cccccc",
            focused_border_color=ft.colors.LIGHT_BLUE_500,
            max_length=30,

                filled=True)
            self.email  =  ft.TextField(label="",hint_text="UserName", cursor_color=ft.colors.BLACK,
                color=ft.colors.BLACK,
                bgcolor="#cccccc",

            focused_color=ft.colors.BLACK,
            focused_bgcolor="#cccccc",
            border_radius=30,
            border_color="#cccccc",
            focused_border_color=ft.colors.LIGHT_BLUE_500,
            max_length=20,

                filled=True)
            self.login_text  =  ft.Container(
                        content = ft.Text("Login",size=40,
                        color="#cccccc",
                        weight=ft.FontWeight.W_500,
                        ),
                        # Here you can change margin left of alrt logo
                        margin = ft.margin.all(20),
                        )
            self.user_img  =ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            controls = [ ft.Container(
                content =  ft.Icon(name=icons.PERSON, color="#ffffff", size=60),
                bgcolor="#cccccc",
                border_radius= ft.border_radius.all(50),
                padding= 15)])
            self.submit =ft.Container(
                                content=ft.Row(
                                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    controls =  [

                                    ft.Text("Sign in"),
                                    ],
                                ),
                                bgcolor="#0099cc",
                                border_radius = 50,
                                padding = 15,
                                #width=150,
                                on_click = self.verify

                            )

            self.login_form = ft.Container( content=ft.Stack(
                [ft.Container(
                    content=ft.Column(
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                        controls = [  ft.Container( padding = 12,),
                                        ft.Container(
                                                            bgcolor="#ffffff",

                                                            padding = 16,
                                                            border_radius= ft.border_radius.all(40),
                                                            content=ft.Column(
                                                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                                    spacing = 7,
                                                                    controls = [
                                                                        self.login_text,
                                                                        self.email,
                                                                        self.password,
                                                                        self.submit
                                                                ]),
                                                            width= 390,
                                                            height = 370),
                                                    ],
                                        )),
                                        self.user_img,]
                            ,width= 340,height = 410, ),
                            bgcolor = "#1A1C1E",
                            margin = ft.margin.symmetric(horizontal=100, vertical=150))

            self.main_container = ft.Row(

                spacing = 40,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(content = ft.Text("Alert",size=80,
                        color="#0066ff",
                        visible = False,
                        style=ft.TextThemeStyle.DISPLAY_LARGE,
                        weight=ft.FontWeight.BOLD,
                        )
                        # Here you can change margin left of alrt logo
                        ,margin = ft.margin.only(left=0)
                        ),
                    self.login_form],
                    width=1400 ,
                    height= 700,

                    )

            self.header = ft.Container(
                    content=ft.Row(
                            alignment = ft.MainAxisAlignment.END,
                            controls = [
                                ft.TextButton(text="About us", on_click=self.go_about, style=ft.ButtonStyle(color=ft.colors.WHITE)),
                                ft.TextButton(text="Contact us", on_click=self.go_contact, style=ft.ButtonStyle(color=ft.colors.WHITE)),
                                ft.TextButton(text="Sign in As CCTV opretor?", on_click=self.go_LoginForCCTVop, style=ft.ButtonStyle(color=ft.colors.WHITE)),
                            ]),
                    padding=0,
                    margin = ft.margin.symmetric(horizontal=100, vertical = 5),
                    width=1570 ,
                    alignment=ft.alignment.top_right,
                    bgcolor="#1A1C1E",

                    )

            self.st = ft.Stack(
                [
                    ft.Image(
                        src=f"/images/ALRT GP2 Interface.png",
                        width=1400,
                        height= 700,
                        fit=ft.ImageFit.FILL,
                    ),
                    self.header,
                    self.main_container,
                    ],
                width=1400 ,
            )

            return  self.st

