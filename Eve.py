from langchain_ollama import OllamaLLM
from PIL import ImageGrab
#Console Rich
from rich.console import Console
from rich.markdown import Markdown

# inicializador
llm_local = OllamaLLM(model="llama3")
console = Console()

def regras_de_comportamento(comando_usuario, historico_conversa):
    """Retorna o prompt estuturado com as regas de comportamento da Eve"""
    return f"""
    Você é a Eve, uma assistente virtual local.
        
        Regras estritas de comportamento:
        1. Seja extremamente direta, curta e objetiva.
        2. NUNCA repita saudações, apenas diga quem você é  como 'Eve' e não faça introduções como 'Eu sou uma assistente...'.
        3. Vá direto para a resposta da pergunta do usuário.
        
        
        Histórico das conversas anteriores: {historico_conversa}
        Pergunta ou Código atual do usuário: {comando_usuario}
        """

def processar_assistente(comando_usuario, historico_conversa):
    comando = comando_usuario.lower()

    # FUNCIONALIDADE visao de tela
    if "olhe para a tela" in comando:
        console.print("Eve: Olhando para a tela...")
        imagem = ImageGrab.grab()
        console.print("[bold cyan]Eve: Processando a imagem...")
        prompt_visao = (
            "O usuário acabou de tirar um print da tela do computador dele. "
            "Como uma assistente prestativa, responda de forma acolhedora, pergunte o que está "
            "acontecendo na tela dele e como você pode ajudá-lo."
        )
        resposta_ia = llm_local.invoke(prompt_visao)
        console.print(f"[bold green]Eve: {resposta_ia}")
        return
        
    # FUNCIONALIDADE conversa normal
    else:
        prompt_sistema = regras_de_comportamento(comando_usuario, historico_conversa)   
        console.print("Eve: Processando sua pergunta...")
        try:
            resposta_ia = llm_local.invoke(prompt_sistema)
            console.print(f"[bold green]Eve: {resposta_ia.strip()}") # O .strip() remove espaços vazios inúteis
            historico_conversa.append(f"Usuário: {comando_usuario}")
            historico_conversa.append(f"Eve: {resposta_ia}")
        except Exception as e:
            console.print(f"[bold red]Eve: Ocorreu um erro ao processar sua pergunta: {e}")


# CORACAO do Programa 
def iniciar_programa():
    historico_conversa = []
    console.print("Eve: Olá! Sou a Eve, sua assistente virtual de programação local. Como posso ajudar você hoje?")
    
    while True:
        usuario = input("Você: ")
        if usuario.lower() in ["sair", "exit", "quit"]:
            console.print(f"[bold pink]Eve: Até logo! Se precisar de ajuda, estarei aqui.")
            break
        if usuario.strip() == "":
            console.print(f"[bold red]Eve: Por favor, digite algo para que eu possa ajudar.")
            continue
        
        processar_assistente(usuario, historico_conversa)

# deve ser alinhado a esquerda
if __name__ == "__main__":
    iniciar_programa()