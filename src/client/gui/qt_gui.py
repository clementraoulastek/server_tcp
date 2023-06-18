import io
import logging
import sys
import time
from threading import Thread
from typing import Union
from src.client.client import Client
from src.client.gui.customWidget.CustomQLabel import RoundedLabel
from src.client.gui.customWidget.CustomQLineEdit import CustomQLineEdit
from src.client.gui.customWidget.CustomQPushButton import CustomQPushButton
from src.client.gui.layout.login_layout import LoginLayout
from src.client.gui.layout.message_layout import MessageLayout
from src.client.gui.stylesheets import scroll_bar_vertical_stylesheet
from src.client.core.qt_core import (
    QApplication,
    QHBoxLayout,
    QIcon,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSize,
    Qt,
    QThread,
    QVBoxLayout,
    QWidget,
    Signal,
)
from src.tools.backend import Backend
from src.tools.constant import IP_API, IP_SERVER, PORT_API, PORT_NB, SOFT_VERSION
from src.tools.utils import Color, Icon, ImageAvatar, QIcon_from_svg
from src.tools.commands import Commands


class Worker(QThread):
    """Tricks to update the GUI with deamon thread

    Args:
        QThread (QThread): Thread
    """

    signal = Signal()

    def __init__(self, polling_interval=0.01):
        super(Worker, self).__init__()
        self._is_running = True
        self.polling_interval = polling_interval

    def run(self):
        if not self._is_running:
            self._is_running = True

        while self._is_running:
            self.signal.emit()
            time.sleep(self.polling_interval)

    def stop(self):
        self.terminate()
        self.exit()
        self._is_running = False


# Global variable to handle worker
comming_msg = {"id": "", "message": ""}
coming_user = {"username": "", "content": ""}


class QtGui:
    def __init__(self, title):
        self.app = QApplication([])
        self.main_window = MainWindow(title)
        self.app.setWindowIcon(QIcon(ImageAvatar.SERVER.value))
        self.app.setApplicationName(title)
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())


class MainWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        # GUI size
        self.setFixedHeight(600)
        self.setFixedWidth(850)
        self.setWindowTitle(title)

        self.users_pict = {"server": ImageAvatar.SERVER.value}

        # Create Client socket
        self.client = Client(IP_SERVER, PORT_NB, "Default")

        # Create backend conn
        self.backend = Backend(self, IP_API, PORT_API)

        # GUI settings
        self.setup_gui()

    def setup_gui(self):
        """
        Add elements to the main window
        """
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet(f"background-color: {Color.DARK_GREY.value};")
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_widget.setLayout(self.main_layout)

        self.set_header_gui()
        self.set_core_gui()
        self.set_footer_gui()

        self.login()

    def set_header_gui(self):
        """
        Update the header GUI
        """

        # --- Background
        server_status_widget = QWidget()
        server_status_widget.setStyleSheet(
            f"background-color: {Color.GREY.value};color: {Color.LIGHT_GREY.value};border-radius: 14px"
        )
        self.status_server_layout = QHBoxLayout(server_status_widget)
        self.status_server_layout.setSpacing(20)
        self.status_server_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

        # --- Server information
        self.server_info_widget = QWidget()
        self.server_info_widget.setStyleSheet(
            f"background-color: {Color.DARK_GREY.value};color: {Color.LIGHT_GREY.value};border-radius: 14px"
        )
        self.server_information_dashboard_layout = QHBoxLayout(self.server_info_widget)

        icon_soft = RoundedLabel(content=ImageAvatar.SERVER.value)
        status_server_label = QLabel(f"version: {SOFT_VERSION}")

        # Adding widgets to the main layout
        self.server_information_dashboard_layout.addWidget(icon_soft)
        self.server_information_dashboard_layout.addWidget(status_server_label)

        # --- Client information
        self.user_info_widget = QWidget()
        self.client_information_dashboard_layout = QHBoxLayout(self.user_info_widget)
        self.user_info_widget.setStyleSheet(
            f"background-color: {Color.DARK_GREY.value};color: {Color.LIGHT_GREY.value};border-radius: 14px"
        )
        self.user_icon = QIcon(QIcon_from_svg(Icon.USER_ICON.value)).pixmap(
            QSize(30, 30)
        )

        self.custom_user_button = CustomQPushButton(
            "Update user picture",
        )

        self.user_picture = RoundedLabel(content="")
        self.user_name = QLabel("User disconnected")

        self.user_name.setStyleSheet("font-weight: bold")

        self.custom_user_button.setIcon(self.user_icon)
        self.custom_user_button.clicked.connect(self.send_user_icon)
        self.custom_user_button.setEnabled(False)

        self.client_information_dashboard_layout.addWidget(self.custom_user_button)
        self.client_information_dashboard_layout.addWidget(self.user_name)
        self.client_information_dashboard_layout.addWidget(self.user_picture)

        self.status_server_layout.addWidget(self.server_info_widget)
        self.status_server_layout.addWidget(self.user_info_widget)

        self.main_layout.addWidget(server_status_widget)

    def scrollToBottom(self):
        """
        Update the scrollbar vertical position to the bottom
        """
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def set_core_gui(self):
        """
        Update the core GUI
        """
        self.core_layout = QHBoxLayout()
        
        # --- Left layout with scroll area
        self.info_layout = QVBoxLayout()
        self.info_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.scroll_area_avatar = QScrollArea()
        self.scroll_area_avatar.setFixedWidth(self.scroll_area_avatar.width()/3 +13)

        self.scroll_widget_avatar = QWidget()
        self.scroll_widget_avatar.setFixedWidth(self.scroll_widget_avatar.width() / 3)
        self.scroll_widget_avatar.setStyleSheet(
            f"font-weight: bold; color: {Color.LIGHT_GREY.value};background-color: {Color.GREY.value};border-radius: 14px"
        )
        
        self.scroll_area_avatar.verticalScrollBar().setStyleSheet(
            scroll_bar_vertical_stylesheet
        )
        self.scroll_area_avatar.setStyleSheet("background-color: transparent;color: white")
        self.scroll_area_avatar.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area_avatar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_avatar.setWidgetResizable(True)

        self.scroll_widget_avatar.setLayout(self.info_layout)
        self.scroll_area_avatar.setWidget(self.scroll_widget_avatar)
        
        
        self.info_label = QLabel("Please login")
        self.info_label.setContentsMargins(10, 5, 10, 5)
        self.info_label.setStyleSheet(
            f"font-weight: bold; color: {Color.LIGHT_GREY.value};background-color: {Color.DARK_GREY.value};border-radius: 8px"
        )
        self.info_layout.addWidget(self.info_label)

        
        # --- Right layout with scroll area
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setObjectName("scroll layout")

        self.scroll_area = QScrollArea()
        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scrollToBottom)

        self.scroll_area.setContentsMargins(0, 0, 90, 0)
        self.scroll_area.setMaximumHeight(380)
        self.scroll_area.setMinimumHeight(380)

        self.scroll_widget = QWidget()
        self.scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.verticalScrollBar().setStyleSheet(
            scroll_bar_vertical_stylesheet
        )
        self.scroll_area.setStyleSheet("background-color: transparent;color: white")
        self.scroll_area.setObjectName("scroll_feature")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        
        self.core_layout.addWidget(self.scroll_area_avatar)
        self.core_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(self.core_layout)
        self.main_layout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

    def set_footer_gui(self):
        """
        Update the footer GUI
        """
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
        self.button_layout.setObjectName("button layout")
        self.button_layout.setSpacing(5)

        self.clear_button = CustomQPushButton("")
        self.clear_button.clicked.connect(self.clear)
        self.clear_icon = QIcon(QIcon_from_svg(Icon.CLEAR.value))
        self.clear_button.setIcon(self.clear_icon)
        self.clear_button.setDisabled(True)

        self.login_button = CustomQPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_icon = QIcon(QIcon_from_svg(Icon.LOGIN.value))
        self.login_button.setIcon(self.login_icon)

        self.logout_button = CustomQPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.logout_icon = QIcon(QIcon_from_svg(Icon.LOGOUT.value))
        self.logout_button.setIcon(self.logout_icon)
        self.logout_button.setDisabled(True)

        self.config_button = CustomQPushButton("")
        self.config_button.clicked.connect(self.config)
        self.settings_icon = QIcon(QIcon_from_svg(Icon.CONFIG.value))
        self.config_button.setFixedWidth(50)
        self.config_button.setIcon(self.settings_icon)

        info_widget = QWidget()
        info_widget.setStyleSheet(
            f"background-color: {Color.GREY.value};border-radius: 14px"
        )

        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.logout_button)
        self.button_layout.addWidget(self.config_button)
        self.button_layout.addWidget(info_widget)

        self.main_layout.addLayout(self.button_layout)

        self.send_layout = QHBoxLayout()
        self.send_layout.setObjectName("send layout")
        self.send_layout.setSpacing(5)

        self.entry = CustomQLineEdit(place_holder_text="Please login")
        self.entry.returnPressed.connect(self.send_messages)
        self.entry.setDisabled(True)
        self.send_layout.addWidget(self.entry)

        self.send_button = CustomQPushButton("")
        self.send_button.clicked.connect(self.send_messages)
        self.send_icon = QIcon(QIcon_from_svg(Icon.SEND.value))
        self.send_button.setIcon(self.send_icon)
        self.send_button.setDisabled(True)

        self.send_layout.addWidget(self.send_button)
        self.main_layout.addLayout(self.send_layout)

    def close_connection(self, *args) -> None:
        """
        Close the socket and destroy the gui
        """
        if hasattr(self.client, "sock"):
            self.client.close_connection()
            logging.debug("Client disconnected")
        else:
            logging.debug("GUI closed")
            self.destroy()
            sys.exit(0)

    def send_messages(self, *args) -> None:
        """
            Send message to the server

        Args:
            signal (event): event coming from signal
        """
        if message := self.entry.text():
            self.client.send_data(message)
            self._diplay_message_after_send(self.client.user_name, message)

    def _diplay_message_after_send(self, id_sender: str, message: str) -> None:
        """
            Display message on gui and clear the entry

        Args:
            id_sender (str): id from the sender
            message (str): message to display
        """
        comming_msg = {"id": id_sender, "message": message}
        self.scroll_layout.addLayout(
            MessageLayout(comming_msg, content=self.users_pict[self.client.user_name])
        )

        self.entry.clear()

    def parse_coming_message(self, message: str):
        """
            Display message on gui and clear the entry

        Args:
            message (str): message to display
        """
        global comming_msg
        if ":" in message:
            if Commands.CONN_NB.value in message:
                nb_of_users = message.split(Commands.CONN_NB.value)[1]
                self.info_label.setText(f"Nb of users connected: {nb_of_users}")
                return
            elif Commands.HELLO_WORLD.value in message:
                id_, _ = message.split(":", 1)
                self.add_sender_picture(id_)
                # Return welcome to hello world
                self.client.send_data(Commands.WELCOME.value)
                return
            elif Commands.WELCOME.value in message:
                id_, _ = message.split(":", 1)
                self.add_sender_picture(id_)
                return
            elif Commands.GOOD_BYE.value in message:
                id_, _ = message.split(":", 1)
                self.clear_avatar(f"{id_}_layout")
                self.users_pict.pop(id_)
                return
            comming_msg["id"], comming_msg["message"] = message.split(":", 1)
        else:
            comming_msg["id"], comming_msg["message"] = "unknown", message

    def update_gui_with_input_messages(self):
        """
        Callback to update gui with input messages
        """
        global comming_msg
        if comming_msg["message"]:
            self.scroll_layout.addLayout(
                MessageLayout(comming_msg, content=self.users_pict[comming_msg["id"]])
            )
            comming_msg["id"], comming_msg["message"] = "", ""

    def update_gui_with_input_avatar(self):
        """
        Callback to update gui with input avatar
        """
        global coming_user
        if coming_user[
            "content"
        ]:  # and coming_user["username"] not in list(self.users_pict.keys()):
            user_layout = QHBoxLayout()
            username = coming_user["username"]
            content = coming_user["content"]
            user_layout.setObjectName(f"{username}_layout")
            user_layout.addWidget(RoundedLabel(content=content))
            user_layout.addWidget(QLabel(username))
            self.info_layout.addLayout(user_layout)
            coming_user["username"], coming_user["content"] = "", ""

    def read_messages(self):
        """
        Read message comming from server
        """
        while self.client.is_connected:
            if message := self.client.read_data():
                self.parse_coming_message(message)
            time.sleep(0.1)

    def clear(self):
        """
        Clear the entry
        """
        for i in reversed(range(self.scroll_layout.count())):
            layout = self.scroll_layout.itemAt(i).layout()
            for j in reversed(range(layout.count())):
                layout.itemAt(j).widget().deleteLater()
        self.scroll_layout.update()

    def clear_avatar(self, layout_name: Union[QHBoxLayout, None] = None):
        """
        Clear the entry
        """
        for i in reversed(range(self.info_layout.count())):
            if layout := self.info_layout.itemAt(i).layout():
                if (
                    layout_name
                    and layout_name == layout.objectName()
                    or not layout_name
                ):
                    for j in reversed(range(layout.count())):
                        layout.itemAt(j).widget().deleteLater()
                                        
        self.info_layout.update()

    def login(self) -> None:
        """
        Display the login form
        """
        self.clear()
        if not hasattr(self, "login_form") or not self.login_form:
            self.login_form = LoginLayout()
            self.scroll_layout.addLayout(self.login_form)
            self.login_form.send_button.clicked.connect(self.send_login_form)
            self.login_form.register_button.clicked.connect(self.send_register_form)

        self.login_button.setDisabled(True)
        self.clear_button.setDisabled(True)

    def send_login_form(self):
        """
        Backend request for login form
        """
        username = self.login_form.username_entry.text().replace(" ", "")
        password = self.login_form.password_entry.text().replace(" ", "")
        if not username or not password:
            return

        if self.backend.send_login_form(username, password):
            if username:  # Check if username not empty
                self.client.user_name = username

            self._clean_gui_and_connect(update_avatar=True)

    def send_register_form(self):
        """
        Backend request for register form
        """
        username = self.login_form.username_entry.text().replace(" ", "")
        password = self.login_form.password_entry.text().replace(" ", "")
        if not username or not password:
            return

        if self.backend.send_register_form(username, password):
            if username:
                self.client.user_name = username

            self._clean_gui_and_connect(update_avatar=False)

    def send_user_icon(self, picture_path=None):
        """
        Backend request for sending user icon
        """
        username = self.client.user_name
        if self.backend.send_user_icon(username, picture_path):
            self.get_user_icon(update_avatar=True)

    def get_user_icon(self, username=None, update_avatar=False):
        """
        Backend request for getting user icon
        """
        if not username:
            username = self.client.user_name
        if content := self.backend.get_user_icon(username):
            self.users_pict[username] = content
            if update_avatar:
                self.user_picture.update_picture(content=content)
            global coming_user
            coming_user["username"], coming_user["content"] = username, content
        else:
            self.users_pict[username] = ""

    def add_sender_picture(self, sender_id):
        """Add sender picture to the list of sender pictures

        Args:
            sender_id (str): sender identifier
        """
        if sender_id not in list(self.users_pict.keys()):
            self.get_user_icon(sender_id)

    def _clean_gui_and_connect(self, update_avatar: bool) -> None:
        if self.connect_to_server():
            self.login_form = None
            self.clear_button.setDisabled(False)
            self.clear()
            self.get_user_icon(update_avatar=update_avatar)

    def connect_to_server(self) -> bool:
        self.client.init_connection()
        if self.client.is_connected:
            # Worker for incoming messages
            self.read_worker = Worker()
            self.read_worker.signal.connect(self.update_gui_with_input_messages)
            self.read_worker.start()

            # Worker for incoming avatar
            self.read_avatar_worker = Worker()
            self.read_avatar_worker.signal.connect(self.update_gui_with_input_avatar)
            self.read_avatar_worker.start()

            self.worker_thread = Thread(target=self.read_messages, daemon=True)
            self.worker_thread.start()
            self.update_buttons()
            return True
        else:
            self.parse_coming_message("Server off")
            return False

    def logout(self) -> None:
        """
        Disconnect the client
        """
        self.client.close_connection()
        self.update_buttons()
        self.clear_avatar()
        self.users_pict = {"server": ImageAvatar.SERVER.value}

    def config(self):
        """
        Display the config
        """
        config = f"User name = '{self.client.user_name}' Client host = '{self.client.host}' Client port = '{self.client.port}'"
        comming_msg = {"id": "server", "message": config}
        self.scroll_layout.addLayout(
            MessageLayout(comming_msg, content=ImageAvatar.SERVER.value)
        )

    def update_buttons(self):
        if self.client.is_connected:
            self._set_buttons_status(True, False, "Enter your message")
            self.user_name.setText(self.client.user_name)
        else:
            self._set_buttons_status(False, True, "Please login")
            self.user_name.setText("User disconnected")
            self.info_label.setText("Please login")
            self.user_picture.update_picture(content="")

    def _set_buttons_status(self, arg0, arg1, lock_message):
        self.custom_user_button.setDisabled(arg1)
        self.login_button.setDisabled(arg0)
        self.logout_button.setDisabled(arg1)
        self.send_button.setDisabled(arg1)
        self.entry.setDisabled(arg1)
        self.entry.setPlaceholderText(lock_message)
