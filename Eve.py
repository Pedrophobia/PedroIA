import os
import json
import sys
import time
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

# Componentes visuais do terminal
from rich.console import Console
from rich.markdown import Markdown

# Machine Learning e IA Local
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from langchain_ollama import OllamaLLM

# Configuração de atalhos: Enter = nova linha, Alt+Enter = enviar
bindings = KeyBindings()

@bindings.add(Keys.Enter)
def _(event):
    event.current_buffer.insert_text("\n")

@bindings.add(Keys.ControlJ)  # Control+Enter é interpretado como Escape+Enter no terminal
def _(event):
    event.current_buffer.validate_and_handle()

session = PromptSession(key_bindings=bindings)

console = Console()

# Inicializa o modelo do Ollama (Roda 100% offline no teu PC)
try:
    llm_local = OllamaLLM(model="llama3")
except Exception:
    console.print("[bold red]Eve: Erro ao iniciar o Ollama. Certifica-te de que o aplicativo está aberto![/bold red]")
    sys.exit(0)

# DOCUMENTAÇÃO: CARREGAR DADOS E TREINAR ML LOCAL

def carregar_intencoes():
    if not os.path.exists("intencoes.json"):
        console.print("[bold red]Erro: O arquivo 'intencoes.json' não foi encontrado![/bold red]")
        sys.exit(0)
    with open("intencoes.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Treinamento do classificador de intenções
dados_treino = carregar_intencoes()
textos = [item["frase"] for item in dados_treino]
intencoes = [item["intencao"] for item in dados_treino]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(textos)
y = intencoes

modelo_ml = LogisticRegression()
modelo_ml.fit(X, y)

# Estrutura de Logs para salvar a sessão
dados_da_sessao = {
    "data_hora_inicio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "modelo_utilizado": "ML_Local_+_Ollama_Offline",
    "historico_conversa": []
}

# DOCUMENTAÇÃO: REGRAS DE COMPORTAMENTO (PROMPT INJETADO)
def gerar_prompt_com_regras(intencao, comando_usuario, historico):
    """Garante que o Ollama obedeça às tuas regras com base na intenção do ML"""
    
    regras_base = """
    Você é a Eve, uma assistente virtual local de programação.
    Regras estritas de comportamento:
    1. Seja extremamente direta, curta, grossa e objetiva.
    2. NUNCA repita saudações. Não faça introduções como 'Eu sou uma assistente...'.
    3. Vá direto para o ponto ou para a resposta/correção do código.
    """
    
    if intencao == "ajuda_codigo":
        foco_contexto = "O usuário precisa de ajuda específica com programação ou correção de código."
    else:
        foco_contexto = "O usuário está a fazer uma conversa genérica ou saudação."

    return f"""
    {regras_base}
    
    Contexto da Intenção Atual: {foco_contexto}
    Histórico anterior: {historico}
    Pergunta/Código do Usuário: {comando_usuario}
    """

def salvar_log():
    if not os.path.exists("logs"):
        os.makedirs("logs") 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"logs/sessao_{timestamp}.json"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_da_sessao, f, ensure_ascii=False, indent=4)
        console.print(f"[bold blue]Eve: Log salvo em {nome_arquivo}[/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Eve: Erro ao salvar log: {e}[/bold red]")


# PROCESSAMENTO HÍBRIDO (ML DETECTA -> OLLAMA RESPONDE COM REGRAS)

def processar_assistente(comando_usuario, historico_conversa):
    # 1. ML local descobre o que o utilizador quer
    frase_vetorizada = vectorizer.transform([comando_usuario.lower()])
    intencao_prevista = modelo_ml.predict(frase_vetorizada)[0]
    
    # 2. Gera o prompt injetando as regras e intenção
    prompt_final = gerar_prompt_com_regras(
        intencao_prevista, 
        comando_usuario, 
        "\n".join(historico_conversa)
    )
    
    resposta_ia = ""
    inicio = time.time()
    
    # 3. Processa a resposta via Ollama com indicador de carregamento
    try:
        with console.status("[bold cyan]Eve está pensando...[/bold cyan]", spinner="dots"):
            for pedaco in llm_local.stream(prompt_final):
                resposta_ia += pedaco

        if not resposta_ia or not resposta_ia.strip():
            console.print("[bold red]Eve: Não consegui gerar uma resposta. Tenta novamente.[/bold red]")
            return
        tempo_gasto = time.time() - inicio

        # Exibe a resposta formatada
        console.print(f"\n[bold magenta]Eve:[/bold magenta] [dim](pensou por {tempo_gasto:.1f}s)[/dim]")
        console.print(Markdown(resposta_ia.strip()))
        
        # Atualiza o histórico e logs
        historico_conversa.append(f"Usuário: {comando_usuario}")
        historico_conversa.append(f"Eve: {resposta_ia}")
        dados_da_sessao["historico_conversa"].append({"autor": "Usuário", "mensagem": comando_usuario})
        dados_da_sessao["historico_conversa"].append({"autor": "Eve", "mensagem": resposta_ia})
        
    except Exception as e:
        console.print(f"[bold red]Eve: Erro ao processar com o Ollama: {e}[/bold red]")

def iniciar_programa():
    historico_conversa = []
    console.print("[bold green]🧠 Inteligência Híbrida (ML + Ollama Offline) Carregada![/bold green]")
    console.print("Eve: Olá. Como posso ajudar com o teu código hoje?")
    
    while True:
        usuario = session.prompt("\nVocê: ")
        
        if usuario.lower() in ["sair", "exit", "quit"]:
            console.print("[bold green]Eve: Até logo.[/bold green]")
            salvar_log()
            break
            
        if usuario.strip() == "":
            continue
        
        processar_assistente(usuario, historico_conversa)

if __name__ == "__main__":
    iniciar_programa()