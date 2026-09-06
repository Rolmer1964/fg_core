"""fg_core — integrador da família FinGuard.

Estado atual: incorpora apenas o `fg_rag`.

    from fg_core import Nucleo, Configuracao

    nucleo = Nucleo(Configuracao(rag_vetorizador="deterministico"))
    nucleo.rag.ingerir()
    trechos = nucleo.rag.buscar_semelhantes("cliente ameaça acionar o Banco Central")
"""

from .configuracao import Configuracao
from .nucleo import Nucleo

__version__ = "0.1.0"

__all__ = ["Configuracao", "Nucleo", "__version__"]
