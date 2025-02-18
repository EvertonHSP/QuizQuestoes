class Usuario:
    def __init__(self, id_usuario, nome, email, senha):
        self._id_usuario = id_usuario
        self._nome = nome
        self._email = email
        self._senha = senha

    # Getters
    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha

    # Setters
    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @email.setter
    def email(self, email):
        self._email = email

    @senha.setter
    def senha(self, senha):
        self._senha = senha
