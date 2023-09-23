from enum import Enum, unique
from typing import Optional
from src.client.core.qt_core import (
    QPixmap,
    QLabel,
    QIcon,
    QSize,
    QColor,
    Qt,
    QPainter,
    QBrush,
    QPoint,
    QPen,
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
    QStaticText,
)


@unique
class AvatarStatus(Enum):
    DEACTIVATED = 0
    ACTIVATED = 1
    IDLE = 2
    DM = 3


class AvatarLabel(QLabel):
    def __init__(
        self,
        *args,
        content=None,
        height=40,
        width=40,
        color=None,
        status=AvatarStatus.IDLE,
        background_color=QColor(49, 51, 56),
    ):
        super(AvatarLabel, self).__init__(*args)
        self.color = color
        self.height_ = height
        self.width_ = width
        self.content = content
        self.update_picture(status, background_color)
        self.setStyleSheet("border: none")

    def update_picture(self, status: AvatarStatus, background_color: Optional[QColor] = QColor(49, 51, 56), content: Optional[bytes] = None) -> None:
        if content:
            self.content = content
        if isinstance(self.content, str):
            p = QIcon(self.content).pixmap(QSize(self.height_, self.width_))
            if self.color:
                painter = QPainter(p)
                painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter.fillRect(p.rect(), QColor(self.color))
                painter.end()
            self.setPixmap(p)
        else:
            self.update_icon_status(status, background_color)

    def update_icon_status(
        self, status: AvatarStatus, background_color: QColor
    ) -> None:
        icon_pixmap = self.__init_pixmap()
        if status == AvatarStatus.IDLE:
            self.setPixmap(icon_pixmap)
            return

        painter = self.__create_painter(icon_pixmap)
        if status == AvatarStatus.ACTIVATED:
            brush_color = self._update_circle_color(74, 160, 50)
        elif status == AvatarStatus.DEACTIVATED:
            brush_color = self._update_circle_color(154, 152, 147)
        elif status == AvatarStatus.DM:
            brush_color = self._update_circle_color(255, 0, 0)
        self.__create_ellipse(painter, background_color, brush_color, icon_pixmap)

    def _update_circle_color(self, r, g, b):
        return QColor(r, g, b)

    def widget_shadow(self) -> None:
        """
        Update shadow
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 2)
        shadow.setBlurRadius(1)
        return shadow

    def set_opacity(self, opacity: int) -> None:
        """
        Update opacity

        Args:
            opacity (int): opacity value
        """
        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(opacity)
        self.setGraphicsEffect(opacity_effect)

    def update_pixmap(
        self, status: AvatarStatus, background_color=QColor(49, 51, 56)
    ) -> None:
        """
        Update pixmap of the icon

        Args:
            status (AvatarStatus): avatar status
        """
        icon_pixmap = self.__init_pixmap()
        painter = self.__create_painter(icon_pixmap)
        if status == AvatarStatus.ACTIVATED:
            brush_color = self._update_circle_color(74, 160, 50)
        elif status == AvatarStatus.DM:
            brush_color = self._update_circle_color(255, 0, 0)
        elif status == AvatarStatus.DEACTIVATED:
            brush_color = self._update_circle_color(154, 152, 147)
        elif status == AvatarStatus.IDLE:
            painter.end()
            self.setPixmap(icon_pixmap)
            return

        self.__create_ellipse(painter, background_color, brush_color, icon_pixmap)

    def __create_painter(self, icon_pixmap: QPixmap) -> QPainter:
        result = QPainter(icon_pixmap)
        result.setRenderHint(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        result.drawPixmap(0, 0, icon_pixmap)
        return result

    def __init_pixmap(self) -> QPixmap:
        pm = QPixmap()
        pm.loadFromData(self.content)
        return QIcon(pm).pixmap(QSize(self.height_, self.width_))

    def __create_ellipse(
        self,
        painter: QPainter,
        outer_brush_color: QColor,
        inner_brush_color: QColor,
        icon_pixmap: QPixmap,
    ) -> None:
        painter.setPen(QPen(Qt.NoPen))
        circle_radius = 8 if self.height_ >= 40 else 4
        circle_center = QPoint(
            self.width_ - 1 * circle_radius, self.height_ - circle_radius * 1
        )

        self.__draw_ellipse(outer_brush_color, painter, circle_center, circle_radius)

        inner_radius = circle_radius / 2
        inner_center = circle_center

        self.__draw_ellipse(inner_brush_color, painter, inner_center, inner_radius)
        painter.end()
        self.setPixmap(icon_pixmap)

    def __draw_ellipse(self, arg0, painter, arg2, arg3):
        outer_brush = QBrush(arg0)
        painter.setBrush(outer_brush)
        painter.drawEllipse(arg2, arg3, arg3)
