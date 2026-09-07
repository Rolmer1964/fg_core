"""Núcleo orquestrador da família FinGuard.

Estado atual: RAG (`fg_rag`), guardrails (`fg_guardrail`), triagem (`fg_triagem`) e
risco (`fg_risco`). Conforme `fg_relatorios` e `fg_front` ficarem prontos, cada um
vira uma propriedade lazy aqui.

O `Nucleo` é o único ponto que conhece vários pacotes ao mesmo tempo. As folhas
não se enxergam: quando a saída de um passo precisa entrar noutro, é aqui que a
costura acontece (ver `avaliar_risco`).
"""

from __future__ import annotations

from fg_dominio import ResultadoRisco, ResultadoTriagem
from fg_guardrail import Guardrail
from fg_rag import RagLocal
from fg_risco import Risco
from fg_triagem import Triagem

from .configuracao import Configuracao


def _consulta_politica(texto: str, triagem: ResultadoTriagem) -> str:
    """Texto + dimensões da triagem, para focar a busca semântica na política.

    Portado do `risk.service._build_query` do finguard-modular: no monólito o
    risco fazia a própria recuperação; aqui isso é responsabilidade do orquestrador.
    """
    partes = [texto, triagem.categoria, triagem.produto, triagem.sentimento]
    return " ".join(p for p in partes if p)


class Nucleo:
    def __init__(self, configuracao: Configuracao | None = None) -> None:
        self.configuracao = configuracao or Configuracao()
        self._rag: RagLocal | None = None
        self._guardrail: Guardrail | None = None
        self._triagem: Triagem | None = None
        self._risco: Risco | None = None

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

    def avaliar_risco(self, texto: str, triagem: ResultadoTriagem) -> ResultadoRisco:
        """Costura `fg_rag` → `fg_risco`.

        Recupera os trechos relevantes da política interna, formata o contexto e
        delega ao `fg_risco` — que não conhece `fg_rag` nem `fg_triagem` e só
        recebe a string pronta.
        """
        consulta = _consulta_politica(texto, triagem)
        trechos = self.rag.recuperar(consulta, k=self.configuracao.rag_top_k)
        contexto = self.rag.formatar_para_prompt(trechos)
        return self.risco.avaliar(texto, triagem, contexto, trechos_rag_usados=len(trechos))
