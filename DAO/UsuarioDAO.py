from Models.Usuario import Usuario


class UsuarioDAO:
    def __init__(self, connection):
        self.connection = connection

    def add_user(self, nome, email, senha):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha))
            conn.commit()

    def get_user_by_email(self, email):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, nome, email, senha FROM usuarios WHERE email = ?",  # noqa: E501
                (email,)
            )
            data = cursor.fetchone()
            return Usuario(*data) if data else None

    def get_user_by_id(self, user_id):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_usuario, nome, email, senha FROM usuarios WHERE id_usuario = ?",
                (user_id,)
            )
            data = cursor.fetchone()
            return Usuario(*data) if data else None
