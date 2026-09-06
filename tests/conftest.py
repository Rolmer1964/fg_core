from pathlib import Path

import pytest

from fg_core import Configuracao


@pytest.fixture
def config(tmp_path) -> Configuracao:
    docs = tmp_path / "documentos"
    docs.mkdir()
    return Configuracao(
        rag_diretorio_documentos=str(docs),
        rag_diretorio_indice=str(tmp_path / "indice"),
        rag_vetorizador="deterministico",
        rag_dimensao_embedding=64,
        rag_tamanho_trecho=200,
        rag_sobreposicao_trecho=40,
        rag_top_k=3,
    )


@pytest.fixture
def escrever_doc(config):
    def _escrever(nome: str, conteudo: str) -> Path:
        caminho = Path(config.rag_diretorio_documentos) / nome
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    return _escrever
