from fg_rag import RagLocal

from fg_core import Nucleo


def test_rag_e_raglocal_lazy_e_unico(config):
    n = Nucleo(config)
    assert n._rag is None
    primeiro = n.rag
    assert isinstance(primeiro, RagLocal)
    assert n.rag is primeiro  # não reconstrói


def test_nucleo_sem_config_usa_ambiente(monkeypatch):
    monkeypatch.setenv("FG_CORE_RAG_VETORIZADOR", "deterministico")
    n = Nucleo()
    assert n.configuracao.rag_vetorizador == "deterministico"


def test_ponta_a_ponta_via_nucleo(config, escrever_doc):
    escrever_doc(
        "fraude.md",
        "Seção 3. Fraude e transação não autorizada.\n\n"
        "Bloquear o cartão imediatamente e abrir apuração interna.",
    )
    escrever_doc(
        "cobranca.md",
        "Seção 2. Cobrança indevida.\n\nEstornar o cliente em até 24 horas.",
    )

    nucleo = Nucleo(config)
    est = nucleo.rag.ingerir()
    assert est.total_vetores_final >= 2

    trechos = nucleo.rag.buscar_semelhantes("bloquear cartão por transação não autorizada", k=1)
    assert trechos and trechos[0].fonte == "fraude.md"
    assert "Política Interna" in nucleo.rag.formatar_para_prompt(trechos)


def test_reingestao_ignora_inalterado(config, escrever_doc):
    escrever_doc("p.md", "conteúdo estável da política")
    nucleo = Nucleo(config)
    nucleo.rag.ingerir()
    est = nucleo.rag.ingerir()
    assert est.ignorados == ["p.md"]
    assert est.trechos_adicionados == 0
