import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


DINERO_INICIAL = 1500
COBRO_SALIDA = 200
MONEDA = "€"


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.posicion = 0
        self.propiedades = []
        self.bancarrota = False


class Casilla:
    def __init__(self, nombre, tipo="normal", precio=0, alquiler=0):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.alquiler = alquiler
        self.duenio = None


class MonorsApp(App):

    def build(self):

        self.tablero = self.crear_tablero()

        self.jugadores = [
            Jugador("Jugador 1"),
            Jugador("Jugador 2")
        ]

        self.turno = 0

        self.root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.info = Label(
            text="MONORS - Monopoly Costa del Sol",
            font_size=22,
            size_hint=(1, 0.15)
        )

        self.root.add_widget(self.info)

        self.grid = GridLayout(
            cols=5,
            spacing=5,
            size_hint=(1, 0.55)
        )

        self.botones_casillas = []

        for casilla in self.tablero:

            boton = Button(
                text=casilla.nombre,
                font_size=12
            )

            self.botones_casillas.append(boton)
            self.grid.add_widget(boton)

        self.root.add_widget(self.grid)

        self.estado = Label(
            text="Pulsa 'Tirar dados' para comenzar.",
            font_size=16,
            size_hint=(1, 0.2)
        )

        self.root.add_widget(self.estado)

        controles = BoxLayout(
            size_hint=(1, 0.1),
            spacing=10
        )

        self.boton_tirar = Button(text="Tirar dados")
        self.boton_tirar.bind(on_press=self.tirar_turno)

        controles.add_widget(self.boton_tirar)

        self.root.add_widget(controles)

        self.actualizar_tablero()

        return self.root

    def crear_tablero(self):

        return [

            Casilla("SALIDA", "salida"),

            Casilla(
                "Málaga\nCalle Larios",
                "propiedad",
                60,
                10
            ),

            Casilla("Caja", "caja"),

            Casilla(
                "Málaga\nPaseo del Parque",
                "propiedad",
                60,
                20
            ),

            Casilla("Impuesto", "impuesto"),

            Casilla(
                "Tren Cercanías",
                "propiedad",
                200,
                25
            ),

            Casilla(
                "Marbella\nAv. Ricardo Soriano",
                "propiedad",
                100,
                30
            ),

            Casilla("Suerte", "suerte"),

            Casilla(
                "Marbella\nMilla de Oro",
                "propiedad",
                100,
                30
            ),

            Casilla(
                "Marbella\nPuerto Banús",
                "propiedad",
                120,
                40
            ),

            Casilla("Cárcel", "visita"),

            Casilla(
                "Ronda\nCalle La Bola",
                "propiedad",
                140,
                50
            ),

            Casilla(
                "Ronda\nPuente Nuevo",
                "propiedad",
                140,
                50
            ),

            Casilla(
                "Mijas\nAv. Virgen de la Peña",
                "propiedad",
                160,
                60
            ),

            Casilla("Parking", "parking"),

            Casilla(
                "Estepona\nPaseo Marítimo",
                "propiedad",
                180,
                70
            ),

            Casilla(
                "Fuengirola\nAv. Condes San Isidro",
                "propiedad",
                180,
                70
            ),

            Casilla(
                "San Pedro\nAv. Marqués del Duero",
                "propiedad",
                200,
                80
            ),

            Casilla(
                "Vélez-Málaga\nCamino de Málaga",
                "propiedad",
                220,
                90
            ),

            Casilla(
                "Manilva\nSabinillas",
                "propiedad",
                240,
                100
            ),
        ]

    def jugador_actual(self):

        return self.jugadores[
            self.turno % len(self.jugadores)
        ]

    def tirar_turno(self, instancia):

        jugador = self.jugador_actual()

        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)

        total = dado1 + dado2

        posicion_anterior = jugador.posicion

        jugador.posicion = (
            jugador.posicion + total
        ) % len(self.tablero)

        mensaje = (
            f"{jugador.nombre} tira "
            f"{dado1} + {dado2} = {total}\n"
        )

        if jugador.posicion < posicion_anterior:

            jugador.dinero += COBRO_SALIDA

            mensaje += (
                f"Pasa por SALIDA y cobra "
                f"{COBRO_SALIDA}{MONEDA}.\n"
            )

        casilla = self.tablero[jugador.posicion]

        mensaje += f"Cae en:\n{casilla.nombre}\n"

        mensaje += self.resolver_casilla(
            jugador,
            casilla
        )

        if jugador.dinero < 0:

            jugador.bancarrota = True

            mensaje += (
                f"\n{jugador.nombre} "
                f"entra en bancarrota.\n"
            )

        self.turno += 1

        self.actualizar_tablero()

        jugadores_activos = [
            j for j in self.jugadores
            if not j.bancarrota
        ]

        if len(jugadores_activos) == 1:

            mensaje += (
                f"\nGANADOR:\n"
                f"{jugadores_activos[0].nombre}"
            )

            self.boton_tirar.disabled = True

        else:

            siguiente = self.jugador_actual()

            mensaje += (
                f"\nSiguiente turno:\n"
                f"{siguiente.nombre}"
            )

        self.estado.text = mensaje

    def resolver_casilla(
        self,
        jugador,
        casilla
    ):

        if casilla.tipo == "propiedad":

            if casilla.duenio is None:

                if jugador.dinero >= casilla.precio:

                    jugador.dinero -= casilla.precio

                    casilla.duenio = jugador

                    jugador.propiedades.append(
                        casilla.nombre
                    )

                    return (
                        f"Compra la propiedad por "
                        f"{casilla.precio}{MONEDA}.\n"
                    )

                else:

                    return (
                        "No tiene dinero suficiente.\n"
                    )

            elif casilla.duenio != jugador:

                jugador.dinero -= casilla.alquiler

                casilla.duenio.dinero += (
                    casilla.alquiler
                )

                return (
                    f"Paga alquiler de "
                    f"{casilla.alquiler}{MONEDA} "
                    f"a {casilla.duenio.nombre}.\n"
                )

            else:

                return (
                    "La propiedad ya le pertenece.\n"
                )

        elif casilla.tipo == "impuesto":

            impuesto = 100

            jugador.dinero -= impuesto

            return (
                f"Paga impuesto de "
                f"{impuesto}{MONEDA}.\n"
            )

        elif casilla.tipo == "caja":

            premio = 100

            jugador.dinero += premio

            return (
                f"Caja de Comunidad:\n"
                f"Cobra {premio}{MONEDA}.\n"
            )

        elif casilla.tipo == "suerte":

            multa = 50

            jugador.dinero -= multa

            return (
                f"Suerte:\n"
                f"Paga {multa}{MONEDA}.\n"
            )

        elif casilla.tipo == "parking":

            return (
                "Parking gratuito.\n"
            )

        elif casilla.tipo == "visita":

            return (
                "Solo está de visita "
                "en la cárcel.\n"
            )

        return "Casilla de salida.\n"

    def actualizar_tablero(self):

        for i, boton in enumerate(
            self.botones_casillas
        ):

            casilla = self.tablero[i]

            jugadores_aqui = [

                jugador.nombre[-1]

                for jugador in self.jugadores

                if jugador.posicion == i
            ]

            texto = casilla.nombre

            if casilla.duenio:

                texto += (
                    f"\n[{casilla.duenio.nombre}]"
                )

            if jugadores_aqui:

                texto += (
                    f"\nP: "
                    f"{', '.join(jugadores_aqui)}"
                )

            boton.text = texto

        resumen = " | ".join(

            f"{j.nombre}: "
            f"{j.dinero}{MONEDA}"

            for j in self.jugadores
        )

        self.info.text = (
            f"MONORS - {resumen}"
        )


if __name__ == "__main__":
    MonorsApp().run()
