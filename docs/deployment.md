# 🚀 Guia de Deploy - AI Chatbot Brasileiro

Este guia mostra como fazer deploy do seu chatbot em diferentes plataformas.

## 📋 Pré-requisitos

- Conta no GitHub
- API Key do OpenAI
- Python 3.8+ (para desenvolvimento local)

## 🌐 Streamlit Cloud (Recomendado)

### Vantagens
- ✅ Deploy gratuito
- ✅ Integração automática com GitHub
- ✅ SSL automático
- ✅ Fácil configuração

### Passos

1. **Prepare o repositório**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Acesse Streamlit Cloud**
   - Vá para [share.streamlit.io](https://share.streamlit.io)
   - Faça login com GitHub

3. **Configure o app**
   - Clique em "New app"
   - Selecione seu repositório
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Configure variáveis de ambiente**
   - Clique em "Advanced settings"
   - Adicione suas variáveis:
     ```
     OPENAI_API_KEY = "sua-chave-aqui"
     CHATBOT_NAME = "Seu Chatbot"
     ```

5. **Deploy**
   - Clique em "Deploy!"
   - Aguarde alguns minutos

### URL do seu app
Será algo como: `https://seu-usuario-ai-chatbot-brasileiro-streamlit-app-xyz.streamlit.app`

## 🐳 Docker

### Construir imagem
```bash
docker build -t ai-chatbot-brasileiro .
```

### Executar container
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="sua-chave" \
  ai-chatbot-brasileiro
```

### Docker Compose
```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=sua-chave
    volumes:
      - ./data:/app/data
```

## ☁️ Heroku

### Preparar arquivos

1. **Criar Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Criar runtime.txt**
   ```
   python-3.9.18
   ```

### Deploy
```bash
# Instalar Heroku CLI
heroku login
heroku create seu-chatbot-app

# Configurar variáveis
heroku config:set OPENAI_API_KEY="sua-chave"
heroku config:set CHATBOT_NAME="Seu Chatbot"

# Deploy
git push heroku main
```

## 🔧 Railway

1. **Conectar GitHub**
   - Acesse [railway.app](https://railway.app)
   - Conecte seu repositório

2. **Configurar variáveis**
   - Adicione `OPENAI_API_KEY`
   - Configure porta: `PORT=8501`

3. **Deploy automático**
   - Railway detecta automaticamente Streamlit

## 🌍 Render

1. **Criar Web Service**
   - Acesse [render.com](https://render.com)
   - Conecte repositório GitHub

2. **Configurações**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Variáveis de ambiente**
   - Adicione `OPENAI_API_KEY`

## 🔒 Configuração de Segurança

### Variáveis de Ambiente Obrigatórias
```env
OPENAI_API_KEY=sk-...
```

### Variáveis Opcionais
```env
CHATBOT_NAME=Meu Chatbot
MAX_TOKENS=150
TEMPERATURE=0.7
DEBUG=false
```

## 📊 Monitoramento

### Logs do Streamlit
```bash
# Ver logs em tempo real
streamlit run app.py --logger.level=debug
```

### Métricas importantes
- Tempo de resposta da API
- Número de usuários ativos
- Uso de tokens
- Erros de API

## 🔧 Troubleshooting

### Erro: "API Key não configurada"
- Verifique se `OPENAI_API_KEY` está definida
- Confirme que não há espaços extras na chave

### Erro: "Module not found"
- Verifique se `requirements.txt` está correto
- Confirme que todas as dependências estão listadas

### App muito lento
- Reduza `MAX_TOKENS`
- Implemente cache de respostas
- Use modelo mais rápido (gpt-3.5-turbo)

### Limite de tokens excedido
- Configure `MAX_TOKENS_PER_DAY`
- Implemente rate limiting
- Monitore uso da API

## 💡 Dicas de Performance

1. **Cache de respostas**
   ```python
   @st.cache_data
   def cached_response(prompt):
       return chatbot.generate_response(prompt)
   ```

2. **Lazy loading**
   - Carregue componentes apenas quando necessário

3. **Otimização de tokens**
   - Limite histórico de conversa
   - Use prompts mais concisos

## 🔄 CI/CD

### GitHub Actions
```yaml
name: Deploy to Streamlit
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit
        run: echo "Deploy automático configurado"
```

## 📈 Escalabilidade

### Para muitos usuários
- Use Redis para cache
- Implemente queue de requisições
- Configure load balancer

### Banco de dados
- Migre de SQLite para PostgreSQL
- Configure backup automático
- Implemente replicação

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs da aplicação
2. Confirme configurações de ambiente
3. Teste localmente primeiro
4. Abra uma issue no GitHub

**Boa sorte com seu deploy! 🚀**
