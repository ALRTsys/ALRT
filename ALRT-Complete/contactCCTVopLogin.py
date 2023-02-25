import flet as ft

# Contact us page
class ContactAppCCTVopLogin(ft.UserControl):
    def go_main(self, e):
        self.page.route = "/LoginForCCTVop"
        self.page.update()

    def build(self):
        self.st = ft.Stack(
            [ft.Container(
                content=ft.Image(
                    src=f"/images/contact Blue (2).png",
                    width=1550,
                    height=850,
                    expand=1,
                    fit=ft.ImageFit.FILL,

                ), alignment=ft.alignment.center, expand=True),
                ft.Row(controls=[ft.Container(
                    width=100,
                    padding=6,
                    bgcolor="#1A1C1E",
                    border_radius=0,

                    alignment=ft.alignment.center,
                    content=ft.Text("Back", size=20),
                    on_click=self.go_main,
                )],
                    width=1200,
                    top=30,
                    left=15,
                )
            ],
            width=1400,
            height=600,
        )
        return self.st

