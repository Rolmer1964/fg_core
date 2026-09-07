"""Núcleo de *wiring* da família FinGuard.

Estado atual: RAG (`fg_rag`), guardrails (`fg_guardrail`), triagem (`fg_triagem`),
risco (`fg_risco`) e relatórios (`fg_relatorios`). Cada pacote vira uma
propriedade lazy que devolve a fachada dele já configurada a partir da
`Configuracao` agregada.

O `Nucleo` **só entrega instâncias configuradas** — não combina folhas. Quando a
saída de um passo precisa alimentar outro (ex.: montar a consulta do RAG a partir
da triagem antes de chamar o risco), essa costura é responsabilidade do
orquestrador (`fg_orquestrador`), não daqui.
"""

from __future__ import annotations

from fg_guardrail import Guardrail
from fg_rag import RagLocal
from fg_relatorios import Relatorios
from fg_risco import Risco
from fg_triagem import Triagem

from .configuracao import Configuracao


class Nucleo:
    def __init__(self, configuracao: Configuracao | None = None) -> None:
        self.configuracao = configuracao or Configuracao()
        self._rag: RagLocal | None = None
        self._guardrail: Guardrail | None = None
        self._triagem: Triagem | None = None
        self._risco: Risco | None = None
        self._relatorios: Relatorios | None = None

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

    @property
    def risco(self) -> Risco:
        """Instância única de `fg_risco.Risco`, construída a partir da configuração."""
        if self._risco is None:
            self._risco = Risco(self.configuracao.para_risco())
        return self._risco

    @property
    def relatorios(self) -> Relatorios:
        """Instância única de `fg_relatorios.Relatorios`, construída a partir da configuração."""
        if self._relatorios is None:
            self._relatorios = Relatorios(self.configuracao.para_relatorios())
        return self._relatorios
