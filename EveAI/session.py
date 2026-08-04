import logging
import os
from datetime import datetime

# HISTÓRICO E LOG DE SESSÃO (uma única fonte de verdade)


class SessaoChat:
    """Guarda o histórico da conversa em um único lugar e formata para o prompt ou para o log."""

    def __init__(self, modelo: str, historico_max: int):
        self.historico_max = historico_max
        self.dados = {
            "data_hora_inicio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modelo_utilizado": modelo,
            "historico_conversa": [],
        }

    def registrar(self, autor: str, mensagem: str):
        self.dados["historico_conversa"].append({"autor": autor, "mensagem": mensagem})

    def historico_formatado(self) -> str:
        """Retorna as últimas N trocas formatadas como texto, para caber no prompt."""
        recentes = self.dados["historico_conversa"][-(self.historico_max * 2):]
        return "\n".join(f'{item["autor"]}: {item["mensagem"]}' for item in recentes)

    def salvar(self, pasta_logs: str):
        os.makedirs(pasta_logs, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(pasta_logs, f"sessao_{timestamp}.json")
        try:
            import json
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=4)
            return caminho
        except Exception as e:
            logging.exception("Falha ao salvar log da sessão")
            raise