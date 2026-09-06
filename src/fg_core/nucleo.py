"""Núcleo integrador da família FinGuard.

Estado atual: RAG (`fg_rag`), guardrails (`fg_guardrail`) e triagem (`fg_triagem`).
Conforme `fg_risco`, `fg_relatorios` e `fg_front` ficarem prontos, cada um vira
uma propriedade lazy aqui.
"""

from __future__ import annotations

from fg_guardrail import Guardrail
from fg_rag import RagLocal
from fg_triagem import Triagem

from .configuracao import Configuracao


class Nucleo:
    def __init__(self, configuracao: Configuracao | None = None) -> None:
        self.configuracao = configuracao or Configuracao()
        self._rag: RagLocal | None = None
        self._guardrail: Guardrail | None = None
        self._triagem: Triagem | None = None

    @property
    def rag(self) -> RagLocal:
        """Instância única de `fg_rag.RagLocal`, construída a partir da configuração."""
        if self._rag is None:
            self._rag = RagLocal(self.configuracao.para_rag())
        return self._rag

    @property
    def guardrail(self) -> Guardrail:
        """Instância única de `fg_guardrail.Guardrail`, construída a partir da configuração."""
        if self._guardrail is None:
            self._guardrail = Guardrail(self.configuracao.para_guardrail())
        return self._guardrail

    @property
    def triagem(self) -> Triagem:
        """Instância única de `fg_triagem.Triagem`, construída a partir da configuração."""
        if self._triagem is None:
            self._triagem = Triagem(self.configuracao.para_triagem())
        return self._triagem
