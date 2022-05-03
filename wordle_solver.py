# Wordle Solver
#   Geoffroy Penny

import operator
import numpy
from numpy import zeros
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.label import Label


from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.textinput import TextInput

# Todo
#  Bugs:
#   When entering 2 of the same letter green or yellow only filters by one

class CharInput(TextInput):
    def on_text(self, _, text):
        # if text == "\n":
        #     print(HomeGui.letter1.text)
        #     if HomeGui.letter1 == "a":
        #         print("yes")
        if not text:
            return
        if len(text) > 1:
            self.text = self.text[-1]
        next = self.get_focus_next()
        if next:
            self.focus = False
            next.focus = True




# # ==========================================================================================
# #       Home GUI:
# # ==========================================================================================
class HomeGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.letter_to_position = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
                                   'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
                                   'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
        self.words = open("word_list")
        self.all_words = ""
        self.all_not_in_word = set()
        self.all_in_word = set()
        self.green = "?????"
        self.not_in_word = ""
        self.in_word = ""


        # Transforms the words into a list
        for line in self.words:
            self.all_words = line.split(" ")

    def enter_greens(self):
        # Narrowing the word bank using the known positions of letters
        if self.letter1.text != " " and self.letter1.text != "" and self.letter1.text != "	":
            temp = list(self.green)
            temp[0] = self.letter1.text
            self.green = ("".join(temp)).upper()
            print(self.green)
            self.update_word_bank_green()
        if self.letter2.text != " " and self.letter2.text != "" and self.letter2.text != "	":
            temp = list(self.green)
            temp[1] = self.letter2.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter3.text != " " and self.letter3.text != "" and self.letter3.text != "	":
            temp = list(self.green)
            temp[2] = self.letter3.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter4.text != " " and self.letter4.text != "" and self.letter4.text != "	":
            temp = list(self.green)
            temp[3] = self.letter4.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter5.text != " " and self.letter5.text != "" and self.letter5.text != "	":
            temp = list(self.green)
            temp[4] = self.letter5.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()

        print(self.all_words)
        self.clear_text_input()


    def update_word_bank_green(self):
        word_index = 0
        for i in range(len(self.all_words)):
            known_letter_pos = 0
            for letter in self.green:
                if letter != "?":
                    if letter != list(self.all_words[word_index])[known_letter_pos]:
                        self.all_words.pop(word_index)
                        word_index -= 1
                        break
                known_letter_pos += 1
            word_index += 1


    def enter_yellows(self):
        yellow_input = ""
        if self.letter1.text != " " and self.letter1.text != "" and self.letter1.text != "	":
            yellow_input += self.letter1.text.upper()
        else:
            yellow_input += "?"
        if self.letter2.text != " " and self.letter2.text != "" and self.letter2.text != "	":
            yellow_input += self.letter2.text.upper()
        else:
            yellow_input += "?"
        if self.letter3.text != " " and self.letter3.text != "" and self.letter3.text != "	":
            yellow_input += self.letter3.text.upper()
        else:
            yellow_input += "?"
        if self.letter4.text != " " and self.letter4.text != "" and self.letter4.text != "	":
            yellow_input += self.letter4.text.upper()
        else:
            yellow_input += "?"
        if self.letter5.text != " " and self.letter5.text != "" and self.letter5.text != "	":
            yellow_input += self.letter5.text.upper()
        else:
            yellow_input += "?"

        # Remove every word with yellow in that position
        word_index = 0
        for i in range(len(self.all_words)):
            known_letter_pos = 0
            for letter in yellow_input:
                if letter != "?":
                    if letter == list(self.all_words[word_index])[known_letter_pos]:
                        self.all_words.pop(word_index)
                        word_index -= 1
                        break
                known_letter_pos += 1
            word_index += 1

        # Remove any word without the yellow not in the word. as long as spot not occupied by green
        word_index = 0
        for i in range(len(self.all_words)):
            for letter in yellow_input:
                if letter != "?":
                    if letter not in list(self.all_words[word_index]):
                        self.all_words.pop(word_index)
                        word_index -= 1
                        break
            word_index += 1

        print(self.all_words)
        self.clear_text_input()


    def enter_greys(self):
        # Narrowing the word bank using letters not in the word
        grey_input = ""
        if self.letter1.text != " " and self.letter1.text != "" and self.letter1.text != "	":
            grey_input += self.letter1.text.upper()
        if self.letter2.text != " " and self.letter2.text != "" and self.letter2.text != "	":
            grey_input += self.letter2.text.upper()
        if self.letter3.text != " " and self.letter3.text != "" and self.letter3.text != "	":
            grey_input += self.letter3.text.upper()
        if self.letter4.text != " " and self.letter4.text != "" and self.letter4.text != "	":
            grey_input += self.letter4.text.upper()
        if self.letter5.text != " " and self.letter5.text != "" and self.letter5.text != "	":
            grey_input += self.letter5.text.upper()

        word_index = 0
        for i in range(len(self.all_words)):
            if grey_input != "":
                for letter in grey_input:
                    if letter in list(self.all_words[word_index]):
                        self.all_words.pop(word_index)
                        word_index -= 1
                        break
                word_index += 1

        print(self.all_words)
        self.clear_text_input()

    def find_choice(self):
        # Creating a set of letters in, and not in the word
        self.all_in_word = set.union(self.all_in_word, self.in_word)
        self.all_not_in_word = set.union(self.all_not_in_word, self.not_in_word)
        letter_scoring = numpy.zeros((5, 26), dtype=int)

        for word in self.all_words:
            i = 0
            for letter in word:
                letter_scoring[i][self.letter_to_position[letter]] += 1
                i += 1

        # Second find word scores using previously calculated values
        best_choice = {}
        for word in self.all_words:
            total = 0
            i = 0
            for letter in word:
                total += letter_scoring[i][self.letter_to_position[letter]]
                i += 1
            best_choice[word] = total
        sorted_choices = sorted(best_choice.items(), key=operator.itemgetter(1), reverse=True)
        if len(sorted_choices) == 1:
            self.choice1.text = str(sorted_choices[0])
        elif len(sorted_choices) == 2:
            self.choice1.text = str(sorted_choices[0])
            self.choice2.text = str(sorted_choices[1])
        else:
            self.choice1.text = str(sorted_choices[0])
            self.choice2.text = str(sorted_choices[1])
            self.choice3.text = str(sorted_choices[2])

    def clear_text_input(self):
        self.letter1.text = ""
        self.letter2.text = ""
        self.letter3.text = ""
        self.letter4.text = ""
        self.letter5.text = ""

    def new_game(self):
        self.words = open("word_list")
        self.all_words = ""
        self.all_not_in_word = set()
        self.all_in_word = set()
        self.green = "?????"
        self.not_in_word = ""
        self.in_word = ""
        self.choice1.text = ""
        self.choice2.text = ""
        self.choice3.text = ""

        # Transforms the words into a list
        for line in self.words:
            self.all_words = line.split(" ")
        print(self.all_words)
# ==========================================================================================
#       Gui Manager:
# ==========================================================================================
class GuiManager(ScreenManager):
    pass


# ==========================================================================================
# Driver Code
# ==========================================================================================
kv = Builder.load_file("wordle_solver.kv")


class RandomClassApp(App):
    def build(self):
        return kv
#
#
if __name__ == "__main__":
    RandomClassApp().run()