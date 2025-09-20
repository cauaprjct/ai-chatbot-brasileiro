"""
Testes para a classe ChatbotAI
"""

import pytest
import os
from unittest.mock import Mock, patch
from src.chatbot import ChatbotAI
from src.config import DEFAULT_CONFIG

class TestChatbotAI:
    """Testes para a classe ChatbotAI"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.config = {
            **DEFAULT_CONFIG,
            'openai_api_key': 'test-key-123'
        }
    
    def test_init_with_valid_config(self):
        """Teste inicialização com configuração válida"""
        chatbot = ChatbotAI(self.config)
        assert chatbot.config['openai_api_key'] == 'test-key-123'
        assert chatbot.current_personality == 'assistente_geral'
        assert len(chatbot.conversation_memory) == 0
    
    def test_init_without_api_key(self):
        """Teste inicialização sem API key"""
        config = {**self.config}
        del config['openai_api_key']
        
        with pytest.raises(ValueError, match="OpenAI API Key não configurada"):
            ChatbotAI(config)
    
    def test_set_personality(self):
        """Teste mudança de personalidade"""
        chatbot = ChatbotAI(self.config)
        
        # Adicionar algumas mensagens à memória
        chatbot.add_to_memory("user", "Olá")
        chatbot.add_to_memory("assistant", "Oi!")
        
        assert len(chatbot.conversation_memory) == 2
        
        # Mudar personalidade deve limpar memória
        chatbot.set_personality("desenvolvedor")
        
        assert chatbot.current_personality == "desenvolvedor"
        assert len(chatbot.conversation_memory) == 0
    
    def test_add_to_memory(self):
        """Teste adição de mensagens à memória"""
        chatbot = ChatbotAI(self.config)
        
        chatbot.add_to_memory("user", "Teste")
        
        assert len(chatbot.conversation_memory) == 1
        assert chatbot.conversation_memory[0]['role'] == 'user'
        assert chatbot.conversation_memory[0]['content'] == 'Teste'
        assert 'timestamp' in chatbot.conversation_memory[0]
    
    def test_memory_limit(self):
        """Teste limite de memória"""
        config = {**self.config, 'max_conversation_history': 3}
        chatbot = ChatbotAI(config)
        
        # Adicionar mais mensagens que o limite
        for i in range(5):
            chatbot.add_to_memory("user", f"Mensagem {i}")
        
        # Deve manter apenas as últimas mensagens
        assert len(chatbot.conversation_memory) <= 3
    
    def test_clear_memory(self):
        """Teste limpeza de memória"""
        chatbot = ChatbotAI(self.config)
        
        chatbot.add_to_memory("user", "Teste")
        assert len(chatbot.conversation_memory) == 1
        
        chatbot.clear_memory()
        assert len(chatbot.conversation_memory) == 0
    
    def test_update_config(self):
        """Teste atualização de configuração"""
        chatbot = ChatbotAI(self.config)
        
        new_config = {'temperature': 0.9, 'max_tokens': 200}
        chatbot.update_config(new_config)
        
        assert chatbot.config['temperature'] == 0.9
        assert chatbot.config['max_tokens'] == 200
        # Configurações antigas devem permanecer
        assert chatbot.config['openai_api_key'] == 'test-key-123'
    
    def test_prepare_messages(self):
        """Teste preparação de mensagens para API"""
        chatbot = ChatbotAI(self.config)
        
        # Adicionar algumas mensagens à memória
        chatbot.add_to_memory("user", "Primeira mensagem")
        chatbot.add_to_memory("assistant", "Primeira resposta")
        
        messages = chatbot.prepare_messages("Nova mensagem")
        
        # Deve ter: system prompt + histórico + nova mensagem
        assert len(messages) >= 3
        assert messages[0]['role'] == 'system'
        assert messages[-1]['role'] == 'user'
        assert messages[-1]['content'] == 'Nova mensagem'
    
    @patch('openai.ChatCompletion.create')
    def test_generate_response_success(self, mock_openai):
        """Teste geração de resposta com sucesso"""
        # Mock da resposta da OpenAI
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Resposta do chatbot"
        mock_openai.return_value = mock_response
        
        chatbot = ChatbotAI(self.config)
        response = chatbot.generate_response("Olá")
        
        assert response == "Resposta do chatbot"
        assert len(chatbot.conversation_memory) == 2  # user + assistant
        
        # Verificar se a API foi chamada corretamente
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args[1]
        assert call_args['model'] == self.config['openai_model']
        assert call_args['max_tokens'] == self.config['max_tokens']
    
    @patch('openai.ChatCompletion.create')
    def test_generate_response_api_error(self, mock_openai):
        """Teste tratamento de erro da API"""
        import openai
        mock_openai.side_effect = openai.error.AuthenticationError("Invalid API key")
        
        chatbot = ChatbotAI(self.config)
        response = chatbot.generate_response("Olá")
        
        assert "Erro de autenticação" in response
    
    def test_get_conversation_summary(self):
        """Teste resumo da conversa"""
        chatbot = ChatbotAI(self.config)
        
        # Conversa vazia
        summary = chatbot.get_conversation_summary()
        assert summary['total_messages'] == 0
        assert summary['user_messages'] == 0
        assert summary['assistant_messages'] == 0
        
        # Adicionar mensagens
        chatbot.add_to_memory("user", "Pergunta 1")
        chatbot.add_to_memory("assistant", "Resposta 1")
        chatbot.add_to_memory("user", "Pergunta 2")
        
        summary = chatbot.get_conversation_summary()
        assert summary['total_messages'] == 3
        assert summary['user_messages'] == 2
        assert summary['assistant_messages'] == 1
        assert summary['current_personality'] == 'assistente_geral'
    
    def test_export_conversation(self):
        """Teste exportação de conversa"""
        chatbot = ChatbotAI(self.config)
        
        chatbot.add_to_memory("user", "Teste")
        chatbot.add_to_memory("assistant", "Resposta")
        
        export_data = chatbot.export_conversation()
        
        # Deve ser JSON válido
        import json
        data = json.loads(export_data)
        
        assert 'conversation_summary' in data
        assert 'messages' in data
        assert 'export_timestamp' in data
        assert 'chatbot_config' in data
        
        assert len(data['messages']) == 2
