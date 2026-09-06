# fg_core

Integrador da família FinGuard (ver `../README.md`). **Estado atual: incorpora
apenas o `fg_rag`.** Os demais módulos (`fg_guard_rail`, `fg_triagem`, `fg_risco`,
`fg_relatorios`, `fg_front`) entram um a um, cada um virando uma propriedade do
`Nucleo`.

## Instalação

```bash
python -m venv .venv && .venv\Scripts\activate     # bash: source .venv/Scripts/activate
pip install -e ".[dev]"                            # fg_rag vem do git (pin em pyproject.toml)
```

## Uso

```python
from fg_core import Nucleo, Configuracao

nucleo = Nucleo(Configuracao(rag_vetorizador="deterministico"))  # offline, sem AWS
nucleo.rag.ingerir()                                             # documentos/ -> índice FAISS
trechos = nucleo.rag.buscar_semelhantes("suspeita de fraude no cartão", k=3)
print(nucleo.rag.formatar_para_prompt(trechos))
```

`nucleo.rag` é um `fg_rag.RagLocal`. Toda a API do `fg_rag` está disponível por ele.

## Configuração

`Configuracao` (pydantic-settings, prefixo `FG_CORE_`). Hoje só a fatia `rag_*`;
`para_rag()` traduz para a `Configuracao` do `fg_rag`. Ver `.env.example`.

## Testes

```bash
pytest -q            # offline (vetorizador determinístico do fg_rag)
ruff check src tests
```

## Dependência `fg_rag`

`fg_rag @ git+https://github.com/Rolmer1964/fg_rag.git@v0.1.0`. Para editar o
`fg_rag` localmente: `pip install -e ../../fg_rag` depois do install. Para trocar o
endereço do repositório, edite a linha em `pyproject.toml` e reinstale com
`--force-reinstall --no-deps`.
