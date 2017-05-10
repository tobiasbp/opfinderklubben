#!/usr/bin/python3

# A wonderful game of guessing insecure passwords #


# Import library Random
import random

# The Passwords come from here:
#https://github.com/danielmiessler/SecLists/blob/master/Passwords/10_million_password_list_top_100.txt

# The file to read passwords from
password_file = "passwords.txt"

# How many chars of the word to guess will be obfuscated?
# Start out easy. The player only needs to guess a single character
chars_to_replace = 1

# Open the file with passwords in read mode
open_file = open(password_file, "r")

# Read entire file in to a single string
password_list = open_file.read()

# Close the file
open_file.close()

# Break string at line endings and return a list of passwords
password_list = password_list.splitlines()

# FIXME: Maybe it would be better to continue until the
# player makes x mistakes?
while chars_to_replace < 5:

  # Randomly pick a password to be guessed
  word_to_guess = password_list[random.randint(0, len(password_list)-1)]
  
  # FIXME: What if the password is shorter than the number of characters to guess?
  
  # Convert the password to be guessed from a string to a list of single characters
  word_to_guess = list(password_list[random.randint(0, len(password_list)-1)])
  
  # The players current guess for each character (Make copy)
  players_guess = list(word_to_guess)
  
  # Insert underscores at random place(s) in players guess
  while players_guess.count("_") < chars_to_replace:
    players_guess[random.randint(0, len(players_guess)-1)] = "_"

  # Continue the game until player guesses the word
  while word_to_guess != players_guess:
	  
    # Print players current guess
    print(''.join(players_guess))

    # Let the player choose a character
    guess = input("Guess a missing character: ")
    
    # FIXME: We should make sure, the player only enters a single character
    
    # Find occurences of players guess in word to guess. 
    for i in range(len(word_to_guess)):
      if players_guess[i] == "_" and  word_to_guess[i] == guess:  
        players_guess[i] = word_to_guess[i]
        #break # If not all occurences are replaced  
    
    # FIXME: Let the player know how many characters were matched bu the guess
    
  # PLayer guessed the word. Congratulate her
  print("You guessed it! The correct word was: " + str(''.join(word_to_guess)))

  # Player needs to guess one more character next time around
  chars_to_replace += 1

  print("Moving on to the next level.")
  print("You now need to guess " + str(chars_to_replace) + " characters")

# Game is over
print("Game over. Thank you for playing.")

