"""
Classe principal do AI Chatbot Brasileiro
"""

import openai
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .personalities import get_personality_prompt
from .config import DEFAULT_CONFIG

class ChatbotAI:
    """
    Classe principal do chatbot com integração OpenAI.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o chatbot com as configurações fornecidas.
        
        Args:
            config: Dicionário com configurações
        """
        self.config = {**DEFAULT_CONFIG, **config}
        self.conversation_memory = []
        self.current_personality = "assistente_geral"
        
        # Configurar cliente OpenAI
        if self.config.get('openai_api_key'):
            openai.api_key = self.config['openai_api_key']
        else:
            raise ValueError("OpenAI API Key não configurada")
    
    def set_personality(self, personality_key: str) -> None:
        """
        Define a personalidade do chatbot.
        
        Args:
            personality_key: Chave da personalidade a ser usada
        """
        self.current_personality = personality_key
        # Limpar memória ao trocar personalidade para evitar conflitos
        self.conversation_memory = []
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Atualiza configurações do chatbot.
        
        Args:
            new_config: Novas configurações a serem aplicadas
        """
        self.config.update(new_config)
    
    def add_to_memory(self, role: str, content: str) -> None:
        """
        Adiciona uma mensagem à memória da conversa.
        
        Args:
            role: 'user' ou 'assistant'
            content: Conteúdo da mensagem
        """
        self.conversation_memory.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Limitar tamanho da memória para evitar excesso de tokens
        max_memory = self.config.get('max_conversation_history', 20)
        if len(self.conversation_memory) > max_memory:
            # Manter sempre o prompt do sistema e as últimas mensagens
            system_messages = [msg for msg in self.conversation_memory if msg['role'] == 'system']
            recent_messages = self.conversation_memory[-(max_memory-len(system_messages)):]
            self.conversation_memory = system_messages + recent_messages
    
    def clear_memory(self) -> None:
        """Limpa a memória da conversa."""
        self.conversation_memory = []
    
    def prepare_messages(self, user_input: str) -> List[Dict[str, str]]:
        """
        Prepara as mensagens para envio à API do OpenAI.
        
        Args:
            user_input: Mensagem do usuário
            
        Returns:
            Lista de mensagens formatadas para a API
        """
        messages = []
        
        # Adicionar prompt do sistema com a personalidade atual
        system_prompt = get_personality_prompt(self.current_personality)
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Adicionar histórico da conversa (apenas conteúdo, sem timestamp)
        for msg in self.conversation_memory:
            if msg['role'] in ['user', 'assistant']:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Adicionar mensagem atual do usuário
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        return messages
    
    def generate_response(self, user_input: str) -> str:
        """
        Gera uma resposta usando a API do OpenAI.
        
        Args:
            user_input: Mensagem do usuário
            
        Returns:
            Resposta gerada pelo chatbot
        """
        try:
            # Adicionar mensagem do usuário à memória
            self.add_to_memory("user", user_input)
            
            # Preparar mensagens para a API
            messages = self.prepare_messages(user_input)
            
            # Fazer chamada para a API do OpenAI
            response = openai.ChatCompletion.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=self.config.get('max_tokens', 150),
                temperature=self.config.get('temperature', 0.7),
                top_p=self.config.get('top_p', 1.0),
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extrair resposta
            assistant_response = response.choices[0].message.content.strip()
            
            # Adicionar resposta à memória
            self.add_to_memory("assistant", assistant_response)
            
            return assistant_response
            
        except openai.error.AuthenticationError:
            return "❌ Erro de autenticação: Verifique sua API Key do OpenAI."
        
        except openai.error.RateLimitError:
            return "⏳ Limite de requisições atingido. Tente novamente em alguns minutos."
        
        except openai.error.APIError as e:
            return f"❌ Erro na API do OpenAI: {str(e)}"
        
        except Exception as e:
            return f"❌ Erro inesperado: {str(e)}"
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo da conversa atual.
        
        Returns:
            Dicionário com estatísticas da conversa
        """
        total_messages = len(self.conversation_memory)
        user_messages = len([msg for msg in self.conversation_memory if msg['role'] == 'user'])
        assistant_messages = len([msg for msg in self.conversation_memory if msg['role'] == 'assistant'])
        
        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "current_personality": self.current_personality,
            "start_time": self.conversation_memory[0]['timestamp'] if self.conversation_memory else None,
            "last_message_time": self.conversation_memory[-1]['timestamp'] if self.conversation_memory else None
        }
    
    def export_conversation(self) -> str:
        """
        Exporta a conversa atual em formato JSON.
        
        Returns:
            String JSON com a conversa
        """
        export_data = {
            "conversation_summary": self.get_conversation_summary(),
            "messages": self.conversation_memory,
            "export_timestamp": datetime.now().isoformat(),
            "chatbot_config": {
                "personality": self.current_personality,
                "model": self.config.get('openai_model'),
                "temperature": self.config.get('temperature'),
                "max_tokens": self.config.get('max_tokens')
            }
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
