# Wordle Solver
#   Geoffroy Penny
import operator
import numpy

# Uses a massive list of 5 letter words as the word bank from file
words = open("word_list")
all_words = ""

# Transforms the words into a list
for line in words:
    all_words = line.split(" ")
all_not_in_word = set()
all_in_word = set()


# Uses known information to select next guess
while True:
    # known: Letters you know the position of
    # known_not: Letters you know are in the word but unsure of position
    # not_in_word: Letters that you know are not in the word
    # in_word: Letters you know are in the word
    known = input("LETTERS ARE - use ? for unknown letters").upper()
    known_not = input("LETTER IN WRONG SPOT - use ? for others").upper()
    not_in_word = set(list(input("enter letters not in word").upper()))
    in_word = list(input("enter letters in word").upper())

    # Narrowing the word bank using the known positions of letters
    if known != "?????":
        word_index = 0
        for i in range(len(all_words)):
            known_letter_pos = 0
            for letter in known:
                if letter != "?":
                    if letter != list(all_words[word_index])[known_letter_pos]:
                        all_words.pop(word_index)
                        word_index -= 1
                        break
                known_letter_pos += 1
            word_index += 1

    # Narrowing the word bank using where you know letters are not
    if known_not != "?????":
        word_index = 0
        for i in range(len(all_words)):
            known_letter_pos = 0
            for letter in known_not:
                if letter != "?":
                    if letter == list(all_words[word_index])[known_letter_pos]:
                        all_words.pop(word_index)
                        word_index -= 1
                        break
                known_letter_pos += 1
            word_index += 1

    # Narrowing the word bank using letters in the word
    if all_in_word != in_word:
        word_index = 0
        difference = list(set(all_in_word) - set(in_word))
        for i in range(len(all_words)):
            for letter in in_word:
                if letter not in list(all_words[word_index]):
                    all_words.pop(word_index)
                    word_index -= 1
                    break
            word_index += 1

    # Narrowing the word bank using letters not in the word
    if all_not_in_word != not_in_word:
        word_index = 0
        difference = list(set(all_not_in_word) - set(not_in_word))
        for i in range(len(all_words)):
            for letter in not_in_word:
                if letter in list(all_words[word_index]):
                    all_words.pop(word_index)
                    word_index -= 1
                    break
            word_index += 1

    # Creating a set of letters in, and not in the word
    all_in_word = set.union(all_in_word, in_word)
    all_not_in_word = set.union(all_not_in_word, not_in_word)

    # Using most common positional scoring to select best word guess
    # First calculate the scores for each letter in each position base on how common it is
    letter_scoring = numpy.zeros((5, 26), dtype=int)
    letter_to_position = {'A': 0,
                          'B': 1,
                          'C': 2,
                          'D': 3,
                          'E': 4,
                          'F': 5,
                          'G': 6,
                          'H': 7,
                          'I': 8,
                          'J': 9,
                          'K': 10,
                          'L': 11,
                          'M': 12,
                          'N': 13,
                          'O': 14,
                          'P': 15,
                          'Q': 16,
                          'R': 17,
                          'S': 18,
                          'T': 19,
                          'U': 20,
                          'V': 21,
                          'W': 22,
                          'X': 23,
                          'Y': 24,
                          'Z': 25,
                          }
    for word in all_words:
        i = 0
        for letter in word:
            letter_scoring[i][letter_to_position[letter]] += 1
            i += 1

    # Second find word scores using previously calculated values
    best_choice = {}
    for word in all_words:
        total = 0
        i = 0
        for letter in word:
            total += letter_scoring[i][letter_to_position[letter]]
            i += 1
        best_choice[word] = total
    sorted_choices = sorted(best_choice.items(), key=operator.itemgetter(1), reverse=True)

    # For the user
    # print("letter scoring \n", letter_scoring)
    print(sorted_choices)
    print("confirmed letters", known)
    print("letters in word, wrong spot", known_not)
    print("letters not in word", all_not_in_word)
    print("letters in word", all_in_word)
    print("best guess", sorted_choices[0][0])