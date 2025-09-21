import flet as ft


class SpinBox(ft.Container):
    """
    一个数字选择器控件，按钮叠加在输入框上方。
    """

    def __init__(self, label="", min_val=0, max_val=100, initial_value=10, on_change=None, width=150):
        super().__init__()
        self.width = width
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self._value = initial_value
        self.on_change = on_change

        # 创建内部控件
        # 输入框
        self.text_field = ft.TextField(
            value=str(self._value),
            label=self.label,
            text_align=ft.TextAlign.LEFT,
            input_filter=ft.NumbersOnlyInputFilter(),  # 只允许输入数字
            on_submit=self._text_submit,
            # 设置内容的上边距，为按钮留出空间
            content_padding=ft.padding.only(top=20, left=10, right=5, bottom=5),
        )

        # 减号按钮
        self.subtract_button = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            on_click=self.decrement,
            tooltip="减少",
            icon_size=18,
            padding=0,
        )

        # 加号按钮
        self.add_button = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_UP_ROUNDED,
            on_click=self.increment,
            tooltip="增加",
            icon_size=18,
            padding=0,
        )

        # 使用 Stack 布局来实现叠加效果
        self.content = ft.Stack(
            controls=[
                # 第一个控件是 TextField，在最底层
                self.text_field,

                # 第二个控件是包含两个按钮的 Row，叠加在 TextField 之上
                ft.Row(
                    controls=[
                        self.subtract_button,
                        self.add_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    # 调整按钮行的位置，使其位于输入框的顶部区域
                    top=5,
                    left=5,
                    right=5,
                ),
            ]
        )
        self.update_button_states()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        try:
            val = int(new_val)
            # 限制值的范围
            if val < self.min_val:
                val = self.min_val
            elif val > self.max_val:
                val = self.max_val

            if self._value != val:
                self._value = val
                self.text_field.value = str(self._value)
                self.update_button_states()
                if self.on_change:
                    self.on_change(self._value)
        except (ValueError, TypeError):
            # 如果输入无效，则恢复为上一个有效值
            self.text_field.value = str(self._value)

        # 确保UI更新
        if self.page:
            self.page.update()

    def increment(self, e):
        self.value += 1

    def decrement(self, e):
        self.value -= 1

    def _text_submit(self, e):
        self.value = e.control.value

    def update_button_states(self):
        self.subtract_button.disabled = self._value <= self.min_val
        self.add_button.disabled = self._value >= self.max_val
        # 如果控件已在页面上，则请求更新
        if self.page:
            self.subtract_button.update()
            self.add_button.update()