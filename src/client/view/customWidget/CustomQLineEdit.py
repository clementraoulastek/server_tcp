from src.client.core.qt_core import (
    QLineEdit,
    Qt,
    Signal,
    QToolButton,
    QGraphicsDropShadowEffect,
    QColor,
)
from src.tools.utils import Color

style = """
QLineEdit {{
	background-color: {_bg_color};
	border-radius: {_radius}px;
	border: {_border_size}px solid {_context_color};
	padding-left: 10px;
    padding-right: 5px;
	selection-color: {_selection_color};
	selection-background-color: {_context_color};
    color: {_color};
}}
QLineEdit:focus {{
	border: {_border_size}px solid {_context_color};
    background-color: {_bg_color_active};
}}
"""

style_rounded = """
QLineEdit {{
	background-color: {_bg_color};
	border-radius: {_radius}px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
	border: {_border_size}px solid {_context_color};
    border-bottom: 0px solid;
	padding-left: 10px;
    padding-right: 5px;
	selection-color: {_selection_color};
	selection-background-color: {_context_color};
    color: {_color};
}}
QLineEdit:focus {{
	border: {_border_size}px solid {_context_color};
    border-bottom: 0px solid;
    background-color: {_bg_color_active};
}}
"""


class CustomQLineEdit(QLineEdit, QToolButton):
    def __init__(
        self,
        text="",
        place_holder_text="",
        radius=12,
        border_size=0,
        color=Color.LIGHT_GREY.value,
        selection_color="#FFF",
        bg_color=Color.DARK_GREY.value,
        bg_color_active=Color.DARK_GREY.value,
        context_color=Color.MIDDLE_GREY.value,
    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        self.setFixedHeight(40)

        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color,
        )

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        context_color,
    ):
        # APPLY STYLESHEET
        self.style_format = style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color,
        )
        self.setStyleSheet(self.style_format)

    def widget_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 2)
        shadow.setBlurRadius(1)
        self.setGraphicsEffect(shadow)
        
    def update_layout(self):
        # APPLY STYLESHEET
        style_format = style_rounded.format(
            _radius=12,
            _border_size=1,
            _color=Color.LIGHT_GREY.value,
            _selection_color="#FFF",
            _bg_color=Color.LIGHT_BLACK.value,
            _bg_color_active=Color.LIGHT_BLACK.value,
            _context_color=Color.MIDDLE_GREY.value,
        )
        self.setStyleSheet(style_format)
        
    def reset_layout(self):
        self.setStyleSheet(self.style_format)
