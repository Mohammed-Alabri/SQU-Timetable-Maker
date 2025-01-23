import flet as ft
from functions import courses_data


def home_page(page: ft.Page):
    view = ft.View()
    view.route = '/'
    view.vertical_alignment = ft.MainAxisAlignment.CENTER
    view.controls.append(ft.AppBar(title=ft.Text("SQU TimeTables Maker"), bgcolor=ft.colors.SURFACE_VARIANT))

    def add_cc(crs=None, secs=None):
        if crs is None and secs is None:
            courses_cont.content.controls.append(
                course_countainer(len(courses_cont.content.controls) + 1, page.width))
        else:
            courses_cont.content.controls.append(
                course_countainer(len(courses_cont.content.controls) + 1, page.width, crs, secs))

    courses_cont = ft.Container(content=ft.Column())
    if page.client_storage.contains_key("last_fields"):
        data: dict
        data = page.client_storage.get("last_fields")
        for crss in data:
            add_cc(crss, data[crss])

    else:
        add_cc(1)
        add_cc(1)
    view.controls.append(courses_cont)

    def new_cor(e):
        add_cc(1)
        rm_btn.disabled = False
        clear_btn.disabled = False
        page.update()

    def rm_cor(e):
        courses_cont.content.controls.pop()
        if len(courses_cont.content.controls) < 3:
            rm_btn.disabled = True
        page.update()

    def get_courses() -> dict:
        dic = {}
        for course in courses_cont.content.controls:
            crscode = course.content.controls[0].value.upper()
            sections = course.content.controls[1].value.split()
            dic[crscode] = sections
        return dic

    def dlg_close(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(modal=True, actions=[
        ft.TextButton("Ok", on_click=dlg_close)],
                         actions_alignment=ft.MainAxisAlignment.END)

    def dlg_open(title, message):
        page.dialog = dlg
        dlg.title = ft.Text(title)
        dlg.content = ft.Text(message)
        dlg.open = True
        page.update()

    def dlg_wait_close():
        dlg_wait.open = False
        page.update()

    dlg_wait = ft.AlertDialog(modal=True)

    def dlg_wait_open():
        page.dialog = dlg_wait
        dlg_wait.content = ft.Row(controls=[ft.ProgressRing(), ft.Text("downloading data...")])
        dlg_wait.open = True
        page.update()

    def valid():
        dlg_wait_open()
        page.client_storage.set("last_fields", get_courses())
        page.update()
        courses = page.session.get("courses") if page.session.contains_key("courses") else courses_data()
        page.session.set("courses", courses)
        flag = True
        message = 'Please Enter valid crscode and sections in:\n'
        for course in courses_cont.content.controls:
            x: ft.TextField
            x = course.content.controls[0]
            if courses.find_course(x.value.upper()) == -1 or course.content.controls[1].value == '':
                message += '-' + x.label.split()[0] + '\n'
                flag = False
        if flag:  # valid inputs
            dlg_wait_close()
            return True
        dlg_open('Error', message)
        page.update()
        return False

    def passing(e):
        pass

    def reset(e):
        courses_cont.content.controls.clear()
        add_cc(1)
        add_cc(1)
        rm_btn.disabled = True
        clear_btn.disabled = True
        page.update()

    rm_btn = ft.ElevatedButton("remove", on_click=rm_cor, disabled=True)
    if page.client_storage.contains_key("last_fields"):
        if len(page.client_storage.get("last_fields")) > 2:
            rm_btn.disabled = False
    add_btn = ft.ElevatedButton("Add", on_click=new_cor)
    clear_btn = ft.ElevatedButton("reset", on_click=reset)
    view.controls.append(ft.Row([add_btn, rm_btn, clear_btn], vertical_alignment=ft.CrossAxisAlignment.CENTER))
    result_btn = ft.ElevatedButton("View Result",
                                   on_click=(lambda _: page.go(f'/tables?{get_courses()}') if valid() else passing))
    view.controls.append(ft.Row([result_btn], vertical_alignment=ft.CrossAxisAlignment.CENTER))
    view.controls.append(ft.Column([
        ft.OutlinedButton("Twitter: @3Mohammed21",
                          on_click=lambda _: page.launch_url("https://twitter.com/3Mohammed21")),
        ft.OutlinedButton("Instagram: @thematrex_007",
                          on_click=lambda _: page.launch_url("https://www.instagram.com/thematrex_007/")),
        ft.OutlinedButton("Github: Mohammed-Alabri",
                          on_click=lambda _: page.launch_url("https://github.com/Mohammed-Alabri"))
    ]))
    view.scroll = ft.ScrollMode.AUTO
    return view


def course_countainer(num, width, crs=None, secs=None):
    if crs is not None and secs is not None:
        row = ft.Row([ft.TextField(label=f"Course{num} code", width=(width // 2 * 4 / 5), value=crs),
                      ft.TextField(label="sections", width=width // 2, value=" ".join(secs))])
    else:
        row = ft.Row([ft.TextField(label=f"Course{num} code", width=(width // 2 * 4 / 5)),
                      ft.TextField(label="sections", width=width // 2)])
    cont = ft.Container(content=row)
    return cont
