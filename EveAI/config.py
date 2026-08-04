import argparse
import logging
import os

# CONFIGURAÇÃO (agora via linha de comando, com valores padrão)


def parse_args():
    """Lê parâmetros opcionais de linha de comando (modelo, pasta de logs)."""
    parser = argparse.ArgumentParser(description="Eve - assistente local de programação")
    parser.add_argument("--modelo", default="llama3", help="Nome do modelo no Ollama")
    parser.add_argument("--logs", default="logs", help="Pasta onde salvar os logs da sessão")
    parser.add_argument(
        "--historico-max",
        type=int,
        default=10,
        help="Número máximo de trocas mantidas no contexto enviado ao modelo",
    )
    return parser.parse_args()


# LOGGING (erros reais agora vão para arquivo, não só para a tela)


def configurar_logging():
    """Configura logging em arquivo para registrar erros e eventos internos."""
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/eve.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )