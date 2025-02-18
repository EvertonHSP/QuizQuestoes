from GUI import InterfaceApp
from IntermediaryManager import IntermediaryManager
from PyQt5.QtWidgets import QApplication
import sys
print("importações...")
# Certifique-se de que a classe InterfaceApp está no arquivo GUI.py


def main():
    # Caminho para o banco de dados
    print("Processando o arquivo main...")
    db_path = "questoes.db"

    # Inicializa o gerenciador intermediário
    intermediary_manager = IntermediaryManager(db_path)

    # Inicializa a aplicação PyQt5
    app = QApplication(sys.argv)

    # Cria a janela principal (InterfaceApp)
    window = InterfaceApp(intermediary_manager)

    # Mostra a janela
    window.show()

    # Inicia o loop principal da interface gráfica
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
