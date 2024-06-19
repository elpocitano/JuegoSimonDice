# -*- coding: utf-8 -*-
"""
Luna Juan Marcelo
DNI 24234578
@author: elpocitano@gmail.com
"""
from enum import Enum


class Dificultad(Enum):
    PRINCIPIANTE = "Principiante"
    EXPERTO = "Experto"
    SUPER_EXPERTO = "Super Experto"


class Jugador:
    def __init__(self, nombre, puntaje, fecha, nivel):
        self.nombre = nombre
        self.puntaje = puntaje
        self.fecha = fecha
        self.nivel = nivel

    def __gt__(self, other):
        return self.puntaje > other.puntaje
