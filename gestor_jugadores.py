# -*- coding: utf-8 -*-
"""
Luna Juan Marcelo
DNI 24234578
@author: elpocitano@gmail.com
"""
import json
from jugador import Jugador


class GestorJugadores:
    def __init__(self):
        self.jugadores = []

    def cargar_puntajes(self):
        try:
            with open("pysimonpuntajes.json", "r") as file:
                scores = json.load(file)
                for score in scores:
                    jugador = Jugador(
                        score["player"], score["score"], score["date"], score["level"]
                    )
                    self.jugadores.append(jugador)
        except FileNotFoundError:
            pass

    def guardar_puntajes(self):
        scores = [
            {
                "player": jugador.nombre,
                "score": jugador.puntaje,
                "date": jugador.fecha,
                "level": jugador.nivel.value,
            }
            for jugador in self.jugadores
        ]

        with open("pysimonpuntajes.json", "w") as file:
            json.dump(scores, file, indent=4)

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)
        self.jugadores.sort(reverse=True)
