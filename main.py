from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from casilla import Casilla


class MonorsV2App(App):

    def build(self):

        Window.size = (1200, 900)
        self.title = "MONORS Marbella v2"

        root = FloatLayout()

        salida = Casilla(
            nombre="SALIDA",
            precio=200,
            imagen="casillas/salida.png",
            size_hint=(0.18, 0.18),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        root.add_widget(salida)

        return root


if __name__ == "__main__":
    MonorsV2App().run()
