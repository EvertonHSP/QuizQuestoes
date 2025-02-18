

class HistoricoUsuario:
    def __init__(self, id_usuario, id_questao, acerto, dataTime, erro, id_historico, area):
        self._id_historico = id_historico
        self._id_usuario = id_usuario
        self._id_questao = id_questao
        self._acerto = acerto
        self._dataTime = dataTime  # Renomeado de tempo_resposta para dataTime
        self._erro = erro
        self._area = area  # Nova coluna: área da questão

    # Getters
    @property
    def id_historico(self):
        return self._id_historico

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_questao(self):
        return self._id_questao

    @property
    def acerto(self):
        return self._acerto

    @property
    def dataTime(self):
        return self._dataTime

    @property
    def erro(self):
        return self._erro

    @property
    def area(self):
        return self._area

    # Setters
    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    @id_questao.setter
    def id_questao(self, id_questao):
        self._id_questao = id_questao

    @acerto.setter
    def acerto(self, acerto):
        self._acerto = acerto

    @dataTime.setter
    def dataTime(self, dataTime):
        self._dataTime = dataTime

    @erro.setter
    def erro(self, erro):
        self._erro = erro

    @area.setter
    def area(self, area):
        self._area = area