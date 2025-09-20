"""
Gerenciamento do banco de dados para o AI Chatbot Brasileiro
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

class ConversationDB:
    """
    Classe para gerenciar o banco de dados de conversas.
    """
    
    def __init__(self, db_path: str = "data/conversations.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Inicializar banco de dados
        self._init_database()
    
    def _init_database(self) -> None:
        """Cria as tabelas necessárias no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de conversas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    personality TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    message_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Tabela de mensagens
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            # Índices para melhor performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversations_personality 
                ON conversations (personality)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
                ON messages (conversation_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
                ON messages (timestamp)
            """)
            
            conn.commit()
    
    def save_conversation(self, messages: List[Dict[str, Any]], personality: str) -> str:
        """
        Salva uma conversa no banco de dados.
        
        Args:
            messages: Lista de mensagens da conversa
            personality: Personalidade usada na conversa
            
        Returns:
            ID da conversa salva
        """
        conversation_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        # Calcular tempos de início e fim
        start_time = messages[0]['timestamp'] if messages else current_time
        end_time = messages[-1]['timestamp'] if messages else current_time
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Inserir conversa
            cursor.execute("""
                INSERT INTO conversations 
                (id, personality, start_time, end_time, message_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                conversation_id,
                personality,
                start_time,
                end_time,
                len(messages),
                current_time,
                current_time
            ))
            
            # Inserir mensagens
            for message in messages:
                cursor.execute("""
                    INSERT INTO messages 
                    (conversation_id, role, content, timestamp, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    message['role'],
                    message['content'],
                    message['timestamp'],
                    current_time
                ))
            
            conn.commit()
        
        return conversation_id
    
    def load_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Carrega uma conversa do banco de dados.
        
        Args:
            conversation_id: ID da conversa
            
        Returns:
            Dicionário com dados da conversa ou None se não encontrada
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Buscar dados da conversa
            cursor.execute("""
                SELECT * FROM conversations WHERE id = ?
            """, (conversation_id,))
            
            conversation = cursor.fetchone()
            if not conversation:
                return None
            
            # Buscar mensagens
            cursor.execute("""
                SELECT role, content, timestamp 
                FROM messages 
                WHERE conversation_id = ? 
                ORDER BY timestamp ASC
            """, (conversation_id,))
            
            messages = [dict(row) for row in cursor.fetchall()]
            
            return {
                "id": conversation["id"],
                "personality": conversation["personality"],
                "start_time": conversation["start_time"],
                "end_time": conversation["end_time"],
                "message_count": conversation["message_count"],
                "created_at": conversation["created_at"],
                "messages": messages
            }
    
    def list_conversations(self, limit: int = 50, personality: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lista conversas salvas.
        
        Args:
            limit: Número máximo de conversas a retornar
            personality: Filtrar por personalidade (opcional)
            
        Returns:
            Lista de conversas
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = """
                SELECT id, personality, start_time, end_time, message_count, created_at
                FROM conversations
            """
            params = []
            
            if personality:
                query += " WHERE personality = ?"
                params.append(personality)
            
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Deleta uma conversa do banco de dados.
        
        Args:
            conversation_id: ID da conversa
            
        Returns:
            True se deletada com sucesso, False caso contrário
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Deletar mensagens primeiro (devido à foreign key)
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            
            # Deletar conversa
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            
            conn.commit()
            
            return cursor.rowcount > 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do banco de dados.
        
        Returns:
            Dicionário com estatísticas
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total de conversas
            cursor.execute("SELECT COUNT(*) FROM conversations")
            total_conversations = cursor.fetchone()[0]
            
            # Total de mensagens
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]
            
            # Conversas por personalidade
            cursor.execute("""
                SELECT personality, COUNT(*) as count 
                FROM conversations 
                GROUP BY personality 
                ORDER BY count DESC
            """)
            conversations_by_personality = dict(cursor.fetchall())
            
            # Conversa mais recente
            cursor.execute("""
                SELECT created_at FROM conversations 
                ORDER BY created_at DESC LIMIT 1
            """)
            last_conversation = cursor.fetchone()
            last_conversation_date = last_conversation[0] if last_conversation else None
            
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "conversations_by_personality": conversations_by_personality,
                "last_conversation_date": last_conversation_date
            }
    
    def cleanup_old_conversations(self, days_old: int = 30) -> int:
        """
        Remove conversas antigas do banco de dados.
        
        Args:
            days_old: Número de dias para considerar uma conversa como antiga
            
        Returns:
            Número de conversas removidas
        """
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_old)
        cutoff_str = cutoff_date.isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Buscar IDs das conversas antigas
            cursor.execute("""
                SELECT id FROM conversations WHERE created_at < ?
            """, (cutoff_str,))
            
            old_conversation_ids = [row[0] for row in cursor.fetchall()]
            
            if not old_conversation_ids:
                return 0
            
            # Deletar mensagens das conversas antigas
            placeholders = ','.join('?' * len(old_conversation_ids))
            cursor.execute(f"""
                DELETE FROM messages WHERE conversation_id IN ({placeholders})
            """, old_conversation_ids)
            
            # Deletar conversas antigas
            cursor.execute(f"""
                DELETE FROM conversations WHERE id IN ({placeholders})
            """, old_conversation_ids)
            
            conn.commit()
            
            return len(old_conversation_ids)
