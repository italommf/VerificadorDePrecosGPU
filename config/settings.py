from pathlib import Path
from decouple import config

NOME_PLANILHA = config("NOME_PLANILHA")
# CAMINHO_CREDENCIAL = Path("C:\\Users\\warfa\\OneDrive\\Documentos\\Italo\\Git\\VerificadorDePrecosGPU\\config\\credentials\\verificadorprecosgpu-c2b74b75b0f0.json")
CAMINHO_CREDENCIAL = Path(Path.cwd() / "config" / "credentials" / "verificadorprecosgpu-c2b74b75b0f0.json")