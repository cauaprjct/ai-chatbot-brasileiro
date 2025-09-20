"""
Exemplos de uso do AI Chatbot Brasileiro
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot import ChatbotAI
from src.config import load_config
from src.database import ConversationDB
from src.personalities import list_personalities

def example_basic_usage():
    """Exemplo básico de uso do chatbot"""
    print("🤖 Exemplo Básico - AI Chatbot Brasileiro")
    print("=" * 50)
    
    # Carregar configuração
    config = load_config()
    
    # Verificar se API key está configurada
    if not config.get('openai_api_key'):
        print("❌ Configure sua OPENAI_API_KEY no arquivo .env")
        return
    
    # Criar instância do chatbot
    chatbot = ChatbotAI(config)
    
    # Conversa simples
    print("\n💬 Iniciando conversa...")
    
    user_input = "Olá! Como você pode me ajudar?"
    print(f"👤 Usuário: {user_input}")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Chatbot: {response}")
    
    # Segunda mensagem
    user_input = "Qual é a capital do Brasil?"
    print(f"\n👤 Usuário: {user_input}")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Chatbot: {response}")
    
    # Mostrar resumo da conversa
    summary = chatbot.get_conversation_summary()
    print(f"\n📊 Resumo: {summary['total_messages']} mensagens")

def example_personalities():
    """Exemplo de uso com diferentes personalidades"""
    print("\n🎭 Exemplo Personalidades")
    print("=" * 50)
    
    config = load_config()
    if not config.get('openai_api_key'):
        print("❌ Configure sua OPENAI_API_KEY no arquivo .env")
        return
    
    chatbot = ChatbotAI(config)
    
    # Listar personalidades disponíveis
    personalities = list_personalities()
    print("\n🎯 Personalidades disponíveis:")
    for p in personalities[:3]:  # Mostrar apenas 3
        print(f"  {p['emoji']} {p['nome']}")
    
    # Testar personalidade de desenvolvedor
    print(f"\n💻 Testando personalidade: Desenvolvedor")
    chatbot.set_personality("desenvolvedor")
    
    user_input = "Como criar uma API REST em Python?"
    print(f"👤 Usuário: {user_input}")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Desenvolvedor: {response}")
    
    # Testar personalidade criativa
    print(f"\n🎨 Testando personalidade: Criativo")
    chatbot.set_personality("assistente_criativo")
    
    user_input = "Me dê ideias para um projeto inovador"
    print(f"👤 Usuário: {user_input}")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Criativo: {response}")

def example_database():
    """Exemplo de uso do banco de dados"""
    print("\n💾 Exemplo Banco de Dados")
    print("=" * 50)
    
    # Criar instância do banco
    db = ConversationDB("data/example_conversations.db")
    
    # Criar conversa de exemplo
    example_conversation = [
        {
            "role": "user",
            "content": "Olá, como você está?",
            "timestamp": "2024-01-15T10:00:00"
        },
        {
            "role": "assistant", 
            "content": "Olá! Estou bem, obrigado por perguntar. Como posso ajudá-lo hoje?",
            "timestamp": "2024-01-15T10:00:05"
        },
        {
            "role": "user",
            "content": "Preciso de ajuda com Python",
            "timestamp": "2024-01-15T10:01:00"
        },
        {
            "role": "assistant",
            "content": "Claro! Ficarei feliz em ajudar com Python. Qual é sua dúvida específica?",
            "timestamp": "2024-01-15T10:01:03"
        }
    ]
    
    # Salvar conversa
    conversation_id = db.save_conversation(example_conversation, "assistente_geral")
    print(f"✅ Conversa salva com ID: {conversation_id}")
    
    # Carregar conversa
    loaded_conversation = db.load_conversation(conversation_id)
    if loaded_conversation:
        print(f"📖 Conversa carregada: {loaded_conversation['message_count']} mensagens")
        print(f"🎭 Personalidade: {loaded_conversation['personality']}")
    
    # Listar conversas
    conversations = db.list_conversations(limit=5)
    print(f"\n📋 Total de conversas salvas: {len(conversations)}")
    
    # Estatísticas
    stats = db.get_statistics()
    print(f"📊 Estatísticas:")
    print(f"  - Total de conversas: {stats['total_conversations']}")
    print(f"  - Total de mensagens: {stats['total_messages']}")

def example_export_import():
    """Exemplo de exportação e importação"""
    print("\n📤 Exemplo Export/Import")
    print("=" * 50)
    
    config = load_config()
    if not config.get('openai_api_key'):
        print("❌ Configure sua OPENAI_API_KEY no arquivo .env")
        return
    
    chatbot = ChatbotAI(config)
    
    # Criar uma conversa
    chatbot.add_to_memory("user", "Qual é a diferença entre lista e tupla em Python?")
    chatbot.add_to_memory("assistant", "Listas são mutáveis e tuplas são imutáveis...")
    
    # Exportar conversa
    exported_data = chatbot.export_conversation()
    print("✅ Conversa exportada para JSON")
    
    # Salvar em arquivo
    with open("data/exemplo_conversa.json", "w", encoding="utf-8") as f:
        f.write(exported_data)
    print("💾 Arquivo salvo: data/exemplo_conversa.json")
    
    # Mostrar parte do JSON
    import json
    data = json.loads(exported_data)
    print(f"📋 Resumo: {data['conversation_summary']['total_messages']} mensagens")

def example_configuration():
    """Exemplo de configuração personalizada"""
    print("\n⚙️ Exemplo Configuração")
    print("=" * 50)
    
    # Configuração personalizada
    custom_config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_model': 'gpt-3.5-turbo',
        'max_tokens': 100,  # Respostas mais curtas
        'temperature': 0.9,  # Mais criativo
        'chatbot_name': 'Assistente Personalizado'
    }
    
    if not custom_config['openai_api_key']:
        print("❌ Configure sua OPENAI_API_KEY no arquivo .env")
        return
    
    chatbot = ChatbotAI(custom_config)
    
    print(f"🎯 Configuração:")
    print(f"  - Modelo: {custom_config['openai_model']}")
    print(f"  - Max Tokens: {custom_config['max_tokens']}")
    print(f"  - Temperature: {custom_config['temperature']}")
    
    # Testar com configuração personalizada
    user_input = "Conte uma piada"
    print(f"\n👤 Usuário: {user_input}")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Chatbot: {response}")
    
    # Atualizar configuração em tempo real
    chatbot.update_config({'temperature': 0.1})  # Menos criativo
    print(f"\n🔄 Temperature alterada para 0.1")
    
    response = chatbot.generate_response(user_input)
    print(f"🤖 Chatbot (menos criativo): {response}")

def main():
    """Função principal com menu de exemplos"""
    print("🤖 AI Chatbot Brasileiro - Exemplos de Uso")
    print("=" * 60)
    
    examples = [
        ("1", "Uso Básico", example_basic_usage),
        ("2", "Personalidades", example_personalities),
        ("3", "Banco de Dados", example_database),
        ("4", "Export/Import", example_export_import),
        ("5", "Configuração", example_configuration),
    ]
    
    print("\n📋 Exemplos disponíveis:")
    for code, name, _ in examples:
        print(f"  {code}. {name}")
    
    print("\n0. Executar todos os exemplos")
    print("q. Sair")
    
    while True:
        choice = input("\n🔢 Escolha um exemplo (0-5, q): ").strip().lower()
        
        if choice == 'q':
            print("👋 Até logo!")
            break
        elif choice == '0':
            print("\n🚀 Executando todos os exemplos...")
            for _, name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"❌ Erro no exemplo {name}: {e}")
            break
        else:
            # Encontrar e executar exemplo específico
            example_found = False
            for code, name, func in examples:
                if choice == code:
                    try:
                        func()
                        example_found = True
                    except Exception as e:
                        print(f"❌ Erro: {e}")
                    break
            
            if not example_found:
                print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    # Criar diretório data se não existir
    os.makedirs("data", exist_ok=True)
    
    main()
