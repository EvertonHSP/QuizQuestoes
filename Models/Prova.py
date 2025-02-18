class Prova:
    def __init__(self, id_prova, banca, ano, infor):
        self._id_prova = id_prova
        self._banca = banca
        self._ano = ano
        self._infor = infor

    # Getters
    @property
    def id_prova(self):
        return self._id_prova

    @property
    def banca(self):
        return self._banca

    @property
    def ano(self):
        return self._ano

    @property
    def infor(self):
        return self._infor

    # Setters
    @banca.setter
    def banca(self, banca):
        self._banca = banca

    @ano.setter
    def ano(self, ano):
        self._ano = ano

    @infor.setter
    def infor(self, infor):
        self._infor = infor
