# 🤖 AI Chatbot Brasileiro

Um chatbot inteligente em português com integração OpenAI GPT, interface moderna e sistema de memória de conversas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 **Características**

- ✅ **Interface em Português**: Totalmente localizada para o mercado brasileiro
- ✅ **OpenAI GPT Integration**: Powered by GPT-3.5/GPT-4
- ✅ **Memória de Conversas**: Sistema inteligente de contexto
- ✅ **Interface Moderna**: UI responsiva com Streamlit
- ✅ **Configurações Flexíveis**: Personalize comportamento e personalidade
- ✅ **Deploy Fácil**: Pronto para Streamlit Cloud, Heroku ou Docker
- ✅ **Histórico de Conversas**: Salva e carrega conversas anteriores
- ✅ **Múltiplas Personalidades**: Assistente, Especialista, Criativo, etc.

## 🚀 **Demo Online**

[🔗 Experimente o Chatbot](https://seu-chatbot.streamlit.app) *(em breve)*

## 📸 **Screenshots**

![Chatbot Interface](docs/images/chatbot-interface.png)
![Configurações](docs/images/configuracoes.png)

## 🛠️ **Tecnologias Utilizadas**

- **Python 3.8+**
- **Streamlit** - Interface web moderna
- **OpenAI API** - Inteligência artificial
- **SQLite** - Banco de dados local
- **Pandas** - Manipulação de dados
- **Python-dotenv** - Gerenciamento de variáveis

## ⚡ **Instalação Rápida**

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/ai-chatbot-brasileiro.git
cd ai-chatbot-brasileiro
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure sua API Key
```bash
cp .env.example .env
# Edite o arquivo .env com sua OpenAI API Key
```

### 4. Execute o chatbot
```bash
streamlit run app.py
```

## 🔧 **Configuração**

### Obtenha sua OpenAI API Key

1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Vá em "API Keys" e crie uma nova chave
4. Copie a chave para o arquivo `.env`

### Arquivo .env
```env
OPENAI_API_KEY=sua-chave-aqui
CHATBOT_NAME=Assistente IA
CHATBOT_PERSONALITY=Você é um assistente útil e amigável que fala português brasileiro.
MAX_TOKENS=150
TEMPERATURE=0.7
```

## 📱 **Como Usar**

1. **Inicie uma Conversa**: Digite sua mensagem na caixa de texto
2. **Escolha a Personalidade**: Selecione entre diferentes tipos de assistente
3. **Configure Parâmetros**: Ajuste criatividade e tamanho das respostas
4. **Salve Conversas**: Suas conversas são automaticamente salvas
5. **Exporte Histórico**: Baixe suas conversas em formato JSON

## 🎯 **Personalidades Disponíveis**

- 🤝 **Assistente Geral**: Ajuda com tarefas diversas
- 💼 **Consultor de Negócios**: Especialista em estratégia empresarial
- 🎨 **Assistente Criativo**: Focado em criatividade e brainstorming
- 📚 **Tutor Educacional**: Especialista em ensino e aprendizagem
- 💻 **Desenvolvedor**: Especialista em programação e tecnologia
- 🏥 **Assistente de Saúde**: Informações gerais sobre bem-estar

## 🔧 **Personalização**

### Adicionar Nova Personalidade

```python
# Em src/personalities.py
PERSONALIDADES = {
    "nova_personalidade": {
        "nome": "Seu Nome",
        "prompt": "Você é um especialista em...",
        "emoji": "🎯"
    }
}
```

### Configurar Parâmetros do Modelo

```python
# Em src/config.py
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",  # ou "gpt-4"
    "max_tokens": 150,
    "temperature": 0.7,
    "top_p": 1.0
}
```

## 📊 **Estrutura do Projeto**

```
ai-chatbot-brasileiro/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Este arquivo
├── src/
│   ├── __init__.py
│   ├── chatbot.py       # Lógica principal do chatbot
│   ├── config.py        # Configurações
│   ├── database.py      # Gerenciamento do banco de dados
│   ├── personalities.py # Personalidades do chatbot
│   └── utils.py         # Funções utilitárias
├── data/
│   └── conversations.db # Banco de dados SQLite
├── docs/
│   ├── images/          # Screenshots e imagens
│   └── deployment.md    # Guia de deploy
└── tests/
    ├── __init__.py
    ├── test_chatbot.py  # Testes do chatbot
    └── test_database.py # Testes do banco
```

## 🚀 **Deploy**

### Streamlit Cloud (Recomendado)
1. Faça push do código para GitHub
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
3. Conecte seu repositório
4. Configure as variáveis de ambiente
5. Deploy automático!

### Heroku
```bash
# Instale Heroku CLI e execute:
heroku create seu-chatbot-app
heroku config:set OPENAI_API_KEY=sua-chave
git push heroku main
```

### Docker
```bash
docker build -t ai-chatbot-brasileiro .
docker run -p 8501:8501 ai-chatbot-brasileiro
```

## 🧪 **Testes**

```bash
# Execute todos os testes
python -m pytest tests/

# Teste específico
python -m pytest tests/test_chatbot.py -v

# Com cobertura
python -m pytest tests/ --cov=src
```

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌟 **Roadmap**

- [ ] Integração com WhatsApp API
- [ ] Suporte a múltiplos idiomas
- [ ] Sistema de plugins
- [ ] API REST
- [ ] Interface mobile
- [ ] Integração com Telegram
- [ ] Sistema de analytics
- [ ] Modo offline com modelos locais

## 💰 **Serviços Profissionais**

Precisa de customização ou suporte profissional?

- 🔧 **Customização Completa**: R$ 500-1.500
- 🚀 **Deploy e Configuração**: R$ 200-500
- 📱 **Integração WhatsApp/Telegram**: R$ 300-800
- 🎯 **Treinamento Personalizado**: R$ 400-1.000

**Entre em contato para orçamento personalizado!**

---

⭐ **Se este projeto foi útil, deixe uma estrela no GitHub!**

Desenvolvido com ❤️ por [Seu Nome](https://github.com/seu-usuario)
