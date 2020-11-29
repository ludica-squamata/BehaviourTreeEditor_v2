from pygame import quit
from sys import exit
import json


def salir():
    quit()
    exit()


def abrir_json(ruta):
    with open(ruta, 'rt', encoding='latin_1') as file:
        return json.load(file)


def guardar_json(ruta, data):
    with open(ruta, 'wt', encoding='latin_1') as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': '))
