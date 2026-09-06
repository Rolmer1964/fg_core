"""Configuração agregada do fg_core.

Hoje só carrega a fatia do `fg_rag`. Cada novo módulo da família adiciona seus
campos aqui (prefixados) e um `para_<modulo>()` que devolve a configuração dele.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

from fg_rag import Configuracao as ConfiguracaoRag


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FG_CORE_", env_file=None, extra="ignore")

    # ---- fg_rag ----
    rag_diretorio_documentos: str = "documentos"
    rag_diretorio_indice: str = "indice"
    rag_tamanho_trecho: int = 1000
    rag_sobreposicao_trecho: int = 200
    rag_vetorizador: str = "titan"
    rag_dimensao_embedding: int = 1024
    rag_modelo_embedding_bedrock: str = "amazon.titan-embed-text-v2:0"
    rag_top_k: int = 4
    rag_regiao_aws: str = "us-east-1"

    def para_rag(self) -> ConfiguracaoRag:
        """Traduz a fatia `rag_*` para a `Configuracao` do fg_rag."""
        return ConfiguracaoRag(
            diretorio_documentos=self.rag_diretorio_documentos,
            diretorio_indice=self.rag_diretorio_indice,
            tamanho_trecho=self.rag_tamanho_trecho,
            sobreposicao_trecho=self.rag_sobreposicao_trecho,
            vetorizador=self.rag_vetorizador,
            dimensao_embedding=self.rag_dimensao_embedding,
            modelo_embedding_bedrock=self.rag_modelo_embedding_bedrock,
            top_k=self.rag_top_k,
            regiao_aws=self.rag_regiao_aws,
        )
