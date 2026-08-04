import logging
import sys
from langchain_ollama import OllamaLLM

from config import configurar_logging, parse_args
from llm import processar_assistente
from session import SessaoChat
from ui import console, criar_sessao_prompt

# LOOP PRINCIPAL


def iniciar_programa():
    args = parse_args()
    configurar_logging()
    session = criar_sessao_prompt()

    try:
        llm_local = OllamaLLM(model=args.modelo)
    except Exception as e:
        logging.exception("Erro ao iniciar o Ollama")
        console.print(
            "[bold red]Eve: Erro ao iniciar o Ollama. Certifica-te de que o aplicativo está aberto![/bold red]"
        )
        console.print(f"[dim]{e}[/dim]")
        sys.exit(1)

    sessao = SessaoChat(modelo=args.modelo, historico_max=args.historico_max)

    console.print("[bold green]🧠 Eve carregada (Ollama offline)![/bold green]")
    console.print("Eve: Olá. Como posso ajudar com o teu código hoje?")

    try:
        while True:
            usuario = session.prompt("\nVocê: ")

            if usuario.lower() in ["sair", "exit", "quit"]:
                console.print("[bold green]Eve: Até logo.[/bold green]")
                break

            if usuario.strip() == "":
                continue

            processar_assistente(usuario, sessao, llm_local)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold yellow]Eve: Sessão interrompida pelo usuário.[/bold yellow]")

    finally:
        try:
            caminho = sessao.salvar(args.logs)
            console.print(f"[bold blue]Eve: Log salvo em {caminho}[/bold blue]")
        except Exception:
            console.print(
                "[bold red]Eve: Não foi possível salvar o log (veja logs/eve.log).[/bold red]"
            )


if __name__ == "__main__":
    iniciar_programa()