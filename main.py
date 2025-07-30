import flet as ft
from db.shopdb import ShopDB

db = ShopDB()

def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START

    item_list = ft.Column(spacing=10)
    item_input = ft.TextField(label="Новый товар", expand=True)
    counter_text = ft.Text("Куплено: 0 из 0", style="bodyMedium")

    def update_counter():
        total = len(item_list.controls)
        bought = sum(row.controls[0].value for row in item_list.controls)
        counter_text.value = f"Куплено: {bought} из {total}"
        page.update()

    def toggle_item(item_id, value):
        db.update_status(item_id, value)
        update_counter()

    def delete_item(item_id, row):
        db.delete_item(item_id)
        item_list.controls.remove(row)
        update_counter()
        page.update()

    def create_item_row(item_id, name, bought):
        checkbox = ft.Checkbox(
            value=bool(bought),
            on_change=lambda e: toggle_item(item_id, e.control.value)
        )
        text = ft.Text(name)

        row = ft.Row([
            checkbox,
            text,
            ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Удалить",
                icon_color=ft.Colors.RED,
                on_click=lambda e: delete_item(item_id, row)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return row

    def add_item(e):
        if item_input.value.strip():
            item_id = db.add_item(item_input.value.strip())
            row = create_item_row(item_id, item_input.value.strip(), False)
            item_list.controls.append(row)
            item_input.value = ""
            update_counter()
            page.update()

    def load_items():
        for item_id, name, bought in db.get_items():
            item_list.controls.append(create_item_row(item_id, name, bought))
        update_counter()

    add_button = ft.ElevatedButton("Добавить", on_click=add_item)

    page.add(
        ft.Text("Список покупок", style="headlineMedium"),
        ft.Row([item_input, add_button]),
        counter_text,
        item_list
    )

    load_items()

ft.app(target=main)
