#!/usr/bin/python3

# A wonderful game of guessing insecure passwords #


import random

# The Passwords come from here:
#https://github.com/danielmiessler/SecLists/blob/master/Passwords/10_million_password_list_top_100.txt

# The file to read passwords from
password_file = "passwords.txt"

# Open the file in read mode
open_file = open(password_file, "r")

# Read entire file in to a single string
password_list = open_file.read()

# Close the file
open_file.close()

# Break string at line endings and return a list of passwords
password_list = password_list.splitlines()

# Randomly pick a word to be guessed (As a list of characters)
word_to_guess = list(password_list[random.randint(0, len(password_list)-1)])

# The players current guess for each character (Make copy)
players_guess = list(word_to_guess)

# How many chars of the word to guess will be obfuscated?
chars_to_replace = len(word_to_guess)/2

# Obfuscate players current guess
while players_guess.count("_") < chars_to_replace:
  players_guess[random.randint(0, len(players_guess)-1)] = "_"

while word_to_guess != players_guess:
  #print(''.join(word_to_guess))
  print(''.join(players_guess))

  guess = input("Guess a missing character: ")
  for i in range(len(word_to_guess)):
    if players_guess[i] == "_" and  word_to_guess[i] == guess:  
      players_guess[i] = word_to_guess[i]
      #break # If not all occurences are replaced  

print("You guessed it! Moving on....")
