"""Núcleo integrador da família FinGuard.

Estado atual: expõe apenas a capacidade de RAG (`fg_rag.RagLocal`). Conforme os
demais módulos (`fg_guard_rail`, `fg_triagem`, `fg_risco`, `fg_relatorios`,
`fg_front`) ficarem prontos, cada um vira uma propriedade lazy aqui.
"""

from __future__ import annotations

from fg_rag import RagLocal

from .configuracao import Configuracao


class Nucleo:
    def __init__(self, configuracao: Configuracao | None = None) -> None:
        self.configuracao = configuracao or Configuracao()
        self._rag: RagLocal | None = None

    @property
    def rag(self) -> RagLocal:
        """Instância única de `fg_rag.RagLocal`, construída a partir da configuração."""
        if self._rag is None:
            self._rag = RagLocal(self.configuracao.para_rag())
        return self._rag
