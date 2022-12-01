"""Guess number game"""

import numpy as np

number = np.random.randint(1,101)

count = 0

while True:
    count+=1
    predict_number = int(input('Input number: '))
    
    if predict_number < number:
        print('The answer is MORE')
    elif predict_number > number:
        print('The answer is LESS')
    else:
        print(f'Exactly! Correct answer is {number}. It takes {count} attempts to guess.')
        break #end of the game