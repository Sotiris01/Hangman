
__author__ = 'Sotiris Mpalatsias'
__copyright__ = 'Copyright (C) 2021, Hangman Game'
__version__ = '1.0.1'
__date__ = '2021/03/02'
__maintainer__ = 'Sotiris Mpalatsias'
__email__ = 'sotiris.mp@gmail.com'
__description__ = 'A simple Hangman Game Player VS Player/Computer'

# Begin Code

import random
import os

dictionary_file = "words.txt"

TOTAL_TRIAS = 5

HANGMAN_PICS = ['''
    +------+
    |
    |
    |
  ===== ''', '''
    +------+
    |      o
    |
    |
  =====  ''', '''
    +------+
    |      o
    |     /|
    |
  ===== ''', '''
    +------+
    |      o
    |     /|\\
    |
  ===== ''', '''
    +------+
    |      o
    |     /|\\
    |     /
  =====  ''', '''
    +------+
    |      o
    |     /|\\
    |     / \\
  ===== ''']


def main():
    while True:
        clear()
        print("~~~ Welcome to Hangman ~~~")

        missed_letters = []
        correct_letters = []
        secret_word = get_secret_word()

        while True:
            displayBoard(missed_letters, correct_letters, secret_word)
            guess = make_guess(missed_letters, correct_letters)
            if len(guess) > 1:
                if guess == secret_word:
                    WinGame()
                else:
                    GameOver(secret_word)
                break
            else:
                if guess in secret_word:
                    correct_letters.append(guess)
                else:
                    missed_letters.append(guess)
            if len(missed_letters) == TOTAL_TRIAS:
                displayBoard(missed_letters, correct_letters, secret_word)
                GameOver(secret_word)
                break
            if all(letter in correct_letters for letter in list(secret_word)):
                WinGame()
                break

        answer = input("Do you want to play again? <yes>/<no> ")
        if answer.upper()[0] == 'Y':
            continue
        else:
            break


def WinGame():
    print()
    print("You Win")
    print()


def GameOver(secret_word):
    print()
    print("Game Over")
    print("Secret Word is: ", secret_word.upper())
    print()


def make_guess(missed_letters, correct_letters):
    while True:
        guess = input("Make a guess: ").lower()
        if guess.isalpha():
            break
    while True:
        if guess in missed_letters + correct_letters:
            print("You have already guess the followint letters:")
            for letter in missed_letters + correct_letters:
                print(letter, end=', ')
            print()
            while True:
                guess = input("A new one please: ").lower()
                if guess.isalpha():
                    break
        else:
            return guess


def displayBoard(missed_letters, correct_letters, secret_word):
    clear()
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    for letter in secret_word:
        if letter in correct_letters:
            print(letter.upper(), end='')
        else:
            print('_', end='')
    print()

    print("Missed letter: ", end='')
    for letter in missed_letters:
        print(letter, end=', ')
    print()


def get_secret_word():
    while True:
        print()
        answer = ''.join(input("Give me a word or press <Enter>"
                                "to find you a random one: ").lower().split())
        if answer == '':
            return random_word()
        else:
            return new_word(answer)


def random_word():
    while True:
        clear()
        length = input("Specify the word length or press <Enter>"
                        "for a random one:")
        if length == '':
            length = random.randint(3, 20)
            break
        else:
            try:
                length = int(length)
            except ValueError:
                print("Invalid Input")
                continue
            else:
                if 3 <= length <= 20:
                    break
                else:
                    print("Word length must be between 3 and 20 characters")
    try:
        with open(dictionary_file, "r") as file:
            words = [line.strip() for line in file.readlines()]
            while True:
                secret_word = random.choice(words)
                if len(secret_word) == length:
                    break
    except FileNotFoundError:
        print("The Dictionary was not found")
        secret_word = input("Give me a Word: ")
    finally:
        return secret_word


def new_word(secret_word):
    try:
        with open(dictionary_file, "r+") as file:
            words = [line.strip() for line in file.readlines()]
            while True:
                if secret_word in words:
                    break
                else:
                    print("I could't find this word in my dictionary")
                    print("Do you want to add it as a new one? <yes>/<no>")
                    if input().upper()[0] == 'Y':
                        file.write(secret_word+'\n')
                        break
                    else:
                        secret_word = input("Give me another one: ")
                        continue
    except FileNotFoundError:
        pass
    finally:
        return secret_word


def clear():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")


if __name__ == '__main__':
    main()
