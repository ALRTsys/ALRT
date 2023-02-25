from cgitb import text

import flet as ft


# About Page
class Adminlogs(ft.UserControl):
    def go_main(self, e):
        self.page.route = "/AdminMonitorPage"
        self.page.update()
    def build(self):
        self.st = ft.Stack(
            [ft.Container(
                content=ft.Image(
                    src=f"/images/logs.png",
                    width=1550,
                    height=850,
                    expand=1,
                    fit=ft.ImageFit.FILL,
                ), alignment=ft.alignment.center, expand=True),
                ft.Container(
                    width=100,
                    padding=6,
                    bgcolor="#1A1C1E",
                    border_radius=5,
                    left=15,
                    top=30,
                    alignment=ft.alignment.center,
                    content=ft.Text("Back", size=20),
                    on_click=self.go_main,
                ),

                ft.Row(controls=[
                    ft.Text(self.get_text(), size=18, style=ft.TextThemeStyle.TITLE_LARGE),
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    top=220,  # used to space date in right place
                    right=700,  # used to space date in right place
                ),
            ],
            width=1400,
            height=600,

        )
        return self.st

    def get_text (self):
        with open('log.txt') as f:
            text = f.read()
        return text

    def build1(self):
        self.st = ft.Stack(

            width=1400,
        )
        return self.st
