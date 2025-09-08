import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from functools import partial
from kivy.app import App
    
class ColorPalette:
    def __init__(self):
        self.colors = {
            'bg': (0.09, 0.17, 0.28, 1),        #fondo de pantalla
            'header': (0.08, 0.29, 0.49, 1),    #encabezado
            'text': (1, 1, 1, 1),               #color del texto
            'primary': (0.12, 0.45, 0.84, 1),   #color principal
            'primary_dark': (0.09, 0.35, 0.68, 1), 
            'card': (0.11, 0.33, 0.58, 1),      #cartas
            'choice_bg': (0.12, 0.45, 0.84, 0.9),
            'choice_bg_pressed': (0.09, 0.35, 0.68, 1),
        }

class MenuPrincipal(MDScreen): pass

class Ejercicios(MDScreen): pass

class Sumadificultad(MDScreen): pass

class Restadificultad(MDScreen): pass

class Multiplicaciondificultad(MDScreen): pass

class Ecuacionbasicadificultad(MDScreen): pass

class Divisiondificultad(MDScreen): pass
    
class Ecuaciones(MDScreen): pass

class Desafiodificultad(MDScreen): pass

class Timer(Label):
    def __init__(self, duration, on_timeout, progress_bar=None, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.remaining = duration
        self.on_timeout = on_timeout
        self.progress_bar = progress_bar
        self.event = None
        self.update_text()
        self.update_bar()

    def start(self):
        self.stop()  # Deterno por si acaso 
        self.remaining = self.duration
        self.event = Clock.schedule_interval(self._tick, 1)
        self.update_text()
    
    def update_bar(self):
        if self.progress_bar:
            porcentaje = (self.remaining / self.duration) * 100
            self.progress_bar.value = porcentaje

            # Cambiar color según tiempo restante (opcional)
            if porcentaje > 60:
                self.progress_bar.color = [0, 1, 0, 1]  # verde
            elif porcentaje > 30:
                self.progress_bar.color = [1, 1, 0, 1]  # amarillo
            else:
                self.progress_bar.color = [1, 0, 0, 1]  # rojo

    def _tick(self, dt):
        self.remaining -= 1
        self.update_text()
        self.update_bar()
        if self.remaining <= 0:
            self.stop()
            if self.on_timeout:
                self.on_timeout()

    def stop(self):
        if self.event:
            self.event.cancel()
            self.event = None

    def update_text(self):
        self.text = f"{self.remaining} s"
        if self.remaining > 6:
            self.color = (0, 1, 0, 1)  # color cerde
        elif self.remaining > 3:
            self.color = (1, 1, 0, 1) # color amarillo
        else:
            self.color = (1, 0, 0, 1)  # color negro
            
class Suma(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 10  # segundos
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)

    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
        elif dificultad == "medio":
            rango = (10, 25)
        elif dificultad == "dificil":
            rango = (25, 100)
        else: 
            rango = (1, 10)
        
        print("generando ejercicio de suma") #comprobar en el cmd
        self.n1 = random.randint(*rango)
        self.n2 = random.randint(*rango)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.resultado.text = ""
        self.timer.start()
        self.timer.update_text()
        self.generar_opciones()
        self.generando = False
        
    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()

        correcta = self.n1 + self.n2
        opciones = [correcta]

        # Genera 3 distractores únicos
        while len(opciones) < 4:
            distractor = random.randint(correcta - 10, correcta + 10)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)

        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )
            
            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)

    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.n1 + self.n2

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]  # Verde
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado.text = "¡Correcto! :)"
                            self.ids.resultado.text_color = [0, 0.6, 0, 1]

                        else:
                            card.md_bg_color = [1, 0, 0, 1]    # Rojo
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado.text = f"Incorrecto :( la respuesta era = {correcta}"
                            self.ids.resultado.text_color = [1, 0, 0, 1]
                            
        Clock.unschedule(self.generar_numero)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 3)

    def tiempo_agotado(self):
        self.ids.resultado.text = "Tiempo agotado :o"
        self.ids.resultado.text_color = [1, 0.5, 0, 1]
        
        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Suma") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()

