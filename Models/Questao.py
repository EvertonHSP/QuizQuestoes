class Questao:
    def __init__(self, id_questao, enunciado, imagem,
                 alternativas, resposta_correta, area, id_prova=None):
        self._id_questao = id_questao
        self._enunciado = enunciado
        self._imagem = imagem
        self._alternativas = alternativas
        self._resposta_correta = resposta_correta
        self._area = area
        self._id_prova = id_prova

    # Getters
    @property
    def id_questao(self):
        return self._id_questao

    @property
    def enunciado(self):
        return self._enunciado

    @property
    def imagem(self):
        return self._imagem

    @property
    def alternativas(self):
        return self._alternativas

    @property
    def resposta_correta(self):
        return self._resposta_correta

    @property
    def area(self):
        return self._area

    @property
    def id_prova(self):
        return self._id_prova

    # Setters
    @enunciado.setter
    def enunciado(self, enunciado):
        self._enunciado = enunciado

    @imagem.setter
    def imagem(self, imagem):
        self._imagem = imagem

    @alternativas.setter
    def alternativas(self, alternativas):
        self._alternativas = alternativas

    @resposta_correta.setter
    def resposta_correta(self, resposta_correta):
        self._resposta_correta = resposta_correta

    @area.setter
    def area(self, area):
        self._area = area

    @id_prova.setter
    def id_prova(self, id_prova):
        self._id_prova = id_prova
