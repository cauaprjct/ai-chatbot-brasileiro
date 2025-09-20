"""
Funções utilitárias para o AI Chatbot Brasileiro
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

def format_message(message: str, max_length: int = 1000) -> str:
    """
    Formata uma mensagem para exibição.
    
    Args:
        message: Mensagem a ser formatada
        max_length: Comprimento máximo da mensagem
        
    Returns:
        Mensagem formatada
    """
    # Truncar se muito longa
    if len(message) > max_length:
        message = message[:max_length] + "..."
    
    # Remover espaços extras
    message = re.sub(r'\s+', ' ', message.strip())
    
    return message

def export_conversation(conversation_history: List[Dict[str, Any]]) -> str:
    """
    Exporta o histórico de conversa para JSON.
    
    Args:
        conversation_history: Lista de mensagens da conversa
        
    Returns:
        String JSON formatada
    """
    export_data = {
        "export_info": {
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(conversation_history),
            "app_version": "1.0.0"
        },
        "conversation": conversation_history
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def import_conversation(json_data: str) -> Optional[List[Dict[str, Any]]]:
    """
    Importa uma conversa de dados JSON.
    
    Args:
        json_data: String JSON com dados da conversa
        
    Returns:
        Lista de mensagens ou None se erro
    """
    try:
        data = json.loads(json_data)
        
        # Verificar se tem a estrutura esperada
        if "conversation" in data:
            return data["conversation"]
        elif isinstance(data, list):
            return data
        else:
            return None
            
    except json.JSONDecodeError:
        return None

def calculate_tokens_estimate(text: str) -> int:
    """
    Estima o número de tokens em um texto.
    Aproximação: 1 token ≈ 4 caracteres em português.
    
    Args:
        text: Texto para estimar tokens
        
    Returns:
        Número estimado de tokens
    """
    return len(text) // 4

def format_timestamp(timestamp_str: str) -> str:
    """
    Formata um timestamp para exibição amigável.
    
    Args:
        timestamp_str: String do timestamp ISO
        
    Returns:
        String formatada para exibição
    """
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y às %H:%M")
    except:
        return timestamp_str

def validate_openai_key(api_key: str) -> bool:
    """
    Valida se uma API key do OpenAI tem formato válido.
    
    Args:
        api_key: Chave da API
        
    Returns:
        True se válida, False caso contrário
    """
    if not api_key:
        return False
    
    # Formato básico: sk-...
    if not api_key.startswith('sk-'):
        return False
    
    # Comprimento mínimo
    if len(api_key) < 20:
        return False
    
    return True

def create_download_link(data: str, filename: str, mime_type: str = "text/plain") -> str:
    """
    Cria um link de download para dados.
    
    Args:
        data: Dados para download
        filename: Nome do arquivo
        mime_type: Tipo MIME do arquivo
        
    Returns:
        HTML do link de download
    """
    import base64
    
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">📥 Baixar {filename}</a>'
    return href

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza um nome de arquivo removendo caracteres inválidos.
    
    Args:
        filename: Nome do arquivo original
        
    Returns:
        Nome do arquivo sanitizado
    """
    # Remover caracteres inválidos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remover espaços extras e pontos no final
    filename = filename.strip('. ')
    
    # Garantir que não está vazio
    if not filename:
        filename = "arquivo"
    
    return filename

def get_conversation_stats(conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula estatísticas de uma conversa.
    
    Args:
        conversation_history: Lista de mensagens
        
    Returns:
        Dicionário com estatísticas
    """
    if not conversation_history:
        return {
            "total_messages": 0,
            "user_messages": 0,
            "assistant_messages": 0,
            "total_characters": 0,
            "estimated_tokens": 0,
            "duration": None
        }
    
    user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
    assistant_messages = [msg for msg in conversation_history if msg.get('role') == 'assistant']
    
    total_characters = sum(len(msg.get('content', '')) for msg in conversation_history)
    estimated_tokens = calculate_tokens_estimate(''.join(msg.get('content', '') for msg in conversation_history))
    
    # Calcular duração se houver timestamps
    duration = None
    if conversation_history and 'timestamp' in conversation_history[0] and 'timestamp' in conversation_history[-1]:
        try:
            start_time = datetime.fromisoformat(conversation_history[0]['timestamp'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(conversation_history[-1]['timestamp'].replace('Z', '+00:00'))
            duration = str(end_time - start_time)
        except:
            pass
    
    return {
        "total_messages": len(conversation_history),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "total_characters": total_characters,
        "estimated_tokens": estimated_tokens,
        "duration": duration
    }

def display_message_with_avatar(role: str, content: str, timestamp: Optional[str] = None):
    """
    Exibe uma mensagem com avatar no Streamlit.
    
    Args:
        role: 'user' ou 'assistant'
        content: Conteúdo da mensagem
        timestamp: Timestamp opcional
    """
    avatar = "🧑‍💻" if role == "user" else "🤖"
    
    with st.chat_message(role, avatar=avatar):
        st.write(content)
        if timestamp:
            st.caption(f"📅 {format_timestamp(timestamp)}")

def check_rate_limit(session_state_key: str, max_requests: int = 20, time_window: int = 60) -> bool:
    """
    Verifica se o usuário está dentro do limite de requisições.
    
    Args:
        session_state_key: Chave para armazenar dados no session state
        max_requests: Número máximo de requisições
        time_window: Janela de tempo em segundos
        
    Returns:
        True se dentro do limite, False caso contrário
    """
    current_time = datetime.now()
    
    if session_state_key not in st.session_state:
        st.session_state[session_state_key] = []
    
    # Remover requisições antigas
    cutoff_time = current_time.timestamp() - time_window
    st.session_state[session_state_key] = [
        req_time for req_time in st.session_state[session_state_key] 
        if req_time > cutoff_time
    ]
    
    # Verificar limite
    if len(st.session_state[session_state_key]) >= max_requests:
        return False
    
    # Adicionar requisição atual
    st.session_state[session_state_key].append(current_time.timestamp())
    return True

def create_personality_badge(personality_key: str, personality_data: Dict[str, str]) -> str:
    """
    Cria um badge HTML para uma personalidade.
    
    Args:
        personality_key: Chave da personalidade
        personality_data: Dados da personalidade
        
    Returns:
        HTML do badge
    """
    return f"""
    <div style="
        display: inline-block;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        margin: 2px;
    ">
        {personality_data['emoji']} {personality_data['nome']}
    </div>
    """
