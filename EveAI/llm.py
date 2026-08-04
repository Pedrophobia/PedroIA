import logging
import textwrap
import time
from rich.markdown import Markdown

from session import SessaoChat
from ui import console
from Ester_eggs import EASTER_EGGS

# CLASSIFICADOR DE INTENÇÃO (troca do ML por palavras-chave)


PALAVRAS_CODIGO = {
    "erro", "bug", "função", "funcao", "código", "codigo", "script",
    "exceção", "excecao", "traceback", "compilar", "debug", "classe",
    "variável", "variavel", "loop", "algoritmo", "corrigir", "refatorar",
}


def detectar_intencao(frase: str) -> str:
    """Classifica a frase como 'ajuda_codigo' ou 'conversa_geral' via palavras-chave."""
    palavras = set(frase.lower().split())
    if palavras & PALAVRAS_CODIGO:
        return "ajuda_codigo"
    return "conversa_geral"


def detectar_easter_egg(frase: str) -> str | None:
    """Retorna a chave do easter egg encontrado na frase, ou None se não houver."""
    frase_lower = frase.lower()
    for gatilho in EASTER_EGGS:
        if gatilho in frase_lower:
            return gatilho
    return None


# PROMPT


REGRAS_BASE = textwrap.dedent("""\
    Você é a Eve, uma assistente virtual local de programação.
    Regras estritas de comportamento:
    1. Seja extremamente direta, curta e objetiva.
    2. NUNCA repita saudações. Não faça introduções como 'Eu sou uma assistente...'.
    3. Vá direto para o ponto ou para a resposta/correção do código.
    """)


def gerar_prompt_com_regras(intencao: str, comando_usuario: str, historico_formatado: str) -> str:
    """Monta o prompt final injetando regras fixas + contexto da intenção + histórico."""
    foco_contexto = (
        "O usuário precisa de ajuda específica com programação ou correção de código."
        if intencao == "ajuda_codigo"
        else "O usuário está a fazer uma conversa genérica ou saudação."
    )
    return textwrap.dedent(f"""\
        {REGRAS_BASE}

        Contexto da Intenção Atual: {foco_contexto}
        Histórico anterior: {historico_formatado}
        Pergunta/Código do Usuário: {comando_usuario}
    """)


# PROCESSAMENTO PRINCIPAL


def processar_assistente(comando_usuario: str, sessao: SessaoChat, llm_local):
    """Detecta intenção, monta prompt, transmite a resposta do modelo e atualiza histórico/log."""
    intencao = detectar_intencao(comando_usuario)
    gatilho = detectar_easter_egg(comando_usuario)
    if gatilho:
        resposta_easter_egg = EASTER_EGGS[gatilho]()
        console.print(f"[bold yellow]Eve: {resposta_easter_egg}[/bold yellow]")
        return
    prompt_final = gerar_prompt_com_regras(
        intencao, comando_usuario, sessao.historico_formatado()
    )

    resposta_ia = ""
    inicio = time.time()

    try:
        console.print("\n[bold magenta]Eve:[/bold magenta]")
        with console.status("[bold cyan]Eve está pensando...[/bold cyan]", spinner="dots"):
            primeiro_pedaco = True
            for pedaco in llm_local.stream(prompt_final):
                if primeiro_pedaco:
                    primeiro_pedaco = False
                resposta_ia += pedaco

        if not resposta_ia.strip():
            console.print("[bold red]Eve: Não consegui gerar uma resposta. Tenta novamente.[/bold red]")
            return

        tempo_gasto = time.time() - inicio
        console.print(f"[dim](pensou por {tempo_gasto:.1f}s)[/dim]")
        console.print(Markdown(resposta_ia.strip()))

        sessao.registrar("Usuário", comando_usuario)
        sessao.registrar("Eve", resposta_ia.strip())

    except Exception as e:
        logging.exception("Erro ao processar resposta do Ollama")
        console.print(f"[bold red]Eve: Erro ao processar com o Ollama: {e}[/bold red]")