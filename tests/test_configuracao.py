from fg_guardrail import Configuracao as ConfiguracaoGuardrail
from fg_rag import Configuracao as ConfiguracaoRag
from fg_relatorios import Configuracao as ConfiguracaoRelatorios
from fg_risco import Configuracao as ConfiguracaoRisco
from fg_triagem import Configuracao as ConfiguracaoTriagem

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


def test_para_triagem_mapeia_1_para_1():
    c = Configuracao(
        triagem_modelo_bedrock="modelo-x",
        triagem_regiao_aws="sa-east-1",
        triagem_temperatura=0.7,
        triagem_max_tokens=999,
    )
    t = c.para_triagem()
    assert isinstance(t, ConfiguracaoTriagem)
    assert t.modelo_bedrock == "modelo-x"
    assert t.regiao_aws == "sa-east-1"
    assert t.temperatura == 0.7
    assert t.max_tokens == 999


def test_para_risco_mapeia_1_para_1():
    c = Configuracao(
        risco_modelo_bedrock="sonnet-x",
        risco_regiao_aws="sa-east-1",
        risco_temperatura=0.5,
        risco_max_tokens=1234,
    )
    r = c.para_risco()
    assert isinstance(r, ConfiguracaoRisco)
    assert r.modelo_bedrock == "sonnet-x"
    assert r.regiao_aws == "sa-east-1"
    assert r.temperatura == 0.5
    assert r.max_tokens == 1234


def test_para_relatorios_mapeia_1_para_1():
    c = Configuracao(relatorios_output_dir="/tmp/saida")
    rel = c.para_relatorios()
    assert isinstance(rel, ConfiguracaoRelatorios)
    assert rel.output_dir == "/tmp/saida"


def test_le_do_ambiente(monkeypatch):
    monkeypatch.setenv("FG_CORE_RAG_TOP_K", "9")
    monkeypatch.setenv("FG_CORE_RAG_VETORIZADOR", "deterministico")
    monkeypatch.setenv("FG_CORE_GUARDRAIL_ID", "abc123")
    monkeypatch.setenv("FG_CORE_TRIAGEM_MAX_TOKENS", "1200")
    c = Configuracao()
    assert c.rag_top_k == 9
    assert c.rag_vetorizador == "deterministico"
    assert c.guardrail_id == "abc123"
    assert c.triagem_max_tokens == 1200


def test_defaults():
    c = Configuracao()
    assert c.rag_vetorizador == "titan"
    assert c.rag_dimensao_embedding == 1024
    assert c.rag_top_k == 4
    assert c.guardrail_id is None
    assert c.guardrail_tamanho_minimo_entrada == 10
    assert c.triagem_modelo_bedrock.startswith("us.anthropic.claude-haiku")
    assert c.triagem_temperatura == 0.1
    assert c.risco_modelo_bedrock.startswith("us.anthropic.claude-sonnet")
    assert c.risco_temperatura == 0.2
    assert c.risco_max_tokens == 800
    assert c.relatorios_output_dir == "output"
