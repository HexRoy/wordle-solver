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
        self.yellow = ""
        self.not_in_word = ""
        self.in_word = ""


        # Transforms the words into a list
        for line in self.words:
            self.all_words = line.split(" ")

    def enter_greens(self):
        # Narrowing the word bank using the known positions of letters
        if self.letter1.text != " " and self.letter1.text != "":
            temp = list(self.green)
            temp[0] = self.letter1.text
            self.green = ("".join(temp)).upper()
            print(self.green)
            self.update_word_bank_green()
        if self.letter2.text != " " and self.letter2.text != "":
            temp = list(self.green)
            temp[1] = self.letter2.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter3.text != " " and self.letter3.text != "":
            temp = list(self.green)
            temp[2] = self.letter3.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter4.text != " " and self.letter4.text != "":
            temp = list(self.green)
            temp[3] = self.letter4.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()
        if self.letter5.text != " " and self.letter5.text != "":
            temp = list(self.green)
            temp[4] = self.letter5.text
            self.green = ("".join(temp)).upper()
            self.update_word_bank_green()

        print('Current word', self.green)

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
        print(self.all_words)

    def enter_yellows(self):
        # Narrowing the word bank using where you know letters are not
        if self.yellow != "?????":
            word_index = 0
            for i in range(len(self.all_words)):
                known_letter_pos = 0
                for letter in self.yellow:
                    if letter != "?":
                        if letter == list(self.all_words[word_index])[known_letter_pos]:
                            self.all_words.pop(word_index)
                            word_index -= 1
                            break
                    known_letter_pos += 1
                word_index += 1

    def enter_greys(self):
        # Narrowing the word bank using letters not in the word
        if self.all_not_in_word != self.not_in_word:
            word_index = 0
            difference = list(set(self.all_not_in_word) - set(self.not_in_word))
            for i in range(len(self.all_words)):
                for letter in self.not_in_word:
                    if letter in list(self.all_words[word_index]):
                        self.all_words.pop(word_index)
                        word_index -= 1
                        break
                word_index += 1

    def using_known_letters(self):
        # Narrowing the word bank using letters in the word
        if self.all_in_word != self.in_word:
            word_index = 0
            difference = list(set(all_in_word) - set(in_word))
            for i in range(len(all_words)):
                for letter in in_word:
                    if letter not in list(all_words[word_index]):
                        all_words.pop(word_index)
                        word_index -= 1
                        break
                word_index += 1

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
        print(sorted_choices[1], sorted_choices[2], sorted_choices[3])

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