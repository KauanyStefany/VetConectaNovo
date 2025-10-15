"""
Configurações Centralizadas do VetConecta
Usa Pydantic Settings para gerenciar variáveis de ambiente
"""
import os
from pathlib import Path
from typing import Set
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas de variáveis de ambiente"""
    
    # Informações da Aplicação
    app_name: str = "VetConecta"
    environment: str = "development"
    debug: bool = True
    
    # Segurança
    secret_key: str = "change-me-in-production"
    csrf_secret_key: str = "change-me-in-production"
    
    # Banco de Dados
    database_url: str = "sqlite:///dados.db"
    test_database_path: str = "storage/database/test_dados.db"
    
    # Sessão
    session_max_age: int = 3600
    session_https_only: bool = False
    
    # Upload de Arquivos
    upload_max_size: int = 5_242_880  # 5MB
    upload_allowed_extensions: Set[str] = {".jpg", ".jpeg", ".png", ".gif"}
    upload_path: str = "static/uploads/usuarios"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "storage/logs/app.log"
    
    # Rate Limiting
    rate_limit_login: int = 5
    rate_limit_cadastro: int = 3
    
    # Email (opcional)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@vetconecta.com"
    
    # Hosts permitidos
    allowed_hosts: str = "localhost,127.0.0.1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_database_path(self) -> str:
        """Retorna o caminho do banco de dados apropriado"""
        if os.environ.get('TESTING'):
            return self.test_database_path
        return self.database_url.replace("sqlite:///", "")
    
    def get_upload_extensions_list(self) -> list[str]:
        """Retorna lista de extensões permitidas para upload"""
        return list(self.upload_allowed_extensions)
    
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.environment.lower() == "production"


# Instância global de configurações
settings = Settings()
