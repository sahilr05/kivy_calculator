import kivy
import math
import random
import re

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.button import (
    MDFlatButton,
    MDRaisedButton,
    MDRectangleFlatButton,
    MDTextButton,
)

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class MainApp(MDApp):
    def build(self):
        main_layout = MDBoxLayout(orientation="vertical")

        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", height=200, font_size=130
        )
        main_layout.add_widget(self.solution)
        buttons = [
            ["sin", "cos", "tan", "π"],
            ["log", "ln", "^", "fact."],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
            ["√", "(", ")", "="],
        ]

        for row in buttons:
            h_layout = MDBoxLayout()
            for label in row:
                button = MDRectangleFlatButton(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    font_size=20,
                    size_hint=(1, 1),
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
            elif current and button_text == "√":
                value = float(current) or float(self.solution.text)
                root_val = math.sqrt(value)
                self.solution.text = str(root_val)
                return
            elif button_text == "=":
                return self.on_solution(instance)
            else:
                new_text = current + button_text
                ops = ["log", "ln", "sin", "cos", "tan", "fact."]
                if button_text in ops:
                    new_text += "("
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            if "π" in text:
                text = text.replace("π", str(math.pi))
            if "^" in text:
                text = text.replace("^", "**")

            complex_op = "".join(re.split("[^a-zA-Z.]*", text))
            if complex_op:
                text = eval(text.replace(complex_op, ""))

                mapping = {
                    "log": math.log(text, 10),
                    "ln": math.log(text),
                    "sin": math.sin(text),
                    "cos": math.cos(text),
                    "tan": math.tan(text),
                    "fact.": math.factorial(text),
                }

                solution = str(mapping[complex_op])

            if not complex_op and not re.sub("[()*'/'-+]", "", text).isdigit():
                return

            if not complex_op:
                solution = str(eval(text))
            self.solution.text = solution


app = MainApp()
app.run()
