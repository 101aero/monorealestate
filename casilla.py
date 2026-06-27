from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Casilla(FloatLayout):

    def __init__(self, nombre, precio, imagen="", **kwargs):
        super().__init__(**kwargs)

        # Imagen de fondo
        self.fondo = Image(
            source=imagen,
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.fondo)

        # Nombre
        self.lbl_nombre = Label(
            text=nombre,
            font_size=16,
            bold=True,
            color=(1,1,1,1),
            pos_hint={"center_x":0.5,"top":1},
            size_hint=(1,0.35)
        )

        self.add_widget(self.lbl_nombre)

        # Precio
        self.lbl_precio = Label(
            text=f"{precio} €",
            font_size=15,
            color=(1,1,0,1),
            pos_hint={"center_x":0.5,"y":0},
            size_hint=(1,0.25)
        )

        self.add_widget(self.lbl_precio)
