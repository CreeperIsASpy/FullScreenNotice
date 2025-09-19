import flet as ft


class SpinBox(ft.Container):
    """数字选择器控件"""
    def __init__(self, label="", min_val=0, max_val=100, initial_value=10, on_change=None):
        super().__init__()
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self._value = initial_value
        self.on_change = on_change

        # 创建内部控件
        self.text_field = ft.TextField(
            value=str(self._value),
            label=self.label,
            width=80,
            text_align=ft.TextAlign.CENTER,
            input_filter=ft.NumbersOnlyInputFilter(),  # 只允许输入数字
            on_submit=self._text_submit,
        )

        self.subtract_button = ft.IconButton(
            icon=ft.Icons.REMOVE, on_click=self.decrement, tooltip="减少"
        )
        self.add_button = ft.IconButton(
            icon=ft.Icons.ADD, on_click=self.increment, tooltip="增加"
        )

        # 使用 Row 组合内部控件
        self.content = ft.Row(
            controls=[
                self.subtract_button,
                self.text_field,
                self.add_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )
        self.update_button_states()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        try:
            val = int(new_val)
            if self.min_val <= val <= self.max_val:
                self._value = val
                self.text_field.value = str(val)
                self.update_button_states()
                if self.on_change:
                    self.on_change(self._value)
            # 如果值超出范围，则不更新，可以根据需要添加错误提示
        except (ValueError, TypeError):
            # 如果输入无效，则恢复为上一个有效值
            self.text_field.value = str(self._value)

    def increment(self, e):
        self.value += 1
        self.page.update()

    def decrement(self, e):
        self.value -= 1
        self.page.update()

    def _text_submit(self, e):
        self.value = e.control.value
        self.page.update()

    def update_button_states(self):
        self.subtract_button.disabled = self._value <= self.min_val
        self.add_button.disabled = self._value >= self.max_val
