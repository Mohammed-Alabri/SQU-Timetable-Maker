import flet as ft
import createTables
from functions import courses_data
import json


def tables_page(page: ft.Page):
    view = ft.View()
    view.theme_mode = ft.ThemeMode.LIGHT
    view.controls.append(ft.AppBar(title=ft.Text("Result"), bgcolor=ft.colors.SURFACE_VARIANT))

    courses = page.session.get("courses") if page.session.contains_key("courses") else courses_data()
    sections = []
    dic = page.route.split('?')[1]
    dic = dic.replace("\'", "\"")
    dic = json.loads(dic)
    for course in dic:
        x = courses.get_sections(course, dic[course])
        if x != -1:
            sections.append(x)

    combs = list(createTables.all_combinations(sections))
    combs = createTables.get_correct_tables(combs)

    def add_table(data: list) -> ft.DataTable:
        rows = []
        table = createTables.print_table(data)[1:]
        for row in table:
            lst = []
            for cell in row:
                lst.append(ft.DataCell(ft.Text(cell)))
            rows.append(ft.DataRow(lst))
        table = ft.DataTable(
            border=ft.border.all(2),
            border_radius=10,
            column_spacing=5,
            vertical_lines=ft.border.BorderSide(1),
            horizontal_lines=ft.border.BorderSide(1),
            # heading_row_color=ft.colors.BLACK12,
            data_row_color={"hovered": "0x30FF0000"},
            columns=[
                ft.DataColumn(
                    ft.Text("Days/\nTimes"),
                ),
                ft.DataColumn(
                    ft.Text("SUN"),
                ), ft.DataColumn(
                    ft.Text("MON"),
                ), ft.DataColumn(
                    ft.Text("TUE"),
                ), ft.DataColumn(
                    ft.Text("WED"),
                ), ft.DataColumn(
                    ft.Text("THU"),
                ),
            ],
            rows=rows)
        return table

    tables_col = ft.Column()

    def print_tabels(tables):
        tables_col.controls.clear()
        if len(tables) > 0:
            for i in tables:
                tablee = add_table(i)
                rr = ft.Row([tablee], scroll=ft.ScrollMode.HIDDEN)
                tables_col.controls.append(rr)
        else:
            tables_col.controls.append(ft.Text("There is no possible table", color="red"))

    fil_days = []
    fil_times = []

    def filtering(e):
        selected = []
        for filtet in fil_days + fil_times:
            if filtet.selected:
                selected.append(filtet.label.value)
        print_tabels(createTables.filters(selected, combs))
        page.update()

    days = ['SUN', 'MON', 'TUE', 'WED', 'THU']
    for day in days:
        x = ft.Chip(label=ft.Text(day),
                    on_select=filtering,
                    )
        fil_days.append(x)
    view.controls.append(ft.Row(fil_days, scroll=ft.ScrollMode.HIDDEN))
    times = ['8', '10', '12', '14', '16']
    for time in times:
        x = ft.Chip(label=ft.Text(time),
                    on_select=filtering,
                    )
        fil_times.append(x)
    view.controls.append(ft.Row(fil_times, scroll=ft.ScrollMode.HIDDEN))
    view.controls.append(tables_col)
    print_tabels(combs)

    view.scroll = ft.ScrollMode.AUTO
    return view
