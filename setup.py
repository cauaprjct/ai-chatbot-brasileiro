#!/usr/bin/env python3
"""
Script de setup para o AI Chatbot Brasileiro
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Exibe banner do projeto"""
    print("🤖" + "=" * 58 + "🤖")
    print("🤖" + " " * 15 + "AI CHATBOT BRASILEIRO" + " " * 15 + "🤖")
    print("🤖" + " " * 12 + "Setup e Configuração Automática" + " " * 12 + "🤖")
    print("🤖" + "=" * 58 + "🤖")

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("\n🔍 Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ["data", "logs", "temp"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório '{directory}' criado")

def setup_env_file():
    """Configura arquivo .env"""
    print("\n⚙️ Configurando arquivo .env...")
    
    if os.path.exists(".env"):
        print("ℹ️ Arquivo .env já existe")
        return True
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Arquivo .env criado a partir do .env.example")
        print("⚠️ IMPORTANTE: Configure sua OPENAI_API_KEY no arquivo .env")
        return True
    else:
        print("❌ Arquivo .env.example não encontrado")
        return False

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("\n🧪 Testando importações...")
    
    modules_to_test = [
        "src.config",
        "src.chatbot", 
        "src.database",
        "src.personalities",
        "src.utils"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def create_sample_data():
    """Cria dados de exemplo"""
    print("\n📊 Criando dados de exemplo...")
    
    try:
        from src.database import ConversationDB
        
        db = ConversationDB("data/conversations.db")
        print("✅ Banco de dados inicializado")
        
        # Criar conversa de exemplo
        sample_conversation = [
            {
                "role": "user",
                "content": "Olá! Como você funciona?",
                "timestamp": "2024-01-15T10:00:00"
            },
            {
                "role": "assistant",
                "content": "Olá! Sou um chatbot brasileiro com IA. Posso ajudar com diversas tarefas usando diferentes personalidades. Como posso ajudá-lo hoje?",
                "timestamp": "2024-01-15T10:00:05"
            }
        ]
        
        conversation_id = db.save_conversation(sample_conversation, "assistente_geral")
        print(f"✅ Conversa de exemplo criada (ID: {conversation_id[:8]}...)")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        return False

def show_next_steps():
    """Mostra próximos passos"""
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("=" * 50)
    print("1. 🔑 Configure sua OpenAI API Key:")
    print("   - Edite o arquivo .env")
    print("   - Adicione: OPENAI_API_KEY=sua-chave-aqui")
    print()
    print("2. 🚀 Execute o chatbot:")
    print("   streamlit run app.py")
    print()
    print("3. 🌐 Acesse no navegador:")
    print("   http://localhost:8501")
    print()
    print("4. 📚 Veja exemplos de uso:")
    print("   python examples/example_usage.py")
    print()
    print("5. 🧪 Execute os testes:")
    print("   python -m pytest tests/")
    print()
    print("💡 Dica: Leia o README.md para mais informações!")

def main():
    """Função principal do setup"""
    print_banner()
    
    # Verificações e instalações
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependências", install_dependencies),
        ("Criar diretórios", create_directories),
        ("Configurar .env", setup_env_file),
        ("Testar importações", test_imports),
        ("Criar dados de exemplo", create_sample_data),
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print(f"⚠️ Falha em: {step_name}")
        except Exception as e:
            print(f"❌ Erro em {step_name}: {e}")
    
    print(f"\n📊 RESULTADO: {success_count}/{len(steps)} etapas concluídas")
    
    if success_count == len(steps):
        print("🎉 Setup concluído com sucesso!")
        show_next_steps()
    else:
        print("⚠️ Setup concluído com alguns problemas")
        print("   Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main()
