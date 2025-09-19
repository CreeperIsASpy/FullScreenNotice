import flet as ft
from flet import (
    Page,
    TextField,
    Dropdown,
    Text,
    Row,
    Column,
    Container,
    alignment,
    border,
    Colors,
    padding,
    Icons,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from tkinter import colorchooser
from SpinBox import SpinBox


# --- 主应用函数 ---
def main(page: Page):
    # 防止颜色选择器出错的状态锁
    color_picker_open = False

    # =========================================================================
    # 1. 配置初始窗口 (inp_win 的属性)
    # =========================================================================
    page.title = "FullScreenNotice"
    page.window.width = 500
    page.window.height = 420
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    # 设置全局字体
    page.fonts = {
        "Microsoft YaHei": "msyh.ttc"  # 确保你的系统中有这个字体文件，或者提供路径
    }
    page.theme = ft.Theme(font_family="Microsoft YaHei")

    # =========================================================================
    # 2. 定义状态和控件
    # =========================================================================

    # -- 输入视图 (inp_win) 的控件 --

    # 公示文本输入框
    notice_text_field = TextField(
        label="请输入需要全屏公示的文本内容。",
        multiline=True,
        min_lines=3,
        max_lines=5,
    )

    # 字号选择器
    font_size_spinbox = SpinBox(
        label="字号",
        min_val=20,
        max_val=500,
        initial_value=100
    )

    # 颜色选择器相关控件
    # 用于显示当前所选颜色的容器
    color_display = Container(
        width=30,
        height=30,
        bgcolor=Colors.WHITE,
        border=border.all(1, Colors.GREY),
        border_radius=5,
    )
    # 用于存储颜色值的隐藏文本，以便在函数间传递
    selected_color = Text(value=Colors.WHITE, visible=False)

    def open_color_picker(e):
        """打开tkinter颜色选择器并更新UI"""
        nonlocal color_picker_open
        if color_picker_open:
            return  # 防止重复打开颜色选择器

        color_picker_open = True  # 加锁
        try:
            # 打开颜色选择对话框
            color_result = colorchooser.askcolor(
                title="选择公示颜色",
                initialcolor=selected_color.value
            )
            # color_result 是一个元组 ( (r,g,b), '#rrggbb' )
            if color_result and color_result[1]:
                hex_color = color_result[1]
                selected_color.value = hex_color
                color_display.bgcolor = hex_color
                page.update()
        finally:
            color_picker_open = False  # 解锁

    # -- 公示视图 (display_win) 的控件 --

    # 用于显示公示内容的文本控件
    display_label = Text(
        text_align=ft.TextAlign.CENTER,
        font_family="Microsoft YaHei"
    )

    # --- 函数：视图切换 ---

    def start_display(e):
        """切换到公示视图"""
        # 1. 更新公示文本控件的内容、字号和颜色
        display_label.value = notice_text_field.value or "（无内容）"
        display_label.size = int(font_size_spinbox.value)
        display_label.color = selected_color.value

        # 2. 清空页面现有控件
        page.controls.clear()

        # 3. 配置页面为全屏、无边框、黑色背景
        page.window.full_screen = True
        page.window_frameless = True
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = Colors.BLACK
        page.padding = padding.all(20)
        page.vertical_alignment = MainAxisAlignment.CENTER
        page.horizontal_alignment = CrossAxisAlignment.CENTER
        page.window_always_on_top = True  # 置顶

        # 4. 构建并加载公示视图的控件
        page.add(
            # 使用Column来居中文本并让关闭按钮在最下方
            Column(
                controls=[
                    # 包含文本的容器，使其能够扩展并居中
                    Container(
                        content=display_label,
                        alignment=alignment.center,
                        expand=True,  # 占据所有可用垂直空间
                    ),
                    # 关闭按钮
                    ft.ElevatedButton(
                        text="关闭",
                        on_click=close_display,
                    )
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True
            )
        )
        page.update()

    def build_input_view():
        """构建输入视图的布局"""
        # 将字号和颜色选择器放入一个水平行中
        color_row = Row(
            controls=[
                color_display,
                ft.FilledButton("选择", icon=Icons.COLOR_LENS_OUTLINED, on_click=open_color_picker, expand=True)
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )

        settings_row = Row(
            controls=[
                # 让下拉框占据大部分空间
                font_size_spinbox,
                color_row
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=40,
        )

        launcher_row = Row(
            controls=[
                ft.ElevatedButton("退出", on_click=lambda _: page.window.close(), expand=True),  # <--- expand=True
                ft.FilledButton("开始公示", on_click=start_display, expand=True),  # <--- expand=True
            ],
            spacing=20,
        )

        return Column(
            controls=[
                notice_text_field,
                settings_row,
                launcher_row
            ],
            spacing=20,  # 控件之间的垂直间距
        )

    def close_display(e):
        """从公示视图切换回输入视图"""
        # 1. 清空页面现有控件
        page.controls.clear()

        # 2. 恢复页面的标准窗口属性
        page.window.full_screen = False
        page.window_frameless = False
        page.bgcolor = None  # 恢复默认背景
        page.padding = padding.all(10)
        page.vertical_alignment = MainAxisAlignment.START
        page.horizontal_alignment = CrossAxisAlignment.START
        page.window_always_on_top = False

        # 3. 重新加载输入视图
        page.add(build_input_view())
        page.update()

    # =========================================================================
    # 3. 初始加载
    # =========================================================================

    # 首次启动时，加载输入视图
    page.add(build_input_view())


# --- 运行 Flet 应用 ---
if __name__ == "__main__":
    ft.app(target=main)
