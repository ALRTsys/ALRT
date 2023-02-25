import flet as ft


# About Page
class AboutApp(ft.UserControl):
    def go_main(self, e):
        self.page.route = "/main"
        self.page.update()


    def build(self):
            self.st = ft.Stack(
                [  ft.Container(
                    content = ft.Image(
                        src=f"/images/about Blue 3.png",
                        width=1550,
                        height= 850,
                   expand=1,
                        fit=ft.ImageFit.FILL,
                       
                        
                    ), alignment=ft.alignment.center,expand = True),
                    ft.Container(
                        width=100,
                        padding=6,
                        bgcolor="#1A1C1E",
                        border_radius=5,
                        left=15,
                        top = 30,
                        alignment=ft.alignment.center,
                        content = ft.Text("Back", size= 20),
                        on_click = self.go_main,
                    ),
                    ],
                width=1400 ,
                height=600,

            )
            return  self.st
