from langchain_ollama import OllamaLLM
from PIL import ImageGrab
#Console Rich
from rich.console import Console
from rich.markdown import Markdown
#import para os logs
import os
import json
from datetime import datetime

# inicializador
llm_local = OllamaLLM(model="llama3")
console = Console()

dados_da_sessao = {
    "data_hora_inicio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "modelo_utilizado": "llama3",
    "historico_conversa": []
}


def regras_de_comportamento(comando_usuario, historico_conversa):
    """Retorna o prompt estuturado com as regas de comportamento da Eve"""
    return f"""
    Você é a Eve, uma assistente virtual local.
        
        Regras estritas de comportamento:
        1. Seja extremamente direta, corta e objetiva.
        2. NUNCA repita saudações, apenas diga quem você é  como 'Eve' e não faça introduções como 'Eu sou uma assistente...'.
        3. Vá direto para a resposta da pergunta do usuário.
        
        
        Histórico das conversas anteriores: {historico_conversa}
        Pergunta ou Código atual do usuário: {comando_usuario}
        """

def salvar_log():
    """função que cira a pasta de logs e salva a conversa em formato json"""
    # Criar a pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs") 
    
    #gera o nome do arquivo com a data e hora atual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"logs/sessao_{timestamp}.json"
    # salva os dados da sessão em formato json
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_da_sessao, f, ensure_ascii=False, indent=4)
        console.print(f"[bold blue]Eve: Conversa salva em {nome_arquivo}")
    except Exception as e:
        console.print(f"[bold red]Eve: Ocorreu um erro ao salvar o log: {e}")
         

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
        #guarda a interacao no json de logs
        dados_da_sessao["historico_conversa"].append({"autor": "Usuário", "mensagem": comando_usuario})
        dados_da_sessao["historico_conversa"].append({"autor": "Eve", "mensagem": resposta_ia})
        return
        
    # FUNCIONALIDADE conversa normal
    else:
        console.print("[bold yellow]Eve: Processando sua pergunta...[/bold yellow]")
        try:
            prompt_sistema = regras_de_comportamento(comando_usuario, historico_conversa)
            resposta_ia = llm_local.invoke(prompt_sistema)
            
            console.print("\n[bold magenta]Eve:[/bold magenta]")
            console.print(Markdown(resposta_ia.strip()))
            
            # Alimenta a memória temporária do terminal
            historico_conversa.append(f"Usuário: {comando_usuario}")
            historico_conversa.append(f"Eve: {resposta_ia}")
            
            # Alimenta a nossa estrutura JSON definitiva para os logs
            dados_da_sessao["historico_conversa"].append({"autor": "Usuário", "mensagem": comando_usuario})
            dados_da_sessao["historico_conversa"].append({"autor": "Eve", "mensagem": resposta_ia})
            
        except Exception as e:
            console.print(f"[bold red]Eve: Ocorreu um erro ao processar sua pergunta: {e}[/bold red]")

# CORACAO do Programa 
def iniciar_programa():
    historico_conversa = []
    console.print("Eve: Olá! Sou a Eve, sua assistente virtual de programação local. Como posso ajudar você hoje?")
    
    while True:
        usuario = input("\nVocê: ")
        if usuario.lower() in ["sair", "exit", "quit"]:
            console.print("[bold green]Eve: Até logo! Se precisar de ajuda, estarei aqui.[/bold green]")
            # CHAMA A FUNÇÃO DE LOG LOGO ANTES DE FECHAR O PROGRAMA
            salvar_log()
            break
        if usuario.strip() == "":
            console.print("[bold red]Eve: Por favor, digite algo para que eu possa ajudar.[/bold red]")
            continue
        
        processar_assistente(usuario, historico_conversa)

# deve ser alinhado a esquerda
if __name__ == "__main__":
    iniciar_programa()