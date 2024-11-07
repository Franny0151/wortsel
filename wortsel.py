
import random
from colorama import init,Fore
from pathlib import Path


#Initalize colorama
init()

#Setup path to wordlist-german.txt
root_dir = Path(__file__).parent
wordlist_german_file = root_dir / 'wordlist-german.txt'

word_size = input(f"\nEnter word size, default is 5 letters: ")

if not word_size.isnumeric() or word_size == "" or word_size == "0":
    word_size = 5

#Generate wordlist and parse by wordsize 
germ_file = open(wordlist_german_file).read().splitlines()
allowed_words = [''.join(string.split()).upper() for string in germ_file if len(string) == int(word_size)]

# Get a random word 
germ_wort = random.choice(allowed_words).upper()

# generate word map
# 1. letters -> occurences i.e {{"G",1},{"R",1}....} 
# 2. pos -> letter i.e. {{"1","G"},{"2","R"}...}
letter_num = dict()
dup_letters = dict()

print(f"\nGuess a letter with {word_size} letters: ")

for i in range(0,len(germ_wort)):
    if germ_wort[i] in letter_num:
        letter_num[germ_wort[i]].add(i)
        if germ_wort[i] in dup_letters:
            dup_letters[germ_wort[i]] = dup_letters[germ_wort[i]] + 1
    else:
        letter_num[germ_wort[i]] = {i}
        dup_letters[germ_wort[i]] = 1

# Define guess size, will loop until you reach the 6th try
guess_num = 1

while(guess_num < 7):

    guess = input(f"\nGuess {guess_num}: ").upper()

    #check if guess is the correct size
    if len(guess) != int(word_size):
        print(f"\nGuess must be {word_size} letters long")
        continue  

    #check if guess is in allowed words
    if guess not in allowed_words: 
        print(f"\nGuess is not in the word list")
        continue

    #create the dup counter map for the guessed word
    dup_ctr = dict()

    for i in range(0,len(guess)):
        
        #if letter of guess is in word dictionary, will either be a match or a mismatch
        #otherwise, letter is completely off 

        if guess[i] in letter_num:
            #check if the index is contained in the value of letter_num
            # if it is - we have a match
            # if it's not - there's a mismatch
            
            if(i in letter_num.get(guess[i])):
                print(f'{Fore.GREEN}{guess[i]}{Fore.RESET}',end=' ')
                
                if guess[i] in dup_ctr:
                    dup_ctr[guess[i]] = dup_ctr[guess[i]] + 1
                
                else:
                    dup_ctr[guess[i]] = 1

            else:
                #need to check if we have enough duplicates - if so, color will be red 
                if guess[i] in dup_letters:
                    if guess[i] in dup_ctr and dup_letters.get(guess[i]) <= dup_ctr.get(guess[i]):
                        print(f'{Fore.RED}{guess[i]}{Fore.RESET}',end=' ')                
                            
                    else:
                        print(f'{Fore.YELLOW}{guess[i]}{Fore.RESET}',end=' ')
                        if guess[i] in dup_ctr:
                            dup_ctr[guess[i]] = dup_ctr[guess[i]] + 1
                        else:
                            dup_ctr[guess[i]] = 1
                        

                else:
                    print(f'{Fore.YELLOW}{guess[i]}{Fore.RESET}',end=' ')
                    
                    if guess[i] in dup_ctr:
                        dup_ctr[guess[i]] = dup_ctr[guess[i]] + 1

                    else:
                        dup_ctr[guess[i]] = 1
        else:
            print(f'{Fore.RED}{guess[i]}{Fore.RESET}',end=' ')

    print("\n")

    #If the guess matches the word
    if guess == germ_wort:
        print(f"\nYou Win!\nTotal tries: {guess_num}")
        break
    
    #Otherwise, increase number tried and output that 
    guess_num+=1
    print(f"\nTries left: {7 - guess_num}")

#If lost, tell the user what the actual word was
if guess_num > 6:
    print(f"\nThe correct word was: {germ_wort}")


