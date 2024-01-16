from instagrapi import Client
from os import path
from pathlib import Path

INSTAGRAM = Client()
DIRECTORIO = path.dirname(__file__)

print("[API]: Iniciando sesión en Instagram")
usuario = input("Usuario: ")
password = input("Contraseña: ")

try:
    INSTAGRAM.login(usuario, password)
except:
    print("[ERROR]: No se pudo logear a la cuenta")
else:
    INSTAGRAM.dump_settings(Path(path.join(DIRECTORIO, "session.json")))
    print(f"[API]: Sesión guardada en {path.join(DIRECTORIO, 'session.json')}")

