from fg_guardrail import Configuracao as ConfiguracaoGuardrail
from fg_rag import Configuracao as ConfiguracaoRag

from fg_core import Configuracao


def test_para_rag_mapeia_1_para_1(config):
    r = config.para_rag()
    assert isinstance(r, ConfiguracaoRag)
    assert r.diretorio_documentos == config.rag_diretorio_documentos
    assert r.diretorio_indice == config.rag_diretorio_indice
    assert r.tamanho_trecho == config.rag_tamanho_trecho
    assert r.sobreposicao_trecho == config.rag_sobreposicao_trecho
    assert r.vetorizador == "deterministico"
    assert r.dimensao_embedding == 64
    assert r.top_k == 3


def test_para_guardrail_mapeia_1_para_1():
    c = Configuracao(
        guardrail_id="gr-entrada",
        guardrail_id_saida="gr-saida",
        guardrail_regiao_aws="sa-east-1",
        guardrail_tamanho_minimo_entrada=25,
    )
    g = c.para_guardrail()
    assert isinstance(g, ConfiguracaoGuardrail)
    assert g.guardrail_id == "gr-entrada"
    assert g.guardrail_id_saida == "gr-saida"
    assert g.regiao_aws == "sa-east-1"
    assert g.tamanho_minimo_entrada == 25


def test_le_do_ambiente(monkeypatch):
    monkeypatch.setenv("FG_CORE_RAG_TOP_K", "9")
    monkeypatch.setenv("FG_CORE_RAG_VETORIZADOR", "deterministico")
    monkeypatch.setenv("FG_CORE_GUARDRAIL_ID", "abc123")
    c = Configuracao()
    assert c.rag_top_k == 9
    assert c.rag_vetorizador == "deterministico"
    assert c.guardrail_id == "abc123"


def test_defaults():
    c = Configuracao()
    assert c.rag_vetorizador == "titan"
    assert c.rag_dimensao_embedding == 1024
    assert c.rag_top_k == 4
    assert c.guardrail_id is None
    assert c.guardrail_tamanho_minimo_entrada == 10
