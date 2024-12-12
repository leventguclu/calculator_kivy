from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import ListProperty

KV = '''
<NeumorphicButton@Button>:
    background_color: 0,0,0,0
    background_normal: ''
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1  # Light gray base color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15]
        Color:
            rgba: 1, 1, 1, 0.8  # Light shadow
        RoundedRectangle:
            pos: [self.pos[0]-3, self.pos[1]-3]
            size: self.size
            radius: [15]
        Color:
            rgba: 0.8, 0.8, 0.8, 0.8  # Dark shadow
        RoundedRectangle:
            pos: [self.pos[0]+3, self.pos[1]+3]
            size: self.size
            radius: [15]
    color: 0.3, 0.3, 0.3, 1  # Text color
    font_size: '20sp'
    on_press: self.background_color = (0.8, 0.8, 0.8, 0.1)
    on_release: self.background_color = (0, 0, 0, 0)

<Calculator>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
    BoxLayout:
        size_hint_y: 0.2
        TextInput:
            id: display
            font_size: '30sp'
            halign: 'right'
            background_color: 0.95, 0.95, 0.95, 1
            foreground_color: 0.3, 0.3, 0.3, 1
            readonly: True
            
    GridLayout:
        cols: 4
        spacing: 10
        
        NeumorphicButton:
            text: 'C'
            on_press: root.clear()
            
        NeumorphicButton:
            text: '+/-'
            on_press: root.negate()
            
        NeumorphicButton:
            text: '%'
            on_press: root.percentage()
            
        NeumorphicButton:
            text: '÷'
            on_press: root.operation('/')
            
        NeumorphicButton:
            text: '7'
            on_press: root.number('7')
            
        NeumorphicButton:
            text: '8'
            on_press: root.number('8')
            
        NeumorphicButton:
            text: '9'
            on_press: root.number('9')
            
        NeumorphicButton:
            text: '×'
            on_press: root.operation('*')
            
        NeumorphicButton:
            text: '4'
            on_press: root.number('4')
            
        NeumorphicButton:
            text: '5'
            on_press: root.number('5')
            
        NeumorphicButton:
            text: '6'
            on_press: root.number('6')
            
        NeumorphicButton:
            text: '-'
            on_press: root.operation('-')
            
        NeumorphicButton:
            text: '1'
            on_press: root.number('1')
            
        NeumorphicButton:
            text: '2'
            on_press: root.number('2')
            
        NeumorphicButton:
            text: '3'
            on_press: root.number('3')
            
        NeumorphicButton:
            text: '+'
            on_press: root.operation('+')
            
        NeumorphicButton:
            text: '0'
            on_press: root.number('0')
            
        NeumorphicButton:
            text: '.'
            on_press: root.decimal()
            
        NeumorphicButton:
            text: 'DEL'
            on_press: root.delete()
            
        NeumorphicButton:
            text: '='
            on_press: root.equals()
'''

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = []
        self.operation = None
        self.previous = None

    def number(self, num):
        current = self.ids.display.text
        if current == '0' or current == 'Error':
            self.ids.display.text = num
        else:
            self.ids.display.text = current + num

    def operation(self, op):
        if self.ids.display.text == 'Error':
            return
        try:
            if self.previous is not None and self.operation:
                self.equals()
            self.previous = float(self.ids.display.text)
            self.operation = op
            self.ids.display.text = '0'
        except ValueError:
            self.ids.display.text = 'Error'

    def clear(self):
        self.ids.display.text = '0'
        self.previous = None
        self.operation = None

    def equals(self):
        if not self.operation or self.previous is None:
            return
        try:
            current = float(self.ids.display.text)
            if self.operation == '+':
                result = self.previous + current
            elif self.operation == '-':
                result = self.previous - current
            elif self.operation == '*':
                result = self.previous * current
            elif self.operation == '/':
                if current == 0:
                    raise ZeroDivisionError
                result = self.previous / current
            
            # Sonucu tam sayı ise, ondalık gösterme
            if result.is_integer():
                result = int(result)
            self.ids.display.text = str(result)
            self.previous = None
            self.operation = None
        except (ValueError, ZeroDivisionError):
            self.ids.display.text = 'Error'

    def decimal(self):
        if '.' not in self.ids.display.text:
            self.ids.display.text += '.'

    def negate(self):
        try:
            current = float(self.ids.display.text)
            self.ids.display.text = str(-current)
        except ValueError:
            self.ids.display.text = 'Error'

    def percentage(self):
        try:
            current = float(self.ids.display.text)
            self.ids.display.text = str(current / 100)
        except ValueError:
            self.ids.display.text = 'Error'

    def delete(self):
        current = self.ids.display.text
        if len(current) > 1:
            self.ids.display.text = current[:-1]
        else:
            self.ids.display.text = '0'

class CalculatorApp(App):
    def build(self):
        Window.size = (400, 600)
        Builder.load_string(KV)
        return Calculator()

if __name__ == '__main__':
    CalculatorApp().run()