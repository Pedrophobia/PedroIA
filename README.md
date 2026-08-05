# 🧠 Eve — Assistente Local de Programação

> ⚠️ **Aviso Importante:** > * **Uso de Inteligência Artificial:** Neste projeto foi utilizado IA (inteligência Artificial) que **criaram e alteraram partes do código**.
> * **Projeto em Desenvolvimento:** Esta ferramenta **ainda não está completa** e encontra-se em fase ativa de construção (WIP).

Eve é um assistente virtual de linha de comando (CLI) voltado para auxílio no desenvolvimento de software. O projeto roda **100% local e offline**, integrando a biblioteca **LangChain** com o **Ollama** para processar suas solicitações e manipular código sem enviar dados para servidores externos.

---

## 🚀 Funcionalidades Principais

* 🛠️ **Geração e Edição de Código:** A IA analisa suas solicitações e altera ou cria trechos de código conforme necessário.
* 🔒 **100% Offline & Privado:** Execução totalmente local via Ollama.
* ⌨️ **Interface rica no Terminal:** Suporte a atalhos customizados (ex: `Enter` para nova linha, `Ctrl+J` para enviar) via `prompt_toolkit`.
* 📝 **Formatado com Rich:** Respostas e códigos formatados em Markdown diretamente no terminal.
* 💾 **Histórico & Logs Automatizados:** Histórico da conversa salvo automaticamente em arquivos JSON na pasta de logs ao sair.
* 🎯 **Detecção de Intenção:** Diferencia dúvidas/alterações de código de conversas casuais.
* 🐣 **Easter Eggs:** Respostas divertidas para gatilhos específicos no terminal.

---

## 🛠️ Pré-requisitos

Antes de iniciar, você precisa ter instalado no seu sistema:

1. **Python 3.10+**
2. **Ollama** (com o modelo `llama3` ou outro de sua preferência baixado):
   ```bash
   ollama run llama3
