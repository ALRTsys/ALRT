import flet as ft
from flet import Page
from LoginForCCTVop import CCTVopLoginApp
from LoginForAdmin import AdminLoginApp
from MonitorPage import MainApp
from AdminMonitorPage import AdminMainApp
from about import AboutApp
from aboutAdmin import AboutAppAdmin
from contactAdminLogin import ContactAppAdminLogin
from contactAdminMonitor import ContactAppAdminMonitor
from contactCCTVopLogin import ContactAppCCTVopLogin
from contactCCTVopMonitor import ContactAppCCTVopMonitor
from logs import Adminlogs

IS_LOGIN = False

def main(page: Page):  # the GUI design
    page.title = "ALRT detection System "
    page.window_width = 1400
    page.window_height = 700
    page.padding = 0
    theme = ft.Theme()
    theme.page_transitions.macos = "fadeUpwards"
    page.theme = theme
    page.theme_mode = ft.ThemeMode.DARK
    page.update()
    page.window_center()
   
    def route_change(route):
        print(page.route)
        page.views.clear()
        page.views.append(
            ft.View( # to choose where the path you will go to
                "/login",
                [
                  CCTVopLoginApp()
                ],
            )
        )
        if page.route == "/MonitorPage": # to go to monitorpage
            print("--the route is main--")
            if page.session.get("login"):
                print("---page.session.get(\"login\")",page.session.get("login"))
                print(page.route)
                page.views.append(
                    ft.View(
                        "/MonitorPage",
                        [
                        MainApp()
                        ],
                    )
                )
                page.update()
            else:
                page.go("/login")
                page.update()

        elif page.route == "/contactAdminLogin":
            page.views.append(
            ft.View(
                "/contactAdminLogin",
                [
                  ContactAppAdminLogin()
                ],
            )
        )
        elif page.route == "/contactAdminMonitor":
            page.views.append(
            ft.View(
                "/contactAdminMonitor",
                [
                  ContactAppAdminMonitor()
                ],
            )
        )

        elif page.route == "/contactCCTVopLogin":
            page.views.append(
                ft.View(
                    "/contactCCTVopLogin",
                    [
                        ContactAppCCTVopLogin()
                    ],
                )
            )
        elif page.route == "/contactCCTVopMonitor":
            page.views.append(
                ft.View(
                    "/contactCCTVopMonitorr",
                    [
                        ContactAppCCTVopMonitor()
                    ],
                )
            )
        elif page.route == "/AdminMonitorPage":
            page.views.append(
                ft.View(
                    "/AdminMonitorPage",
                    [
                        AdminMainApp()
                    ],
                )
            )
        elif page.route == "/LoginForAdmin":
            page.views.append(
                ft.View(
                    "/LoginForAdmin",
                    [
                        AdminLoginApp()
                    ],
                )
            )
        elif page.route == "/aboutAdmin":

            page.views.append(
                ft.View(
                    "/aboutAdmin",
                    [
                        AboutAppAdmin()
                    ],
                )
            )
            page.update()
        elif page.route == "/logs":

            page.views.append(
                ft.View(
                    "/logs",
                    [
                        Adminlogs()
                    ],
                )
            )
            page.update()
        elif page.route == "/about":
            
            page.views.append(
            ft.View(
                "/about",
                [
                  AboutApp()  
                ],
            )
        )
            page.update()
        print(page.route)
        page.update()



    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    page.update()
    

ft.app(target=main, port=8550,assets_dir="./assets")
