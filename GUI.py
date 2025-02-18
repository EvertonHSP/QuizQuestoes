from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QStackedWidget,
    QFrame,
    QGridLayout  # Adicione esta linha
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt
from PIL import Image
from io import BytesIO
from PyQt5.QtWidgets import QFrame
from datetime import datetime


class InterfaceApp(QMainWindow):

    def __init__(self, intermediary_manager):
        super().__init__()
        self.intermediary_manager = intermediary_manager
        self.current_question = None
        self.questoes_sugeridas = []
        self.modo_sugestao = False
        self.id_usuario = None

        # Configurações iniciais da janela
        self.setWindowTitle("Quiz App")
        self.setGeometry(100, 100, 800, 600)

        self.background_image_path = "bg.jpg"  # Substitua pelo caminho da imagem
        self.set_background_image(self.background_image_path)

        # Cria o QStackedWidget para gerenciar as telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Tela de login
        self.login_screen = self.create_login_screen()
        self.stacked_widget.addWidget(self.login_screen)

        # Tela intermediária
        self.intermediate_screen = self.create_intermediate_screen()
        self.stacked_widget.addWidget(self.intermediate_screen)

        # Tela principal do quiz
        self.quiz_screen = self.create_quiz_screen()
        self.stacked_widget.addWidget(self.quiz_screen)

        # Tela de cadastro
        self.cadastro_screen = self.create_cadastro_screen()
        self.stacked_widget.addWidget(self.cadastro_screen)

        # Tela de desempenho
        self.desempenho_screen = self.create_desempenho_screen()
        self.stacked_widget.addWidget(self.desempenho_screen)

        # Mostra a tela de login inicialmente
        self.stacked_widget.setCurrentIndex(0)

    def set_background_image(self, image_path):
        """Define uma imagem como plano de fundo da janela."""
        pixmap = QPixmap(image_path)  # Carrega a imagem

        # Redimensiona a imagem para cobrir toda a janela
        scaled_pixmap = pixmap.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Cria um QBrush a partir do QPixmap
        brush = QBrush(scaled_pixmap)

        palette = self.palette()
        # Define o QBrush como plano de fundo
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

    def resizeEvent(self, event):
        """Redimensiona a imagem de fundo quando a janela é redimensionada."""
        super().resizeEvent(event)
        self.set_background_image(self.background_image_path)

    def create_login_screen(self):
        """Cria a tela de login."""
        screen = QWidget()
        # Usa QGridLayout para centralização dinâmica
        screen_layout = QGridLayout(screen)
        screen_layout.setAlignment(Qt.AlignCenter)  # Centraliza o conteúdo

        # Cria um QFrame para o retângulo preto semi-transparente
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 60% de opacidade */
            border: 1px solid white;
            border-radius: 15px;
        """)
        frame.setFixedSize(400, 300)  # Tamanho do retângulo
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Título
        title = QLabel("Autenticação")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 40% de opacidade */
            color: white;
            border-radius: 10px;  /* Bordas arredondadas */
            padding: 10px;  /* Espaçamento interno */
        """)
        title.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title)

        # Campo de email
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")
        self.email_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        """)
        frame_layout.addWidget(self.email_entry)

        # Campo de senha
        self.senha_entry = QLineEdit()
        self.senha_entry.setPlaceholderText("Senha")
        self.senha_entry.setEchoMode(QLineEdit.Password)
        self.senha_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        """)
        frame_layout.addWidget(self.senha_entry)

        # Botão de entrar
        entrar_button = QPushButton("Entrar")
        entrar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 90);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 180);
            }
        """)
        entrar_button.clicked.connect(self.verificar_autenticacao)
        frame_layout.addWidget(entrar_button)

        # Botão de criar cadastro
        cadastro_button = QPushButton("Criar Cadastro")
        cadastro_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 90);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 180);
            }
        """)
        cadastro_button.clicked.connect(self.show_cadastro_screen)
        frame_layout.addWidget(cadastro_button)

        # Adiciona o frame ao layout da tela
        screen_layout.addWidget(frame, 0, 0, alignment=Qt.AlignCenter)

        return screen

    def create_intermediate_screen(self):
        """Cria a tela intermediária após o login."""
        screen = QWidget()
        layout = QVBoxLayout()

        # Título
        title = QLabel("Bem-vindo ao Quiz!")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            color: white;
            padding: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Painel de resumo de desempenho
        self.resumo_frame = QFrame()
        self.resumo_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 90);  /* Preto com 60% de opacidade */
            border-radius: 15px;
            padding: 15px;
        """)
        self.resumo_frame.setFixedSize(500, 350)  # Tamanho do painel
        resumo_layout = QVBoxLayout(self.resumo_frame)
        resumo_layout.setAlignment(Qt.AlignCenter)

        # Label para exibir o resumo de desempenho
        self.resumo_label = QLabel()
        self.resumo_label.setFont(QFont("Arial", 12))
        self.resumo_label.setStyleSheet("""
            color: white;
        """)
        self.resumo_label.setAlignment(Qt.AlignCenter)
        resumo_layout.addWidget(self.resumo_label)

        layout.addWidget(self.resumo_frame, alignment=Qt.AlignCenter)

        # Botão "Começar Quiz"
        comecar_button = QPushButton("Começar Quiz")
        comecar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                max-width: 200px;  /* Largura máxima */
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);
            }
        """)
        comecar_button.setFixedWidth(200)  # Largura fixa

        comecar_button.clicked.connect(self.show_quiz_screen)
        layout.addWidget(comecar_button, alignment=Qt.AlignCenter)

        # Botão "Sair"
        sair_button = QPushButton("Sair")
        sair_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                max-width: 200px;  /* Largura máxima */
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);
            }
        """)
        sair_button.setFixedWidth(200)  # Largura fixa
        sair_button.clicked.connect(self.show_login_screen)
        layout.addWidget(sair_button, alignment=Qt.AlignCenter)
        screen.setLayout(layout)
        return screen

    def create_cadastro_screen(self):
        """Cria a tela de cadastro."""
        screen = QWidget()
        screen_layout = QVBoxLayout(screen)

        # Cria um QFrame para o retângulo preto semi-transparente
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 60% de opacidade */
            border: 1px solid white;
            border-radius: 15px;
        """)
        frame.setFixedSize(400, 300)  # Tamanho do retângulo
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Título
        title = QLabel("Criar Cadastro")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);  /* Preto com 40% de opacidade */
            color: white;
            border-radius: 10px;  /* Bordas arredondadas */
            padding: 10px;  /* Espaçamento interno */
        """)
        title.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title)

        # Campo de nome
        self.nome_entry = QLineEdit()
        self.nome_entry.setPlaceholderText("Nome")
        self.nome_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        """)
        frame_layout.addWidget(self.nome_entry)

        # Campo de email
        self.email_cadastro_entry = QLineEdit()
        self.email_cadastro_entry.setPlaceholderText("Email")
        self.email_cadastro_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        """)
        frame_layout.addWidget(self.email_cadastro_entry)

        # Campo de senha
        self.senha_cadastro_entry = QLineEdit()
        self.senha_cadastro_entry.setPlaceholderText("Senha")
        self.senha_cadastro_entry.setEchoMode(QLineEdit.Password)
        self.senha_cadastro_entry.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        """)
        frame_layout.addWidget(self.senha_cadastro_entry)

        # Botão de confirmar cadastro
        confirmar_button = QPushButton("Confirmar")
        confirmar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 90);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 180);
            }
        """)
        confirmar_button.clicked.connect(self.confirmar_cadastro)
        frame_layout.addWidget(confirmar_button)

        # Botão de voltar
        voltar_button = QPushButton("Voltar")
        voltar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 90);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 180);
            }
        """)
        voltar_button.clicked.connect(self.show_login_screen)
        frame_layout.addWidget(voltar_button)

        # Adiciona o frame ao layout da tela
        screen_layout.addWidget(frame, alignment=Qt.AlignCenter)

        return screen

    def create_quiz_screen(self):
        """Cria a tela principal do quiz."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Cria um QFrame semi-transparente para o fundo
        background_frame = QFrame()
        background_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 80);  /* Preto com 60% de opacidade */
            border-radius: 15px;
        """)
        background_frame.setFixedSize(800, 675)  # Tamanho do frame
        background_layout = QVBoxLayout(background_frame)
        background_layout.setAlignment(Qt.AlignCenter)
        background_layout.setSpacing(2)

        # Área para exibir a imagem da questão
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  /* Fundo semi-transparente */
            border: 1px solid white;
            border-radius: 10px;
            padding: 10px;
        """)
        self.image_label.setFixedSize(750, 450)  #
        background_layout.addWidget(self.image_label)

        # Adiciona um espaçamento entre a imagem e as informações da prova
        background_layout.addSpacing(5)

        # Área para exibir as informações da prova
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  /* Preto com 40% de opacidade */
            border: 1px solid white;
            border-radius: 10px;
            padding: 5px;
        """)
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(10)  # Espaçamento entre os labels
        info_layout.setContentsMargins(2, 2, 2, 2)  # Margens internas

        # Labels para exibir as informações da prova
        self.banca_label = QLabel("Banca: ")
        self.banca_label.setStyleSheet("""
            color: rgba(0, 0, 0, 120);
            font-size: 14px;  /* Aumentei o tamanho da fonte */
            font-weight: bold;
        """)
        info_layout.addWidget(self.banca_label)

        self.ano_label = QLabel("Ano: ")
        self.ano_label.setStyleSheet("""
            color: rgba(0, 0, 0, 120);
            font-size: 14px;  /* Aumentei o tamanho da fonte */
            font-weight: bold;
        """)
        info_layout.addWidget(self.ano_label)

        self.infor_label = QLabel("")
        self.infor_label.setStyleSheet("""
            color: rgba(0, 0, 0, 120);
            font-size: 14px;  /* Aumentei o tamanho da fonte */
            font-weight: bold;
        """)
        info_layout.addWidget(self.infor_label)

        background_layout.addWidget(info_frame)

        # Adiciona um espaçamento entre as informações da prova e os botões de alternativas
        background_layout.addSpacing(5)

        # Frame para os botões de alternativas
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 80);  /* Preto com 40% de opacidade */
            border: 1px solid white;
            border-radius: 10px;
            padding: 5px;
        """)
        buttons_layout = QHBoxLayout(buttons_frame)
        self.buttons = []
        for option in ["A", "B", "C", "D", "E"]:
            button = QPushButton(option)
            button.setFixedSize(100, 50)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 80);  /* Fundo branco semi-transparente */
                    color: rgba(0, 0, 0, 160);  /* Texto preto */
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 160);  /* Fundo mais claro ao passar o mouse */
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 200);  /* Fundo mais escuro ao clicar */
                    color: rgba(255, 255, 255, 160);  /* Texto preto */
                }
            """)
            button.clicked.connect(
                lambda _, o=option: self.check_answer(o))
            buttons_layout.addWidget(button)
            self.buttons.append(button)
        background_layout.addWidget(buttons_frame)

        # Adiciona um espaçamento entre os botões de alternativas e os botões de menu
        background_layout.addSpacing(20)

        # Layout horizontal para os botões "Ver Desempenho" e "Voltar ao Menu"
        menu_buttons_layout = QHBoxLayout()

        # Botão para ver desempenho
        self.desempenho_button = QPushButton("Ver Desempenho")
        self.desempenho_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 80);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 160);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 160);
                color: black;
            }
        """)
        self.desempenho_button.clicked.connect(self.mostrar_desempenho)
        menu_buttons_layout.addWidget(self.desempenho_button)

        # Botão para voltar ao menu inicial
        voltar_menu_button = QPushButton("Voltar ao Menu")
        voltar_menu_button.setStyleSheet("""
             QPushButton {
                background-color: rgba(0, 0, 0, 80);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 160);  /* Opacidade aumentada ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 160);
                color: black;
            }
        """)
        voltar_menu_button.clicked.connect(self.show_intermediate_screen)
        menu_buttons_layout.addWidget(voltar_menu_button)

        background_layout.addLayout(menu_buttons_layout)

        # Adiciona o frame semi-transparente ao layout principal
        layout.addWidget(background_frame, alignment=Qt.AlignCenter)

        screen.setLayout(layout)
        return screen

    def create_desempenho_screen(self):
        """Cria a tela de desempenho."""
        screen = QWidget()
        layout = QVBoxLayout()

        # Label para exibir o desempenho
        self.desempenho_label = QLabel()
        self.desempenho_label.setFont(QFont("Arial", 14))
        self.desempenho_label.setAlignment(Qt.AlignCenter)
        self.desempenho_label.setWordWrap(True)
        self.desempenho_label.setStyleSheet(
            "color: white; font-weight: bold;")  # Texto branco e negrito
        layout.addWidget(self.desempenho_label)

        # Botão para fechar
        fechar_button = QPushButton("Fechar")
        fechar_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 60);
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                max-width: 200px;  /* Largura máxima */
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 120);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 240);
            }
        """)
        fechar_button.setFixedWidth(200)
        fechar_button.clicked.connect(self.show_quiz_screen)
        layout.addWidget(fechar_button, alignment=Qt.AlignCenter)

        screen.setLayout(layout)
        return screen

    def show_login_screen(self):
        """Mostra a tela de login."""
        self.stacked_widget.setCurrentIndex(0)

    def show_intermediate_screen(self):
        """Mostra a tela intermediária após o login."""
        print("idddddddddddddddddddddddddddd...", self.id_usuario)
        self.stacked_widget.setCurrentIndex(1)  # Índice da tela intermediária

    def show_cadastro_screen(self):
        """Mostra a tela de cadastro."""
        self.stacked_widget.setCurrentIndex(3)

    def show_quiz_screen(self):
        """Mostra a tela do quiz."""
        self.stacked_widget.setCurrentIndex(2)  # Índice da tela do quiz
        self.iniciar_quiz()

    def show_desempenho_screen(self):
        """Mostra a tela de desempenho e atualiza o desempenho."""
        if self.id_usuario:
            desempenho = self.intermediary_manager.calcular_desempenho(
                self.id_usuario)
            self.desempenho_label.setText(desempenho)
        else:
            self.desempenho_label.setText("Usuário não autenticado.")
        self.stacked_widget.setCurrentIndex(4)  # Índice da tela de desempenho

    def verificar_autenticacao(self):
        """Verifica se o usuário está autenticado."""
        email = self.email_entry.text()
        senha = self.senha_entry.text()
        self.id_usuario = self.intermediary_manager.autenticar_usuario(
            email, senha)
        print("idddddddddddddddddddddddddddddddddddddddddddddd...", self.id_usuario)
        if self.id_usuario:
            self.atualizar_resumo_desempenho()
            self.show_intermediate_screen()  # Redireciona para a tela intermediária
        else:
            QMessageBox.critical(self, "Erro", "Email ou senha incorretos.")

    def confirmar_cadastro(self):
        """Confirma o cadastro do usuário."""
        nome = self.nome_entry.text()
        email = self.email_cadastro_entry.text()
        senha = self.senha_cadastro_entry.text()

        if not nome or not email or not senha:
            QMessageBox.critical(
                self, "Erro", "Todos os campos são obrigatórios.")
            return

        try:
            self.intermediary_manager.adicionar_usuario(nome, email, senha)
            QMessageBox.information(
                self, "Sucesso", "Cadastro realizado com sucesso!")
            self.show_login_screen()
        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Erro ao criar cadastro: {str(e)}")

    def iniciar_quiz(self):
        """Inicia o quiz após o login bem-sucedido."""
        self.next_question()

    def next_question(self):
        """Carrega a próxima questão."""
        if self.modo_sugestao:
            id_sugerida, questao_sugerida = self.intermediary_manager.sugerir_questao(
                self.current_question.area,
                self.current_question.id_questao,
                self.questoes_sugeridas,
            )
            if questao_sugerida:
                if self.current_question.id_questao not in self.questoes_sugeridas:
                    self.questoes_sugeridas.append(
                        self.current_question.id_questao)
                self.current_question = questao_sugerida

                # Verifica se a lista de sugestões ultrapassou 5 questões
                if len(self.questoes_sugeridas) > 5:
                    self.modo_sugestao = False  # Muda para o modo aleatório
                    self.questoes_sugeridas.clear()
            else:
                QMessageBox.information(
                    self, "Info", "Nenhuma questão sugerida disponível.")
                self.modo_sugestao = False
                self.current_question = None
        else:
            self.current_question = self.intermediary_manager.enviar_questao_aleatoria()

        if self.current_question:
            self.display_question(self.current_question)
        else:
            QMessageBox.information(
                self, "Fim", "Não há mais questões disponíveis.")

    def display_question(self, question):
        """Exibe a questão na interface."""
        try:
            # Exibe a imagem da questão
            image = Image.open(question.imagem)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(image_bytes.getvalue())
            self.image_label.setPixmap(pixmap)

            # Busca as informações da prova usando o id_prova da questão
            if question.id_prova:
                prova = self.intermediary_manager.get_prova_by_id(
                    question.id_prova)
                if prova:
                    self.banca_label.setText(f"Banca: {prova.banca}")
                    self.ano_label.setText(f"Ano: {prova.ano}")
                    self.infor_label.setText(f"Prova: {prova.infor}")
                else:
                    self.banca_label.setText("Banca: N/A")
                    self.ano_label.setText("Ano: N/A")
                    self.infor_label.setText("Prova: N/A")
            else:
                self.banca_label.setText("Banca: N/A")
                self.ano_label.setText("Ano: N/A")
                self.infor_label.setText("Prova: N/A")

        except Exception as e:
            QMessageBox.critical(
                self, "Erro", f"Não foi possível carregar a imagem: {e}")

    def check_answer(self, selected_option):
        """Verifica se a resposta está correta."""
        if self.current_question:
            resposta_correta = self.current_question.resposta_correta.strip().lower()
            selected_option_normalized = selected_option.strip().lower()

            acerto_erro = 1 if selected_option_normalized == resposta_correta else 0
            hora_atual = datetime.now()  # Data e hora atuais
            area_questao = self.current_question.area

            self.intermediary_manager.registrar_resposta(
                self.id_usuario,
                self.current_question.id_questao,
                acerto_erro,
                hora_atual,
                area_questao
            )

            if acerto_erro:
                QMessageBox.information(self, "Resposta", "Correto!")
                self.modo_sugestao = False
                self.questoes_sugeridas.clear()
            else:
                QMessageBox.information(
                    self, "Resposta", "Errado! Buscando uma questão similar...")
                self.modo_sugestao = True

            self.next_question()

    def mostrar_desempenho(self):
        """Mostra a tela de desempenho."""
        print("def mostrar_desempenho(self)...", self.id_usuario)
        if self.id_usuario:
            desempenho = self.intermediary_manager.calcular_desempenho(
                self.id_usuario)
            print("def mostrar_desempenho(self)...", desempenho)
        else:
            desempenho = "Usuário não autenticado."

        self.desempenho_label.setText(desempenho)
        self.show_desempenho_screen()

    def atualizar_resumo_desempenho(self):
        """Atualiza o resumo de desempenho na tela intermediária."""
        if hasattr(self, 'resumo_label'):  # Verifica se o resumo_label já foi criado
            print("if hasattr(self, 'resumo_label'):...")
            if self.id_usuario:
                # Calcula o desempenho do usuário
                desempenho = self.intermediary_manager.calcular_desempenho(
                    self.id_usuario)
                self.resumo_label.setText(desempenho)
            else:
                self.resumo_label.setText("Usuário não autenticado.")

    def showEvent(self, event):
        """Atualiza o painel de resumo de desempenho sempre que a tela intermediária é exibida."""
        super().showEvent(event)
        if self.stacked_widget.currentIndex() == 1:  # Verifica se a tela intermediária está ativa
            self.atualizar_resumo_desempenho()
