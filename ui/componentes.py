from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap, QCursor, QFont, QColor, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal, QSize

class RoundedIconButton(QPushButton):
    def __init__(self, icon_path, color="#E53935", hover_color="#C62828", size=36):
        super().__init__()
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size // 2, size // 2))
        self.color = QColor(color)
        self.hover_color = QColor(hover_color)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: {size // 2}px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

class AnimatedCard(QFrame):
    clicked = Signal()

    def __init__(self, icon_path, title, description_list, accent_color="#E53935"):
        super().__init__()
        self.setFixedSize(380, 280)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.accent_color = accent_color
        self.is_hovered = False

        self.setStyleSheet(f"""
            AnimatedCard {{
                background-color: #212121;
                border: 1px solid #2e2e2e;
                border-radius: 12px;
            }}
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 22, 25, 22)
        self.layout.setSpacing(15)

        # Ícone
        self.icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.icon_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.icon_container = QFrame()
        self.icon_container.setFixedSize(80, 80)
        self.icon_container.setStyleSheet("background-color: #ffffff; border-radius: 40px;")
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.addWidget(self.icon_label)

        # Título
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")

        # Descrição
        self.desc_label = QLabel()
        desc_text = "<ul style='margin: 0; padding-left: 18px;'>"
        for item in description_list:
            desc_text += f"<li style='margin-bottom: 6px; color: #bbbbbb;'>{item}</li>"
        desc_text += "</ul>"
        self.desc_label.setText(desc_text)
        self.desc_label.setStyleSheet("font-size: 13px;")
        self.desc_label.setTextFormat(Qt.RichText)
        self.desc_label.setWordWrap(True)

        # Botão
        self.button = QPushButton("Acessar")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent_color};
                color: white;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(accent_color)};
            }}
        """)
        self.button.clicked.connect(self.clicked.emit)

        # Layout do card
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.icon_container)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.desc_label)
        self.layout.addStretch()
        self.layout.addWidget(self.button)

        # Animação de entrada
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(600)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Animação de hover
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)

    def _darken_color(self, color_hex):
        color = QColor(color_hex)
        h, s, v, a = color.getHsv()
        color.setHsv(h, s, max(0, v - 20), a)
        return color.name()

    def enterEvent(self, event):
        self.setStyleSheet(f"""
            AnimatedCard {{
                background-color: #212121;
                border: 1px solid {self.accent_color};
                border-radius: 12px;
            }}
        """)
        rect = self.geometry()
        self.hover_animation.setStartValue(rect)
        self.hover_animation.setEndValue(QRect(rect.x(), rect.y() - 5, rect.width(), rect.height()))
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            AnimatedCard {{
                background-color: #212121;
                border: 1px solid #2e2e2e;
                border-radius: 12px;
            }}
        """)
        rect = self.geometry()
        self.hover_animation.setStartValue(rect)
        self.hover_animation.setEndValue(QRect(rect.x(), rect.y() + 5, rect.width(), rect.height()))
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
