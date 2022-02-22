# Wordle Solver
#   Geoffroy Penny

# Uses a massive list of 5 letter words as the word bank from file
words = open("word_list")
all_words = ""

# Transforms the words into a list
for line in words:
    all_words = line.split(" ")
all_not_in_word = set()
all_in_word = set()

while True:
    # known: Letters you know the position of
    # known_not: Letters you know are in the word but unsure of position
    # not_in_word: Letters that you know are not in the word
    # in_word: Letters you know are in the word
    known = input("LETTERS ARE - use ? for unknown letters").upper()
    known_not = input("LETTER CANT BE - use ? for others").upper()
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

    # For the user
    print(all_words)
    print("confirmed letters", known)
    print("letters in word, wrong spot", known_not)
    print("letters not in word", all_not_in_word)
    print("letters in word", all_in_word)
