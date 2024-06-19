# -*- coding: utf-8 -*-
"""
Luna Juan Marcelo
DNI 24234578
@author: elpocitano@gmail.com
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from datetime import datetime
from gestor_jugadores import GestorJugadores
from jugador import Jugador, Dificultad


class SimonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simon Dice")
        self.sequence = []
        self.user_sequence = []
        self.buttons = []
        self.colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
        self.score = 0
        self.nivel = Dificultad.PRINCIPIANTE
        self.delay = 1300

        self.gestor = GestorJugadores()
        self.gestor.cargar_puntajes()
        self.player_name = self.ask_player_name()
        self.create_menu()
        self.create_widgets()
        self.create_player_info()
        self.start_game()

    def ask_player_name(self):
        return simpledialog.askstring("Nombre del jugador", "Ingrese su nombre:")

    def create_menu(self):
        # Crea una barra de menú principal
        menubar = tk.Menu(self.root)

        # Configura la ventana principal para usar esta barra de menú
        self.root.config(menu=menubar)

        # Crea un menú desplegable llamado "Opciones"
        options_menu = tk.Menu(menubar, tearoff=0)

        # Añade el menú desplegable "Opciones" a la barra de menú principal
        menubar.add_cascade(label="Opciones", menu=options_menu)

        # Añade una opción "Puntajes" al menú "Opciones" que llama al método show_scores cuando se selecciona
        options_menu.add_command(label="Puntajes", command=self.show_scores)

        # Añade una opción "Salir" al menú "Opciones" que cierra la aplicación cuando se selecciona
        options_menu.add_command(label="Salir", command=self.root.quit)

        # Añade una opción "Cambiar Nivel" al menú "Opciones" que llama al método select_level cuando se selecciona
        options_menu.add_command(label="Cambiar Nivel", command=self.select_level)

    def select_level(self):
        # Muestra un cuadro de diálogo para solicitar el nivel del juego al usuario
        level = simpledialog.askstring("Nivel", "Ingrese el nivel (Principiante, Experto, Super Experto):")

        # Verifica si el usuario ingresó un nivel
        if level:
            # Convierte el nivel ingresado a mayúsculas y reemplaza espacios con guiones bajos
            # Asigna el nivel correspondiente de la enumeración Dificultad
            self.nivel = Dificultad[level.upper().replace(" ", "_")]

            # Configura el retraso en función del nivel seleccionado
            if self.nivel == Dificultad.EXPERTO:
                self.delay = 900
            elif self.nivel == Dificultad.SUPER_EXPERTO:
                self.delay = 700
            else:
                self.delay = 1300

    def create_widgets(self):
        # Itera sobre la lista de colores con sus índices
        for i, color in enumerate(self.colors):
            # Crea un widget Canvas para cada botón con las propiedades especificadas
            button = tk.Canvas(self.root, width=100, height=100, bg=color, relief="raised")
            # Ubica el botón en la cuadrícula usando cálculos de fila y columna
            button.grid(row=i // 2 + 3, column=i % 2, padx=10, pady=10)
            # Vincula un evento de clic izquierdo al botón y asigna el manejador de eventos
            button.bind("<Button-1>", lambda e, i=i: self.on_button_click(i))
            # Añade el botón a la lista de botones
            self.buttons.append(button)

    def create_player_info(self):
        self.player_info_label = tk.Label(self.root, text=f"Jugador: {self.player_name}")
        self.player_info_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.score_info_label = tk.Label(self.root, text=f"Puntaje: {self.score}")
        self.score_info_label.grid(row=0, column=1, sticky="e", padx=10, pady=10)

    def start_game(self):
        self.sequence = []
        self.user_sequence = []
        self.score = 0
        self.update_player_info()
        self.root.after(1000, self.next_round)

    def next_round(self):
        self.user_sequence = []
        next_color = random.choice(self.buttons)
        self.sequence.append(next_color)
        self.play_sequence()

    def play_sequence(self):
        # Iterar sobre la secuencia de botones
        for i, button in enumerate(self.sequence):
            # Programar el resaltado de cada botón después de un cierto retraso
            self.root.after(i * self.delay, lambda b=button: self.highlight_button(b))

        # Calcular el retraso total necesario para mostrar toda la secuencia
        total_delay = len(self.sequence) * self.delay

        # Programar el inicio del temporizador después de mostrar toda la secuencia
        self.root.after(total_delay, self.start_timer)

    def highlight_button(self, button):
        original_color = button.cget("bg")
        button.config(bg="white", relief="groove")  # Cambia el color de fondo y el relieve
        self.root.after(500, lambda: button.config(bg=original_color,
                                                   relief="raised"))  # Restaura el color original y el relieve

    def on_button_click(self, index):
        self.user_sequence.append(self.buttons[index])
        self.highlight_button(self.buttons[index])
        if self.user_sequence == self.sequence[:len(self.user_sequence)]:
            if len(self.user_sequence) == len(self.sequence):
                self.score += 1
                self.update_player_info()
                self.root.after(1000, self.next_round)
        else:
            self.game_over()

    def game_over(self):
        messagebox.showinfo("GAME OVER", f"Juego terminado. Puntaje: {self.score}")
        self.save_score()
        self.start_game()

    def save_score(self):
        score_data = {
            "player": self.player_name,
            "score": self.score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": self.nivel.value,
        }
        self.gestor.agregar_jugador(Jugador(
            self.player_name,
            self.score,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.nivel
        ))
        self.gestor.guardar_puntajes()

    def update_player_info(self):
        self.player_info_label.config(text=f"Jugador: {self.player_name}")
        self.score_info_label.config(text=f"Puntaje: {self.score}")

    def show_scores(self):
        scores_window = tk.Toplevel(self.root)
        scores_window.title("Galería de puntajes")
        tk.Label(scores_window, text="Jugador", borderwidth=2, relief="ridge", width=20).grid(row=0, column=0)
        tk.Label(scores_window, text="Fecha", borderwidth=2, relief="ridge", width=20).grid(row=0, column=1)
        tk.Label(scores_window, text="Puntaje", borderwidth=2, relief="ridge", width=20).grid(row=0, column=2)
        tk.Label(scores_window, text="Nivel", borderwidth=2, relief="ridge", width=20).grid(row=0, column=3)
        for i, jugador in enumerate(self.gestor.jugadores):
            tk.Label(scores_window, text=jugador.nombre, borderwidth=2, relief="ridge", width=20).grid(row=i + 1,
                                                                                                       column=0)
            tk.Label(scores_window, text=jugador.fecha, borderwidth=2, relief="ridge", width=20).grid(row=i + 1,
                                                                                                      column=1)
            tk.Label(scores_window, text=jugador.puntaje, borderwidth=2, relief="ridge", width=20).grid(row=i + 1,
                                                                                                        column=2)
            tk.Label(scores_window, text=jugador.nivel, borderwidth=2, relief="ridge", width=20).grid(row=i + 1,
                                                                                                      column=3)
