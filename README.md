# Sistema de Recomendação de Questões de Múltipla Escolha

Este projeto visa desenvolver um sistema de recomendação de questões de múltipla escolha, adaptativo ao desempenho do usuário. O sistema utiliza técnicas de processamento de linguagem natural (NLP) e embeddings de texto para sugerir questões semelhantes às que o usuário errou, ajudando a otimizar o aprendizado.

## Autores
- Everton Hian Dos Santos Pinheiro
- Paulo Gabriel Souza Moreira

## Instituição
Instituto de Engenharia e Geociências – Universidade Federal do Oeste do Pará (UFOPA)

## Contato
- E-mail: {evertonhian.santos20, souzamoreira.stm}@gmail.com

---

## Relatório e Casos de Uso
O relatório detalhado do projeto, incluindo casos de uso, metodologia e resultados parciais, está disponível na pasta Relatório e Casos de Uso deste repositório. Alternativamente, você pode acessar o relatório diretamente pelo Google Drive.
< https://drive.google.com/drive/folders/1OYgByZ8btGlxXGSk524rx8eNkOfnjl7P >

Importante: Tanto o relatório quanto o projeto não estão finalizados. O sistema já está funcional, mas ainda está em desenvolvimento ativo, com melhorias e ajustes sendo implementados continuamente.

---

## Como Executar o Projeto

### Pré-requisitos
1. **Python 3.8 ou superior**: Certifique-se de ter o Python instalado. Você pode verificar a versão instalada com o comando:
   ```bash
   python --version
   ```

### Instalação das Dependências
1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/EvertonHSP/QuizQuestoes.git
   cd QuizQuestoes
   ```

2. Crie um ambiente virtual para isolar as dependências do projeto:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Executando o Sistema
1. Após instalar as dependências, execute o arquivo `main.py` para iniciar a aplicação:
   ```bash
   python main.py
   ```
2. A interface gráfica será aberta, permitindo que você interaja com o sistema.

---

## Funcionalidades do Sistema

### 1. **Autenticação de Usuário**
   - **Login**: Os usuários podem fazer login com e-mail e senha.
   - **Registro**: Novos usuários podem se cadastrar fornecendo nome, e-mail e senha.

### 2. **Recomendação de Questões**
   - O sistema recomenda questões com base no desempenho do usuário.
   - Se o usuário errar uma questão, o sistema sugere questões semelhantes utilizando embeddings de texto e similaridade de cosseno.

### 3. **Análise de Desempenho**
   - O sistema classifica o desempenho do usuário em três categorias:
     - **Bom**: Acertos acima de 80%.
     - **Médio**: Acertos entre 50% e 79%.
     - **Ruim**: Acertos abaixo de 50%.
   - Um relatório detalhado é gerado, incluindo gráficos e sugestões de melhoria.

### 4. **Interface Gráfica**
   - Desenvolvida com **PyQt5**, a interface é intuitiva e responsiva, permitindo que os usuários interajam facilmente com o sistema.

---

## Estrutura do Projeto

### Principais Componentes
- **`GUI.py`**: Funções da interface gráfica.
- **`IntermediaryManager.py`**: Gerencia a lógica de negócios e a comunicação entre a interface e o banco de dados.
- **`DatabaseManager.py`**: Responsável pela conexão e operações no banco de dados SQLite.
- **`DAO/`**: Contém as classes de acesso a dados (Data Access Object).
- **`Models/`**: Define as entidades do sistema, como usuários, questões e provas.
- **`main.py`**: Ponto de entrada do sistema.

### Banco de Dados
- O banco de dados é gerenciado pelo **SQLite** e armazena:
  - Informações dos usuários.
  - Questões e suas representações vetoriais (embeddings).
  - Histórico de desempenho dos usuários.
  - Informações das bancas das questões.

---

## Tecnologias Utilizadas

### Linguagem de Programação
- **Python**: Escolhido por sua simplicidade e vasta gama de bibliotecas.

### Bibliotecas Principais
- **PyQt5**: Para desenvolvimento da interface gráfica.
- **Sentence-Transformers**: Para geração de embeddings de texto.
- **SQLite**: Para armazenamento e gerenciamento de dados.
- **NumPy**: Para operações numéricas e cálculos de similaridade.

### Modelo de Embedding
- **all-MiniLM-L6-v2**: Modelo pré-treinado utilizado para transformar questões em vetores numéricos.

---

## Referências
- Reimers, N. and Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.
- VITOR, R. Agrupando frases usando similaridade por cosseno. Medium, 2020.
- BRAIN'S DEV. Embeddings, medidas de distância e similaridade. 2024.
- MATEMATIX. Média Aritmética: Critério de Convergência Explicado.
- INTELLICA AI. Comparison of Different Word Embeddings on Text Similarity: A Use Case in NLP. Medium, 2023.
