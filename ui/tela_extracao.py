import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.processar_combustivel import selecionar_e_processar_pasta
from utils.icone import usar_icone

class TelaExtracao(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extração de XML")
        self.setGeometry(200, 100, 800, 600)
        usar_icone(self)

        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
                color: white;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                background-color: #E53935;
                color: white;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
            QProgressBar {
                border: 1px solid #333;
                border-radius: 8px;
                background-color: #2e2e2e;
                height: 24px;
                text-align: center;
                font-size: 13px;
            }
            QProgressBar::chunk {
                background-color: #69c458;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)

        # Topo com botão de voltar
        topo_layout = QHBoxLayout()
        btn_voltar = QPushButton("Voltar")
        btn_voltar.setCursor(Qt.PointingHandCursor)
        btn_voltar.setFixedWidth(100)
        btn_voltar.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9C2825;
            }
        """)
        btn_voltar.clicked.connect(self.voltar_para_dashboard)
        topo_layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        layout.addLayout(topo_layout)

        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)

        # Logo
        logo = QLabel()
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            logo.setPixmap(QPixmap(logo_path).scaled(240, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Botão principal
        self.botao_extrair = QPushButton("Selecionar Pasta com XMLs")
        self.botao_extrair.setCursor(Qt.PointingHandCursor)
        self.botao_extrair.clicked.connect(self.iniciar_extracao)
        layout.addWidget(self.botao_extrair, alignment=Qt.AlignCenter)

        # Barra de progresso
        self.barra_progresso = QProgressBar()
        self.barra_progresso.setValue(0)
        layout.addWidget(self.barra_progresso)

    def iniciar_extracao(self):
        self.botao_extrair.setEnabled(False)
        self.barra_progresso.setValue(0)

        def atualizar_barra(valor):
            self.barra_progresso.setValue(int(valor))

        selecionar_e_processar_pasta(atualizar_barra)
        self.botao_extrair.setEnabled(True)

    def voltar_para_dashboard(self):
        from ui.dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.showMaximized()
        self.close()