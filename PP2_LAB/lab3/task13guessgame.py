import random

def game():
    number_to_guess=random.randint(1,20)
    number_of_guesses=0
    print("hello, what is your name?")
    a=input()
    print("Well, ",a, "i am thinking of number 1 and 20")
    while True:
        print("Take a guess")
        guess=int(input())
        number_of_guesses+=1
        if guess>number_to_guess:
            print("Too high!")
        elif guess<number_to_guess:
            print("Too low!")
        elif  guess==number_to_guess:
            print ("Good job ", a, "You guessed my number in ",number_of_guesses )
            break
game()    
        
    