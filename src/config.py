"""
Configurações do AI Chatbot Brasileiro
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Carregar variáveis de ambiente
load_dotenv()

def load_config() -> Dict[str, Any]:
    """
    Carrega as configurações da aplicação.
    
    Returns:
        Dict com todas as configurações
    """
    return {
        # OpenAI Configuration
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'max_tokens': int(os.getenv('MAX_TOKENS', 150)),
        'temperature': float(os.getenv('TEMPERATURE', 0.7)),
        'top_p': float(os.getenv('TOP_P', 1.0)),
        
        # Chatbot Settings
        'chatbot_name': os.getenv('CHATBOT_NAME', 'Assistente IA Brasileiro'),
        'chatbot_personality': os.getenv(
            'CHATBOT_PERSONALITY', 
            'Você é um assistente útil e amigável que fala português brasileiro.'
        ),
        
        # Database
        'database_path': os.getenv('DATABASE_PATH', 'data/conversations.db'),
        
        # App Settings
        'app_title': os.getenv('APP_TITLE', '🤖 AI Chatbot Brasileiro'),
        'app_description': os.getenv('APP_DESCRIPTION', 'Seu assistente inteligente em português'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
        
        # UI Configuration
        'theme': os.getenv('THEME', 'light'),
        'sidebar_expanded': os.getenv('SIDEBAR_EXPANDED', 'true').lower() == 'true',
        'show_conversation_history': os.getenv('SHOW_CONVERSATION_HISTORY', 'true').lower() == 'true',
        'max_conversation_history': int(os.getenv('MAX_CONVERSATION_HISTORY', 50)),
        
        # Rate Limiting
        'max_requests_per_minute': int(os.getenv('MAX_REQUESTS_PER_MINUTE', 20)),
        'max_tokens_per_day': int(os.getenv('MAX_TOKENS_PER_DAY', 10000)),
    }

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Valida se as configurações estão corretas.
    
    Args:
        config: Dicionário de configurações
        
    Returns:
        True se válido, False caso contrário
    """
    required_keys = ['openai_api_key']
    
    for key in required_keys:
        if not config.get(key):
            print(f"Erro: Configuração '{key}' não encontrada ou vazia.")
            return False
    
    return True

# Configurações padrão para desenvolvimento
DEFAULT_CONFIG = {
    'openai_model': 'gpt-3.5-turbo',
    'max_tokens': 150,
    'temperature': 0.7,
    'top_p': 1.0,
    'chatbot_name': 'Assistente IA Brasileiro',
    'database_path': 'data/conversations.db',
    'debug': False,
}