class Resta(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 10  # segundos
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)

    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
        elif dificultad == "medio":
            rango = (10, 25)
        elif dificultad == "dificil":
            rango = (25, 100)
        else: 
            rango = (1, 10)
        
        print("generando ejercicio de Resta")
        self.generando = False
        self.n1 = random.randint(*rango)
        self.n2 = random.randint(*rango)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.resultado.text = ""
        self.timer.start()
        self.timer.update_text()
        self.generando = False
        self.generar_opciones()

    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()

        correcta = self.n1 - self.n2
        opciones = [correcta]

        # Genera 3 distractores únicos
        while len(opciones) < 4:
            distractor = random.randint(correcta - 10, correcta + 10)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)

        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )
            
            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)

    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.n1 - self.n2

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]  # Verde
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado.text = "¡Correcto! :)"
                            self.ids.resultado.text_color = [0, 0.6, 0, 1]

                        else:
                            card.md_bg_color = [1, 0, 0, 1]    # Rojo
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado.text = f"Incorrecto :( la respuesta era = {correcta}"
                            self.ids.resultado.text_color = [1, 0, 0, 1]
                            
        Clock.unschedule(self.generar_numero)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)

    def tiempo_agotado(self):
        self.ids.resultado.text = "Tiempo agotado :o"
        self.ids.resultado.text_color = [1, 0.5, 0, 1]
        
        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Resta") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()

class Multiplicacion(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 10  # segundos
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)

    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
        elif dificultad == "medio":
            rango = (-5, 12)
        elif dificultad == "dificil":
            rango = (-10, 20)
        else: 
            rango = (1, 10)
        
        print("generando ejercicio de Multiplicación")
        self.generando = False
        self.n1 = random.randint(*rango)
        self.n2 = random.randint(*rango)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.resultado.text = ""
        self.timer.start()
        self.timer.update_text()
        self.generando = False
        self.generar_opciones()

    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()

        correcta = self.n1 * self.n2
        opciones = [correcta]

        # Genera 3 distractores únicos
        while len(opciones) < 4:
            distractor = random.randint(correcta - 10, correcta + 10)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)

        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )
            
            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)

    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.n1 * self.n2

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]  # Verde
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado.text = "¡Correcto! :)"
                            self.ids.resultado.text_color = [0, 0.6, 0, 1]

                        else:
                            card.md_bg_color = [1, 0, 0, 1]    # Rojo
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado.text = f"Incorrecto :( la respuesta era = {correcta}"
                            self.ids.resultado.text_color = [1, 0, 0, 1]

        Clock.unschedule(self.generar_numero)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)

    def tiempo_agotado(self):
        self.ids.resultado.text = "Tiempo agotado :o"
        self.ids.resultado.text_color = [1, 0.5, 0, 1]
        
        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Multiplicacion") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()

class Division(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 10  # segundos
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)

    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
        elif dificultad == "medio":
            rango = (9, 12)
        elif dificultad == "dificil":
            rango = (12, 20)
        else: 
            rango = (1, 10)
        
        print("generando ejercicio de division")
        self.generando = False
        self.divisor = random.randint(*rango) #Generamos un numero aleatorio del 1 al 10
        resultado = random.randint(*rango) #Resultado entero
        self.dividendo = self.divisor * resultado #Para asegurar una division exacta
        self.ids.dividendo.text = f"{self.dividendo}"
        self.ids.divisor.text = f"{self.divisor}"
        self.ids.resultado.text = ""
        self.timer.start()
        self.timer.update_text()
        self.generar_opciones()

    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()

        correcta = self.dividendo // self.divisor
        opciones = [correcta]

        # Genera 3 distractores únicos
        while len(opciones) < 4:
            distractor = random.randint(correcta - 10, correcta + 10)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)

        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )
            
            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)

    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.dividendo / self.divisor

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]  # Verde
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado.text = "¡Correcto! :)"
                            self.ids.resultado.text_color = [0, 0.6, 0, 1]

                        else:
                            card.md_bg_color = [1, 0, 0, 1]    # Rojo
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado.text = f"Incorrecto :( la respuesta era = {correcta}"
                            self.ids.resultado.text_color = [1, 0, 0, 1]

        Clock.unschedule(self.generar_numero)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)

    def tiempo_agotado(self):
        self.ids.resultado.text = "Tiempo agotado :o"
        self.ids.resultado.text_color = [1, 0.5, 0, 1]
        
        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Division") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()

