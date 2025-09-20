"""
🤖 AI Chatbot Brasileiro
Aplicação principal Streamlit para o chatbot inteligente em português.
"""

import streamlit as st
import os
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="🤖 AI Chatbot Brasileiro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importações locais
from src.chatbot import ChatbotAI
from src.config import load_config
from src.database import ConversationDB
from src.personalities import PERSONALIDADES
from src.utils import format_message, export_conversation

def initialize_session_state():
    """Inicializa o estado da sessão do Streamlit."""
    if 'chatbot' not in st.session_state:
        config = load_config()
        st.session_state.chatbot = ChatbotAI(config)
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'current_personality' not in st.session_state:
        st.session_state.current_personality = 'assistente_geral'
    
    if 'db' not in st.session_state:
        st.session_state.db = ConversationDB()

def render_sidebar():
    """Renderiza a barra lateral com configurações."""
    st.sidebar.title("⚙️ Configurações")
    
    # Seleção de personalidade
    st.sidebar.subheader("🎭 Personalidade")
    personality_options = {key: f"{data['emoji']} {data['nome']}" 
                          for key, data in PERSONALIDADES.items()}
    
    selected_personality = st.sidebar.selectbox(
        "Escolha a personalidade:",
        options=list(personality_options.keys()),
        format_func=lambda x: personality_options[x],
        index=list(personality_options.keys()).index(st.session_state.current_personality)
    )
    
    if selected_personality != st.session_state.current_personality:
        st.session_state.current_personality = selected_personality
        st.session_state.chatbot.set_personality(selected_personality)
        st.rerun()
    
    # Configurações do modelo
    st.sidebar.subheader("🔧 Parâmetros do Modelo")
    
    temperature = st.sidebar.slider(
        "Criatividade (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Valores mais altos = respostas mais criativas"
    )
    
    max_tokens = st.sidebar.slider(
        "Tamanho da Resposta",
        min_value=50,
        max_value=500,
        value=150,
        step=25,
        help="Número máximo de tokens na resposta"
    )
    
    # Atualizar configurações do chatbot
    st.session_state.chatbot.update_config({
        'temperature': temperature,
        'max_tokens': max_tokens
    })
    
    # Histórico de conversas
    st.sidebar.subheader("📚 Histórico")
    
    if st.sidebar.button("🗑️ Limpar Conversa Atual"):
        st.session_state.conversation_history = []
        st.session_state.chatbot.clear_memory()
        st.rerun()
    
    if st.sidebar.button("💾 Salvar Conversa"):
        if st.session_state.conversation_history:
            conversation_id = st.session_state.db.save_conversation(
                st.session_state.conversation_history,
                st.session_state.current_personality
            )
            st.sidebar.success(f"Conversa salva! ID: {conversation_id}")
    
    # Exportar conversa
    if st.sidebar.button("📥 Exportar Conversa"):
        if st.session_state.conversation_history:
            json_data = export_conversation(st.session_state.conversation_history)
            st.sidebar.download_button(
                label="📄 Baixar JSON",
                data=json_data,
                file_name=f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def render_main_chat():
    """Renderiza a interface principal do chat."""
    st.title("🤖 AI Chatbot Brasileiro")
    
    # Informações da personalidade atual
    current_personality_data = PERSONALIDADES[st.session_state.current_personality]
    st.info(f"**Personalidade Ativa:** {current_personality_data['emoji']} {current_personality_data['nome']}")
    
    # Container para o histórico de mensagens
    chat_container = st.container()
    
    with chat_container:
        # Exibir histórico de conversas
        for i, message in enumerate(st.session_state.conversation_history):
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
    
    # Input para nova mensagem
    user_input = st.chat_input("Digite sua mensagem aqui...")
    
    if user_input:
        # Adicionar mensagem do usuário ao histórico
        user_message = {
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.conversation_history.append(user_message)
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.write(user_input)
        
        # Gerar resposta do chatbot
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = st.session_state.chatbot.generate_response(user_input)
                    st.write(response)
                    
                    # Adicionar resposta ao histórico
                    assistant_message = {
                        'role': 'assistant',
                        'content': response,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.session_state.conversation_history.append(assistant_message)
                    
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {str(e)}")
                    st.info("Verifique se sua API Key do OpenAI está configurada corretamente.")

def render_stats():
    """Renderiza estatísticas da conversa."""
    if st.session_state.conversation_history:
        st.sidebar.subheader("📊 Estatísticas")
        
        total_messages = len(st.session_state.conversation_history)
        user_messages = len([m for m in st.session_state.conversation_history if m['role'] == 'user'])
        assistant_messages = len([m for m in st.session_state.conversation_history if m['role'] == 'assistant'])
        
        st.sidebar.metric("Total de Mensagens", total_messages)
        st.sidebar.metric("Suas Mensagens", user_messages)
        st.sidebar.metric("Respostas do Bot", assistant_messages)

def main():
    """Função principal da aplicação."""
    # Verificar se a API Key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        st.error("⚠️ **API Key do OpenAI não configurada!**")
        st.info("""
        Para usar este chatbot, você precisa:
        1. Obter uma API Key do OpenAI em https://platform.openai.com/
        2. Criar um arquivo `.env` baseado no `.env.example`
        3. Adicionar sua API Key no arquivo `.env`
        """)
        st.stop()
    
    # Inicializar estado da sessão
    initialize_session_state()
    
    # Renderizar interface
    render_sidebar()
    render_main_chat()
    render_stats()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Dica:** Use a barra lateral para alterar a personalidade e configurações do chatbot."
    )

if __name__ == "__main__":
    main()
