import os
import flet as ft
from home_page import home_page
from tables_page import tables_page


# <a href="https://www.flaticon.com/free-icons/calendar" title="calendar icons">Calendar icons created by Freepik - Flaticon</a>

def main(page: ft.Page):
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def event(e):
        if e.data == 'detach' and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)
    page.on_app_lifecycle_state_change = event

    def route_change(route):
        page.views.clear()
        page.views.append(home_page(page))
        if route.route.split("?")[0] == '/tables':
            page.views.append(tables_page(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)
