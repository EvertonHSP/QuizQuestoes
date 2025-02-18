class Embedding:
    def __init__(self, id_questao, vetor):
        self._id_questao = id_questao
        self._vetor = vetor

    # Getters
    @property
    def id_questao(self):
        return self._id_questao

    @property
    def vetor(self):
        return self._vetor

    # Setters
    @vetor.setter
    def vetor(self, vetor):
        self._vetor = vetor
