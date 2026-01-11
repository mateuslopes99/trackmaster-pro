# 📦 TrackMaster Pro

Sistema completo de rastreamento de encomendas para E-commerce e Dropshipping com Dashboard Web e Bot do Telegram integrado.

## 🚀 Características

- **Dashboard Web Profissional**: Interface moderna em dark mode com Tailwind CSS
- **Bot do Telegram**: Respostas formatadas com emojis e negrito
- **API Linketrack**: Integração completa para rastreamento
- **Estatísticas em Tempo Real**: Total de pedidos, em trânsito e entregues
- **Histórico de Rastreamentos**: Tabela interativa com todos os rastreamentos
- **Design Premium**: Inspirado em Stripe com animações suaves

## 📋 Pré-requisitos

- Python 3.7+
- Conta no Telegram (para criar o bot)
- Credenciais da API Linketrack

## 🔧 Instalação

### 1. Clone ou baixe o projeto

```bash
cd project.google
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure suas credenciais

Abra o arquivo `flask_app.py` e edite as seguintes linhas:

```python
# Token do Bot do Telegram (obtenha com @BotFather)
TELEGRAM_TOKEN = 'COLE_SEU_TOKEN_AQUI'

# Credenciais da API Linketrack
LINKETRACK_USER = 'seu_usuario'
LINKETRACK_TOKEN = 'seu_token_aqui'
```

#### Como obter o Token do Telegram:

1. Abra o Telegram e procure por `@BotFather`
2. Envie o comando `/newbot`
3. Siga as instruções e copie o token fornecido
4. Cole o token no arquivo `flask_app.py`

#### Como obter credenciais da Linketrack:

1. Acesse [Linketrack](https://www.linketrack.com/)
2. Crie uma conta gratuita
3. Acesse a área de API e copie suas credenciais
4. Cole no arquivo `flask_app.py`

## ▶️ Como Executar

### Localmente

```bash
python flask_app.py
```

Acesse: `http://localhost:5000`

### No PythonAnywhere

1. Faça upload dos arquivos para sua conta
2. Configure um novo Web App (Flask)
3. Aponte para o arquivo `flask_app.py`
4. Instale as dependências via console
5. Recarregue o Web App

## 📱 Como Usar o Bot do Telegram

1. Procure pelo seu bot no Telegram (nome que você definiu)
2. Envie `/start` para ver a mensagem de boas-vindas
3. Envie qualquer código de rastreamento (ex: `BR123456789BR`)
4. Receba informações formatadas instantaneamente!

## 🎨 Funcionalidades do Dashboard

- **Estatísticas Animadas**: Contadores com animação suave
- **Rastreamento Rápido**: Campo de busca integrado
- **Histórico Completo**: Tabela com todos os rastreamentos
- **Auto-Refresh**: Atualização automática a cada 30 segundos
- **Download Report**: Botão visual (pode ser implementado futuramente)
- **Design Responsivo**: Funciona em desktop e mobile

## 🛠️ Estrutura do Projeto

```
project.google/
├── flask_app.py          # Backend Flask + Bot Telegram
├── templates/
│   └── index.html        # Dashboard Frontend
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🔒 Segurança

- Nunca compartilhe seus tokens publicamente
- Use variáveis de ambiente em produção
- Mantenha suas credenciais seguras

## 📝 Notas Importantes

- O sistema usa armazenamento em memória (simples para PythonAnywhere)
- Para produção, considere usar um banco de dados (SQLite, PostgreSQL)
- O bot roda em uma thread separada do Flask
- Certifique-se de que o TELEGRAM_TOKEN está configurado para ativar o bot

## 🎯 Próximas Melhorias (Sugestões)

- [ ] Banco de dados persistente (SQLite/PostgreSQL)
- [ ] Sistema de notificações automáticas
- [ ] Exportação de relatórios em PDF
- [ ] Múltiplos usuários com autenticação
- [ ] Webhooks do Telegram (mais eficiente que polling)
- [ ] Gráficos de estatísticas

## 💡 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as credenciais estão corretas
2. Confirme que as dependências foram instaladas
3. Verifique os logs do console para erros

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins comerciais ou pessoais.

---

**Desenvolvido para E-commerce & Dropshipping** 🚀
