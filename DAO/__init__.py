# DAO/__init__.py
from .UsuarioDAO import UsuarioDAO
from .QuestaoDAO import QuestaoDAO
from .HistoricoUsuarioDAO import HistoricoUsuarioDAO
from .EmbeddingDAO import EmbeddingDAO
from .ProvaDAO import ProvaDAO
__all__ = ["UsuarioDAO", "QuestaoDAO",
           "HistoricoUsuarioDAO", "EmbeddingDAO", "ProvaDAO"]
