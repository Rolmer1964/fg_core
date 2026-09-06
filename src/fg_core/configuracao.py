"""Configuração agregada do fg_core.

Cada módulo da família tem sua fatia de campos (prefixada) e um `para_<modulo>()`
que devolve a `Configuracao` dele. Hoje: `fg_rag`, `fg_guardrail`, `fg_triagem`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

from fg_guardrail import Configuracao as ConfiguracaoGuardrail
from fg_rag import Configuracao as ConfiguracaoRag
from fg_triagem import Configuracao as ConfiguracaoTriagem


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

    # ---- fg_guardrail ----
    guardrail_id: str | None = None
    guardrail_versao: str = "DRAFT"
    guardrail_id_saida: str | None = None
    guardrail_versao_saida: str = "DRAFT"
    guardrail_regiao_aws: str = "us-east-1"
    guardrail_tamanho_minimo_entrada: int = 10

    # ---- fg_triagem ----
    triagem_modelo_bedrock: str = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    triagem_regiao_aws: str = "us-east-1"
    triagem_temperatura: float = 0.1
    triagem_max_tokens: int = 600

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

    def para_guardrail(self) -> ConfiguracaoGuardrail:
        """Traduz a fatia `guardrail_*` para a `Configuracao` do fg_guardrail."""
        return ConfiguracaoGuardrail(
            guardrail_id=self.guardrail_id,
            guardrail_versao=self.guardrail_versao,
            guardrail_id_saida=self.guardrail_id_saida,
            guardrail_versao_saida=self.guardrail_versao_saida,
            regiao_aws=self.guardrail_regiao_aws,
            tamanho_minimo_entrada=self.guardrail_tamanho_minimo_entrada,
        )

    def para_triagem(self) -> ConfiguracaoTriagem:
        """Traduz a fatia `triagem_*` para a `Configuracao` do fg_triagem."""
        return ConfiguracaoTriagem(
            modelo_bedrock=self.triagem_modelo_bedrock,
            regiao_aws=self.triagem_regiao_aws,
            temperatura=self.triagem_temperatura,
            max_tokens=self.triagem_max_tokens,
        )
