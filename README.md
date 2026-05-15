# Eve 

**Eve** é uma assistente virtual local de programação, que roda 100% na sua máquina utilizando modelos de linguagem via [Ollama](https://ollama.com/). Sem nuvem, sem custos de API, sem envio de dados.

---

##  Funcionalidades

- **Conversa natural** com memória de contexto durante a sessão
- **Visão de tela** — Eve pode "olhar" para o que está na sua tela e comentar sobre isso
- **Log automático** — toda conversa é salva em JSON ao encerrar a sessão
- **Renderização Markdown** — respostas formatadas direto no terminal com suporte a código, listas e mais
- **Verificação de serviço** — avisa se o Ollama não estiver rodando antes de iniciar

---

## 🛠️ Requisitos

- Python 3.8+
- [Ollama](https://ollama.com/) instalado e rodando localmente
- Modelo `llama3` baixado no Ollama

### Dependências Python

```bash
pip install langchain-ollama pillow rich
```

---

##  Como usar

**1. Certifique-se de que o Ollama está rodando:**
```bash
ollama serve
```

**2. Baixe o modelo llama3 (caso ainda não tenha):**
```bash
ollama pull llama3
```

**3. Execute a Eve:**
```bash
python Eve.py
```

**4. Converse normalmente no terminal. Para encerrar:**
```
sair
```
ou `exit` / `quit`

---

##  Comandos especiais

| Comando | O que faz |
|---|---|
| `olhe para a tela` | Eve captura um print da tela e comenta sobre o que vê |
| `sair` / `exit` / `quit` | Encerra a sessão e salva o log |

---

## 📁 Estrutura de logs

Ao encerrar, a conversa é salva automaticamente na pasta `logs/`:

```
logs/
└── sessao_20240515_143022.json
```

Cada arquivo contém:
```json
{
    "data_hora_inicio": "2024-05-15 14:30:22",
    "modelo_utilizado": "llama3",
    "historico_conversa": [
        { "autor": "Usuário", "mensagem": "..." },
        { "autor": "Eve", "mensagem": "..." }
    ]
}
```

---

##  Estrutura do projeto

```
Eve.py          # Arquivo principal
logs/           # Gerado automaticamente ao encerrar
```

---

## 🔒 Privacidade

Todo o processamento acontece localmente. Nenhuma mensagem ou imagem é enviada para servidores externos.

---

## 📌 Observações

- A memória da Eve é **por sessão** — ao reiniciar, o histórico começa do zero (os logs anteriores ficam salvos em JSON)
- A funcionalidade de visão de tela (`olhe para a tela`) captura a tela no momento do comando, mas o modelo `llama3` padrão é somente texto. Para análise real de imagens, será necessário um modelo multimodal como o `llava`
- A funcionalidade de printar a tela esta com problemas, mas será corrigida logo


 <img width="1919" height="787" alt="Captura de tela 2026-05-15 141717" src="https://github.com/user-attachments/assets/b70feafe-0070-4560-bc84-ee59e6a87538" />
