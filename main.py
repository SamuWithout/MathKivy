import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock

Window.clearcolor = (1, 1, 1, 1) # fondo de color blanco

class MenuPrincipal(MDScreen): pass

class Ejercicios(MDScreen): pass

class Ecuaciones(MDScreen): pass

class Suma(MDScreen): 
    def generar_numero(self):
        self.n1 = random.randint(1, 20) #Generamos un numeor aleatorio del 1 al 20
        self.n2 = random.randint(1, 20)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.respuesta.text = "" #para limpiar la respuesta anterior
        self.ids.resultado.text = "" #Para limpiar el resultado anterior
    
    def calcular(self):
        try:
            respuesta = float(self.ids.respuesta.text) #Aca el usuario escribe la respuesta
            if respuesta == self.n1 + self.n2: # Se comprueba la validez de la respuesta
                self.ids.resultado.text = "Respuesta correcta"
                Clock.schedule_once(lambda dt: self.generar_numero(), 2) # Se vuelve a generar otro ejercicio
            else:
                self.ids.resultado.text = "Respuesta incorrecta, vuelve a intentar"
        except:
            self.ids.resultado.text = "Hubo un error en el proceso" #En caso de que se ingrese un valor no permitido

class Resta(MDScreen):
    def generar_numero(self):
        self.n1 = random.randint(1, 20) #Generamos un numeor aleatorio del 1 al 20
        self.n2 = random.randint(1, self.n1)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.respuesta.text = "" #para limpiar la respuesta anterior
        self.ids.resultado.text = "" #Para limpiar el resultado anterior
    
    def calcular(self):
        try:
            respuesta = float(self.ids.respuesta.text) #Aca el usuario escribe la respuesta
            if respuesta == self.n1 - self.n2: # Se comprueba la validez de la respuesta
                self.ids.resultado.text = "Respuesta correcta"
                Clock.schedule_once(lambda dt: self.generar_numero(), 2) # Se vuelve a generar otro ejercicio
            else:
                self.ids.resultado.text = "Respuesta incorrecta, vuelve a intentar"
        except:
            self.ids.resultado.text = "Hubo un error en el proceso" #En caso de que se ingrese un valor no permitido

class Multiplicacion(MDScreen):
    def generar_numero(self):
        self.n1 = random.randint(1, 10) #Generamos un numero aleatorio del 1 al 10
        self.n2 = random.randint(1, 10)
        self.ids.num1.text = f"{self.n1}"
        self.ids.num2.text = f"{self.n2}"
        self.ids.respuesta.text = "" #Se limpia la respuesta anterior
        self.ids.resultado.text = "" #Se limpia el resultado anterior
    def calcular(self):
        try:
            respuesta = float(self.ids.respuesta.text)
            if respuesta == self.n1 * self.n2: #Se comprueba la validez de la respuesta
                self.ids.resultado.text = "Respuesta correcta"
                Clock.schedule_once(lambda dt: self.generar_numero(), 2)
            else:
                self.ids.resultado.text = f"Respuesta incorrecta"
        except:
            self.ids.resultado.text = "Error al realizar el calculo" #En caso de que se ingrese un valor no permitido
   
class Division(MDScreen):
    def generar_numero(self):
        self.divisor = random.randint(1, 10) #Generamos un numero aleatorio del 1 al 10
        
        resultado = random.randint(1, 10) #Resultado entero
        
        self.dividendo = self.divisor * resultado #Para asegurar una division exacta
        
        self.ids.num1.text = f"{self.dividendo}"
        self.ids.num2.text = f"{self.divisor}"
        self.ids.respuesta.text = "" #para limpiar la respuesta anterior
        self.ids.resultado.text = "" #para limpiar el resultado anterior
        
    def calcular(self):
        try:
            respuesta = float(self.ids.respuesta.text)
            if respuesta == self.dividendo / self.divisor: #Se comprueba la validez de la respuesta
                self.ids.resultado.text = "Respuesta correcta"
                Clock.schedule_once(lambda dt: self.generar_numero(), 2)
            else:
                self.ids.resultado.text = f"Respuesta incorrecta, intentelo otra vez"
        except:
            self.ids.resultado.text = "Error al realizar el calculo"

class EcuacionBasica(MDScreen):
    def on_enter(self):
        self.generar_numero()

    def generar_numero(self):
        self.n1 = random.randint(1, 10)
        self.n2 = random.randint(-10, 10)
        self.x_real = random.randint(0, 10)
        self.n3 = self.n1 * self.x_real + self.n2

        ecuacion_texto = f"{self.n1}x + {self.n2} = {self.n3}"
        self.ids.ecuacion_label.text = f"Ecuación: {ecuacion_texto}"
        self.ids.resultado_label.text = ""

    def verificar_respuesta(self):
        if not hasattr(self, 'x_real'):
            self.ids.resultado_label.text = "La ecuación no fue generada aún"
            self.ids.resultado_label.text_color = [1, 0.5, 0, 1]
            return

        entrada = self.ids.respuesta_input.text
        try:
            x_usuario = int(entrada)
            if x_usuario == self.x_real:
                self.ids.resultado_label.text = "¡Correcto!"
                self.ids.resultado_label.text_color = [0, 0.6, 0, 1]
                Clock.schedule_once(lambda dt: self.generar_numero(), 2) # Se vuelve a generar otro ejercicio
            
            else:
                self.ids.resultado_label.text = f"Incorrecto. La respuesta era {self.x_real}"
                self.ids.resultado_label.text_color = [1, 0, 0, 1]
        except ValueError:
            self.ids.resultado_label.text = "Por favor ingresa un número válido"
            self.ids.resultado_label.text_color = [1, 0.5, 0, 1]
            
class GestorPantalla(ScreenManager): pass

class Sigma(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"        # Color principal (botones, barra)
        self.theme_cls.primary_hue = "500"             # Intensidad del color
        self.theme_cls.theme_style = "Light"           # O "Dark"
        
        return Builder.load_file("interfaz.kv")

Sigma().run()
