from src.client.core.qt_core import (
    QScrollArea,
    Qt,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)
from src.client.view.stylesheets.stylesheets import scroll_bar_vertical_stylesheet
from src.tools.utils import Themes, check_str_len

theme = Themes()

class BodyScrollArea(QScrollArea):
    def __init__(self, name: str):
        """
        Update the core GUI
        """
        super(BodyScrollArea, self).__init__()

        self.name = name

        # ----------------- Main Layout ----------------- #
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName(f"{name}_layout")

        self.partial_name = check_str_len(name)

        # ----------------- Scroll Area ----------------- #
        self.setMinimumWidth(600)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(380)

        self.scroll_widget = QWidget()
        self.scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.verticalScrollBar().setStyleSheet(scroll_bar_vertical_stylesheet.format(_background_color=theme.background_color))
        self.setStyleSheet(
            "background-color: transparent;\
            color: white;\
            border: 0px"
        )
        self.setObjectName(name)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.is_auto_scroll_ = True
        self.verticalScrollBar().actionTriggered.connect(self.is_auto_scroll)
        self.verticalScrollBar().rangeChanged.connect(self.update_scrollbar)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.scroll_widget.setLayout(self.main_layout)
        self.setWidget(self.scroll_widget)

    def is_auto_scroll(self):
        """
        Check if the scrollbar is at the bottom
        """
        self.is_auto_scroll_ = (
            self.verticalScrollBar().value() == self.verticalScrollBar().maximum()
        )

    def update_scrollbar(self):
        """
        If the scrollbar is at the bottom, update it to the bottom
        """
        if self.is_auto_scroll_:
            self.scrollToBottom()

    def scrollToBottom(self):
        """
        Update the scrollbar vertical position to the bottom
        """
        scroll_bar = self.verticalScrollBar()
        scroll_bar.updateGeometry()
        scroll_bar.setValue(scroll_bar.maximum())

    def def_upper_widget(self):
        self.upper_widget = QWidget()
        self.upper_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.upper_widget.setStyleSheet(
            f"background-color: {self.theme.background_color};\
            border-radius: 0px;\
            border: 0px solid {self.theme.nav_color}; "
        )
        upper_layout = QHBoxLayout()
        self.upper_widget.setLayout(upper_layout)

        frame_name = QLabel(f"#{self.name.capitalize()}")
        frame_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_name.setStyleSheet(
            f"color: {self.theme.title_color};\
            font-weight: bold;\
            border: 0px solid;"
        )
        upper_layout.addWidget(frame_name)
        self.main_layout.addWidget(self.upper_widget)
        if self.name == "home":
            self.upper_widget.hide()
