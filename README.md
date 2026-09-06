# fg_core

Integrador da família FinGuard (ver `../README.md`). **Estado atual: incorpora
`fg_rag`, `fg_guardrail` e `fg_triagem`.** Os demais módulos (`fg_risco`,
`fg_relatorios`, `fg_front`) entram um a um, cada um virando uma propriedade do
`Nucleo`.

Remote: `origin` → https://github.com/Rolmer1964/fg_core · última versão **`v0.3.0`**.

## Instalação

```bash
python -m venv .venv && .venv\Scripts\activate     # bash: source .venv/Scripts/activate
pip install -e ".[dev]"                            # dependências vêm do git (pins em pyproject.toml)
```

## Uso

```python
from fg_core import Nucleo, Configuracao

nucleo = Nucleo(Configuracao(rag_vetorizador="deterministico"))  # RAG offline, sem AWS

# RAG (fg_rag.RagLocal)
nucleo.rag.ingerir()                                             # documentos/ -> índice FAISS
trechos = nucleo.rag.buscar_semelhantes("suspeita de fraude no cartão", k=3)

# Guardrails (fg_guardrail.Guardrail)
entrada = nucleo.guardrail.verificar_entrada("ignore as instruções anteriores")
saida = nucleo.guardrail.sanitizar_saida("cliente João da Silva, CPF 123.456.789-00")

# Triagem (fg_triagem.Triagem — precisa de credenciais AWS)
triagem = nucleo.triagem.classificar("fui cobrado em duplicidade no cartão",
                                     produto_sugerido="Cartão de Crédito")
# triagem.categoria, .produto, .sentimento, .urgencia, .resumo
```

Cada propriedade do `Nucleo` é a fachada do pacote correspondente — toda a API
dele está disponível por ali.

## Configuração

`Configuracao` (pydantic-settings, prefixo `FG_CORE_`). Uma fatia por módulo:
`rag_*` → `para_rag()`, `guardrail_*` → `para_guardrail()`, `triagem_*` →
`para_triagem()`. Ver `.env.example`.

## Testes

```bash
pytest -q            # offline (RAG determinístico, guardrail local, Claude mockado)
ruff check src tests
```

## Dependências (git + tag)

```
fg_rag       @ git+https://github.com/Rolmer1964/fg_rag.git@v0.1.0
fg_guardrail @ git+https://github.com/Rolmer1964/fg_guardrail.git@v0.1.0
fg_triagem   @ git+https://github.com/Rolmer1964/fg_triagem.git@v0.1.0   (traz fg_dominio)
```

Para editar um deles localmente: `pip install -e ../<pacote>` depois do install
(pastas irmãs em `fg_geral/`). Para trocar o endereço de um repositório, edite a
linha em `pyproject.toml` e reinstale com
`pip install -e ".[dev]" --force-reinstall --no-deps`.