class Ecuacionbasica(MDScreen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 12
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)
    
    def on_enter(self):
        self.generar_ejercicio()

    def generar_ejercicio(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
            rangoi = (-10, 5)
        elif dificultad == "medio":
            rango = (10, 15)
            rangoi = (-20, 10)
        elif dificultad == "dificil":
            rango = (15, 20)
            rangoi = (-30, 15)
        else: 
            rango = (1, 10)
        
        print("Generando ejercicio de ecuacion basica") #Comprobar en el CMD
        self.n1 = random.randint(*rango)
        self.n2 = random.randint(*rangoi)
        self.x_real = random.randint(0, 10)
        self.n3 = self.n1 * self.x_real + self.n2

        ecuacion_texto = f"{self.n1}x + {self.n2} = {self.n3}"
        self.ids.ecuacion_label.text = f"{ecuacion_texto}"
        self.ids.resultado_label.text = ""
        self.timer.start()
        self.timer.update_text()
        #self.generar_ejercicio()
        self.generar_opciones()
        self.generando = False

    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()

        correcta = self.x_real
        opciones = [correcta]

        while len(opciones) < 4:
            distractor = random.randint(correcta - 5, correcta + 5)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)

        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )

            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)

    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.x_real

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado_label.text = "¡Correcto!"
                            self.ids.resultado_label.text_color = [0, 0.6, 0, 1]
                        else:
                            card.md_bg_color = [1, 0, 0, 1]
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado_label.text = f"Incorrecto, x vale = {correcta}"
                            self.ids.resultado_label.text_color = [1, 0, 0, 1]

        #Generacion de nuevos ejercicios
        Clock.unschedule(self.generar_ejercicio)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_ejercicio(), 2)

    def tiempo_agotado(self):
        self.ids.resultado_label.text = "Tiempo agotado :o"
        self.ids.resultado_label.text_color = [1, 0.5, 0, 1]
        
        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_ejercicio(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Ecuacion Basica") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()
    
class Ecuacionsegundo(MDScreen): pass

class Desafio(MDScreen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generando = False
        self.tiempo_limite = 10  # segundos
        self.evento_generacion = None

    def on_kv_post(self, base_widget):
        self.timer = Timer(duration=self.tiempo_limite, on_timeout=self.tiempo_agotado, progress_bar=self.ids.barra_tiempo)
        self.ids.contador.add_widget(self.timer)

    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        if self.generando:
            return
        self.generando = True
        #se establece la dificultad del ejercicio
        dificultad = App.get_running_app().dificultad
        if dificultad == "facil":
            rango = (1, 10)
        elif dificultad == "medio":
            rango = (10, 15)
        elif dificultad == "dificil":
            rango = (15, 20)
        else: 
            rango = (1, 10)
        
        print("generando ejercicio de Desafio") #comprobar en el cmd
        self.n1 = random.randint(*rango)
        self.n2 = random.randint(*rango)
        self.x_real = random.randint(*rango)
        self.ids.resultado.text = ""
        self.timer.start()
        self.timer.update_text()
        self.generar_opciones()
        self.generando = False
    #Generar las distintas opciones
    def generar_opciones(self):
        self.ids.opciones_respuesta.clear_widgets()
        operacion = random.choice(['+', '-', '*', '/', 'ex']) #operacion aleatoria
        
        #determinamos el ejercicio
        if operacion == '+':
            print("generado Suma")
            correcta = self.n1 + self.n2
            ejercicio_str = f"{self.n1} + {self.n2}"
            
        elif operacion == '-':
            print("generado resta")
            correcta = self.n1 - self.n2
            ejercicio_str = f"{self.n1} - {self.n2}"
            
        elif operacion == '*':
            print("generado multiplicacion")
            correcta = self.n1 * self.n2
            ejercicio_str = f"{self.n1} x {self.n2}"
            
        elif operacion == '/':
            print("generado division")
            self.n1 = self.n1 * self.n2
            correcta = self.n1 // self.n2
            ejercicio_str = f"{self.n1} ÷ {self.n2}"
        
        elif operacion == 'ex':
            self.n3 = self.n1 * self.x_real + self.n2
            correcta = self.x_real
            ejercicio_str = f"{self.n1}x + {self.n2} = {self.n3}"
            
        self.ids.ejercicio.text = ejercicio_str
        self.resultado_correcto = correcta    
        opciones = [correcta]

        # Genera 3 distractores únicos
        while len(opciones) < 4:
            distractor = random.randint(correcta - 10, correcta + 10)
            if distractor != correcta and distractor not in opciones:
                opciones.append(distractor)

        random.shuffle(opciones)
        
        for valor in opciones:
            card = MDCard(
                size_hint=(1, None),
                height=dp(60),
                radius=[12],
                elevation=4,
                padding=dp(10),
                md_bg_color=App.get_running_app().colors["card"]
            )

            btn = MDRaisedButton(
                text=str(valor),
                size_hint=(1, 1),
                md_bg_color=App.get_running_app().colors["card"],
                text_color=App.get_running_app().colors["text"],
            )
            
            btn.on_release = partial(self.verificar_opcion, valor, card, btn)
            
            card.add_widget(btn)
            self.ids.opciones_respuesta.add_widget(card)
        
    def verificar_opcion(self, seleccion, *args):
        self.timer.stop()
        correcta = self.resultado_correcto

        for card in self.ids.opciones_respuesta.children:
            for widget in card.children:
                if isinstance(widget, MDRaisedButton):
                    if int(widget.text) == seleccion:
                        if seleccion == correcta:
                            card.md_bg_color = [0, 0.6, 0, 1]  # Verde
                            widget.md_bg_color = [0, 0.6, 0, 1]
                            self.ids.resultado.text = "¡Correcto! :)"
                            self.ids.resultado.text_color = [0, 0.6, 0, 1]

                        else:
                            card.md_bg_color = [1, 0, 0, 1]    # Rojo
                            widget.md_bg_color = [1, 0, 0, 1]
                            self.ids.resultado.text = f"Incorrecto :( la respuesta era = {correcta}"
                            self.ids.resultado.text_color = [1, 0, 0, 1]
                            
        Clock.unschedule(self.generar_numero)
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 3)

    def tiempo_agotado(self):
        self.ids.resultado.text = "Tiempo agotado :o"
        self.ids.resultado.text_color = [1, 0.5, 0, 1]
        
        # Desactivar botones
        for container in self.ids.opciones_respuesta.children:
            for widget in container.children:
                if isinstance(widget, MDRaisedButton):
                    widget.disabled = True

        #Cancelar eventos anteriores
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            
        self.evento_generacion = Clock.schedule_once(lambda dt: self.generar_numero(), 2)
    
    def on_leave(self):
        print("Saliendo de pantalla Suma") #verificar en el CMD
        if self.evento_generacion:
            Clock.unschedule(self.evento_generacion)
            self.evento_generacion = None

        if hasattr(self, 'timer'):
            self.timer.stop()
    
class GestorPantalla(ScreenManager): pass

class Sigma(MDApp):         
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.palette = ColorPalette()
        self.colors = self.palette.colors  # acceso directo
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"        # Color principal (botones, barra)
        self.theme_cls.primary_hue = "500"             # Intensidad del color
        self.theme_cls.theme_style = "Light"           # O "Dark"
        
        return Builder.load_file("interfaz.kv")
    
    dificultad = "facil"
    
    def set_dificultad(self, nivel):
        print(f"Dificultad seleccionada: {nivel}")
        self.dificultad = nivel

    def ir_ejercicios(self, *args):
        print("Botón presionado")
        self.root.current = "ejercicios"
    
    def ir_ecuaciones(self, *args):
        print("Botón presionado")
        self.root.current = "ecuaciones"

Sigma().run()
