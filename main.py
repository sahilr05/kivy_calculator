import kivy
import random

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, MDTextButton

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class MainApp(MDApp):
    def build(self):
        main_layout = MDBoxLayout(orientation='vertical')

        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        self.solution = MDTextFieldRect(multiline=False, readonly=True, halign="right", height='40dp')
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
            ["sqr", "(", ")", "="],
        ]

        for row in buttons:
            h_layout = MDBoxLayout(padding=5)
            for label in row:
                button = Button(
                    text=label, pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color=[1,2,4,1]
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            elif current and button_text == "sqr":
                import math
                root_val = math.sqrt(int(current))
                self.solution.text = str(root_val)
                return
            elif button_text == "=":
                return self.on_solution(instance)
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution


app = MainApp()
app.run()
