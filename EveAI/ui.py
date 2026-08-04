from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from rich.console import Console

console = Console()

# TERMINAL / ATALHOS


def criar_sessao_prompt():
    """Cria a sessão de input: Enter = nova linha, Ctrl+Enter = enviar mensagem."""
    bindings = KeyBindings()

    @bindings.add(Keys.Enter)
    def _(event):
        event.current_buffer.insert_text("\n")

    @bindings.add(Keys.ControlJ)
    def _(event):
        event.current_buffer.validate_and_handle()

    return PromptSession(key_bindings=bindings)