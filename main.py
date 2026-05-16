import flet as ft
from my_logic import run_math

def main(page: ft.Page):
    page.title = "Excel Analyzer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- UI Elements ---
    title = ft.Text("📊 Excel Analyzer", size=30, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Select an Excel file to begin.", color=ft.colors.BLUE_GREY)
    
    result_card = ft.Card(
        visible=False,
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Calculation Results:", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(id="result_output", value="")
            ])
        )
    )

    # --- Logic ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            file_name = e.files[0].name
            
            # Update UI to show processing
            status_text.value = f"Processing: {file_name}..."
            status_text.color = ft.colors.BLUE
            result_card.visible = False
            page.update()
            
            try:
                # Run your math logic
                output_string = run_math(file_path)
                
                # Show results
                result_card.content.content.controls[1].value = str(output_string)
                result_card.visible = True
                status_text.value = "Success!"
                status_text.color = ft.colors.GREEN
                
            except Exception as err:
                status_text.value = f"Error in math logic: {str(err)}"
                status_text.color = ft.colors.RED
                
            page.update()
        else:
            status_text.value = "File selection cancelled."
            status_text.color = ft.colors.RED
            page.update()

    # --- File Picker Setup ---
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # --- Upload Button ---
    upload_btn = ft.ElevatedButton(
        text="Upload Excel File",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx", "xls"]),
        style=ft.ButtonStyle(padding=20)
    )

    # --- Build Page ---
    page.add(
        title,
        ft.Divider(),
        upload_btn,
        status_text,
        result_card
    )

ft.app(target=main)