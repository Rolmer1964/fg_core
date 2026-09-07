# fg_core

Wiring da família FinGuard (ver `../README.md`). **Estado atual: incorpora
`fg_rag`, `fg_guardrail`, `fg_triagem`, `fg_risco` e `fg_relatorios`.** Falta só
`fg_front`, que entra como propriedade do `Nucleo` quando ficar pronto.

O `Nucleo` é o único ponto que conhece vários pacotes ao mesmo tempo, mas **só
entrega instâncias configuradas** — não combina folhas. A costura entre passos
(ex.: montar o `contexto_politica` a partir do `fg_rag` antes de chamar o risco)
é do `fg_orquestrador`, não daqui.

Remote: `origin` → https://github.com/Rolmer1964/fg_core · última versão **`v0.5.0`**.

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

# Risco (fg_risco.Risco — recebe o contexto da política já formatado)
contexto = nucleo.rag.formatar_para_prompt(trechos)
risco = nucleo.risco.avaliar("fui cobrado em duplicidade no cartão", triagem, contexto)

# Relatórios (fg_relatorios.Relatorios)
consolidado = nucleo.relatorios.consolidar(triagem, risco, canal="Procon")
nucleo.relatorios.escrever_saidas([{"id": "1", "canal": "Procon", **vars(consolidado)}])
```

Cada propriedade do `Nucleo` é a fachada do pacote correspondente — toda a API
dele está disponível por ali. Ligar a saída de um passo à entrada de outro é
trabalho do `fg_orquestrador`.

## Configuração

`Configuracao` (pydantic-settings, prefixo `FG_CORE_`). Uma fatia por módulo:
`rag_*` → `para_rag()`, `guardrail_*` → `para_guardrail()`, `triagem_*` →
`para_triagem()`, `risco_*` → `para_risco()`, `relatorios_*` →
`para_relatorios()`. Ver `.env.example`.

## Testes

```bash
pytest -q            # offline (RAG determinístico, guardrail local, Claude mockado)
ruff check src tests
```

## Dependências (git + tag)

```
fg_dominio    @ git+https://github.com/Rolmer1964/fg_dominio.git@v0.3.0
fg_rag        @ git+https://github.com/Rolmer1964/fg_rag.git@v0.1.0
fg_guardrail  @ git+https://github.com/Rolmer1964/fg_guardrail.git@v0.1.0
fg_triagem    @ git+https://github.com/Rolmer1964/fg_triagem.git@v0.2.1
fg_risco      @ git+https://github.com/Rolmer1964/fg_risco.git@v0.1.1
fg_relatorios @ git+https://github.com/Rolmer1964/fg_relatorios.git@v0.2.0
```

Para editar um deles localmente: `pip install -e ../<pacote>` depois do install
(pastas irmãs em `fg_geral/`). Para trocar o endereço de um repositório, edite a
linha em `pyproject.toml` e reinstale com
`pip install -e ".[dev]" --force-reinstall --no-deps`.
