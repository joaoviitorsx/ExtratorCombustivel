import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.icone import usar_icone
from utils.conversor_planilha import converter_planilha
from utils.mensagem import mensagem_sucesso, mensagem_error

class TelaConversor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de Planilha - NFSe")
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
                background-color: #1E88E5;
                color: white;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
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

        # Botões
        btn_converter = QPushButton("Selecionar Planilha para Conversão")
        btn_converter.setCursor(Qt.PointingHandCursor)
        btn_converter.clicked.connect(self.iniciar_conversao)
        layout.addWidget(btn_converter, alignment=Qt.AlignCenter)

    def iniciar_conversao(self):
        try:
            arquivo_entrada, _ = QFileDialog.getOpenFileName(self, "Selecionar planilha original (.xls)", "", "Arquivos Excel (*.xls *.xlsx)")
            if not arquivo_entrada:
                return

            caminho_saida, _ = QFileDialog.getSaveFileName(self, "Salvar nova planilha", "", "Arquivos Excel (*.xlsx)")
            if not caminho_saida:
                return

            converter_planilha(arquivo_entrada, caminho_saida)
            mensagem_sucesso("Conversão finalizada com sucesso!")

        except Exception as e:
            mensagem_error(f"Erro ao converter planilha:\n{str(e)}")

    def voltar_para_dashboard(self):
        from ui.dashboard import Dashboard
        self.dashboard = Dashboard()
        self.dashboard.showMaximized()
        self.close()
