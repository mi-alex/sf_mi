import numpy as np
import collections as col
import time as t
import math as m
#np.random.seed(1)

def start_board() -> list: # формирует начальную матрицу из одних нулей
    board = []
    zero_line = [0,0,0,0]
    for line_num in range(4):
        board.append(zero_line)
    return(board)

def count_zero(board) -> int: # считает число нулей на доске
    count_zero = 0
    for line_num in range(4):
        cur_line = board[line_num]
        count_zero += cur_line.count(0)
    return(count_zero)

def game_over(board) -> bool: # проверяет, окончена ли игра
    if can_move(my_board, 'down') or can_move(my_board, 'up') or can_move(my_board, 'left') or can_move(my_board, 'right'):
        return(False)
    else:
        return(True)

def you_win(board) -> bool: # проверяет, выиграл ли игрок
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])
    if max(board_list) == 2048:
        return(True)
    else:
        return(False)

def next_number(board) -> list: # очередной "ход" машины: ставит на пустое место число 2 или 4
    choose_num = np.random.randint(10)
    random_num = np.random.randint(count_zero(board))
    for line_num in range(4):
        cur_line = list(board[line_num])
        for row_num in range(4):
            if cur_line[row_num] != 0:
                pass
            else:
                if random_num == 0:
                    cur_line[row_num] = 4 if choose_num == 0 else 2
                    board[line_num] = cur_line
                    return(board)
                else:
                    random_num -= 1

def can_move(board, direction) -> bool: #проверка, можно ли свайпнуть в определённом направлении
    res = False
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])
    if direction == 'down':
        template = list(range(0, 12))
        shift = 4
    elif direction == 'up':
        template = list(range(4, 16))
        shift = -4
    elif direction == 'left':
        template = [1,2,3,5,6,7,9,10,11,13,14,15]
        shift = -1
    elif direction == 'right':
        template = [0,1,2,4,5,6,8,9,10,12,13,14]
        shift = 1
    else:
        return(False)
    for item in template:
        if board_list[item] == board_list[item+shift] != 0:
            res = True
    for item in template:
        if (board_list[item] != 0) and (board_list[item+shift] == 0):
            res = True    
    return(res)

def swipe_line(line) -> list: # схлопывание ряда от начала к концу
    a = line[0]
    b = line[1]
    c = line[2]
    d = line[3]
    sw_line = []
    if line.count(0) == 4:
        sw_line = [0, 0, 0, 0]
    elif line.count(0) == 3:
        if d != 0:
            sw_line = [0, 0, 0, d]
        elif c != 0:
            sw_line = [0, 0, 0, c]
        elif b != 0:
            sw_line = [0, 0, 0, b]
        elif a != 0:
            sw_line = [0, 0, 0, a]
    elif line.count(0) == 2:
        if c != 0 and d != 0 and c == d:
            sw_line = [0, 0, 0, c + d]
        elif c != 0 and d != 0 and c != d:
            sw_line = [0, 0, c, d]
        elif b != 0 and d != 0 and b == d:
            sw_line = [0, 0, 0, b + d]
        elif b != 0 and d != 0 and b != d:
            sw_line = [0, 0, b, d]
        elif b != 0 and c != 0 and b == c:
            sw_line = [0, 0, 0, b + c]
        elif b != 0 and c != 0 and b != c:
            sw_line = [0, 0, b, c]
        elif a != 0 and d != 0 and a == d:
            sw_line = [0, 0, 0, a + d]
        elif a != 0 and d != 0 and a != d:
            sw_line = [0, 0, a, d]
        elif a != 0 and c != 0 and a == c:
            sw_line = [0, 0, 0, a + c]
        elif a != 0 and c != 0 and a != c:
            sw_line = [0, 0, a, c]
        elif a != 0 and b != 0 and a == b:
            sw_line = [0, 0, 0, a + b]
        else:
            sw_line = [0, 0, a, b]
    elif line.count(0) == 1:
        if a == 0:
            if c == d:
                sw_line = [0, 0, b, c + d]
            elif b == c:
                sw_line = [0, 0, b + c, d]
            else:
                sw_line = [0, b, c, d]
        elif b == 0:
            if c == d:
                sw_line = [0, 0, a, c + d]
            elif a == c:
                sw_line = [0, 0, a + c, d]
            else:
                sw_line = [0, a, c, d]
        elif c == 0:
            if b == d:
                sw_line = [0, 0, a, b + d]
            elif a == b:
                sw_line = [0, 0, a + b, d]
            else:
                sw_line = [0, a, b, d]
        else:
            if b == c:
                sw_line = [0, 0, a, b + c]
            elif a == b:
                sw_line = [0, 0, a + b, c]
            else:
                sw_line = [0, a, b, c]
    else:
        if c == d:
            if a == b:
                sw_line = [0, 0, a + b, c + d]
            else:
                sw_line = [0, a, b, c + d]
        else:
            if b == c:
                sw_line = [0, a, b + c, d]
            else:
                if a == b:
                    sw_line = [0, a + b, c, d]
                else:
                    sw_line = [a, b, c, d]
    return(sw_line)

def swipe_board(board, direction) -> list: # свайп доски в указанную сторону
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])
    if direction == 'down':
        for row_num in range(4):
            line_to_swipe = []
            for line_num in range(4):
                line_to_swipe.append(board_list[4*line_num + row_num])
            swiped_line = swipe_line(line_to_swipe)
            for line_num in range(4):
                board_list[4*line_num + row_num] = swiped_line[line_num]
    elif direction == 'up':
        for row_num in range(4):
            line_to_swipe = []
            for line_num in range(4):
                line_to_swipe.append(board_list[4*(3-line_num) + row_num])
            swiped_line = swipe_line(line_to_swipe)
            for line_num in range(4):
                board_list[4*(3-line_num) + row_num] = swiped_line[line_num]
    elif direction == 'left':
        for line_num in range(4):
            line_to_swipe = []
            for row_num in range(4):
                line_to_swipe.append(board_list[4*line_num + (3-row_num)])
            swiped_line = swipe_line(line_to_swipe)
            for row_num in range(4):
                board_list[4*line_num + (3-row_num)] = swiped_line[row_num]
    elif direction == 'right':
        for line_num in range(4):
            line_to_swipe = []
            for row_num in range(4):
                line_to_swipe.append(board_list[4*line_num + row_num])
            swiped_line = swipe_line(line_to_swipe)
            for row_num in range(4):
                board_list[4*line_num + row_num] = swiped_line[row_num]
    else:
        pass
    board = []
    for line_num in range(4):
        line_to_add = []
        for row_num in range(4):
            line_to_add.append(board_list[4*line_num + row_num])
        board.append(line_to_add)
    return(board)

def print_board(board): # печать текущей матрицы
    for line_num in range(4):
        cur_line = list(board[line_num])
        for row_num in range(4):
            print(cur_line[row_num], end = '')
            for space_num in range(5 - len(str(cur_line[row_num]))):
                print(' ', end= '')
        print('\n', end = '')

def estimate_board(board, direction) -> int: # оценка доски
    estim = 0
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])  # развернули доску в один список из 16 элементов
    
    if direction == 'down':    
        for line_num in range(3):
            for row_num in range(4):
                if board_list[4*line_num + row_num] == board_list[4*(line_num + 1) + row_num]:
                    estim += board_list[4*line_num + row_num]

    elif direction == 'right' or direction == 'left':
        for row_num in range(3):
            for line_num in range(4):
                if board_list[4*line_num + row_num] == board_list[4*line_num + row_num + 1]:
                    estim += board_list[4*line_num + row_num]
    else:
        pass
    return(estim)  

def eval_up_prob(test_board) -> bool: # оценка вероятности вынужденного up
    danger = False
        
    if count_zero(test_board) not in [5,9]:
        return False

    board_list = []
    for line_num in range(4):
        board_list.extend(test_board[line_num])
        
    for attempt in range(10):
        try_board = next_number(test_board)
        if not can_move(try_board, 'down') and not can_move(try_board, 'left'):
            danger = True
        test_board = []
        for line_num in range(4):
            line_to_add = []
            for row_num in range(4):
                line_to_add.append(board_list[4*line_num + row_num])
            test_board.append(line_to_add)
    
    return(danger)

def eval_monotocity(board) -> int: # оценка монотонности
    eval = 0
    
    bl = []
    for line_num in range(4):
        bl.extend(board[line_num])
    bl1 = [num + 1 if num == 0 else num for num in bl]
    snake = [12,13,14,15,11,10,9,8,4,5,6,7,3,2,1,0]
    
    for item in range(len(snake) - 1):
        upper = m.log(bl1[snake[item]], 2)
        lower = m.log(bl1[snake[item + 1]], 2)
        if upper > lower:
            eval += (12 - upper + lower)
        else:
            eval -= (upper - lower)**2
    
    scale = m.log(max(bl), 2)
    eval *= m.log(scale, 2)
        
    return(int(eval/16))

def decision_maker(board, echo) -> str: # принятие решения о ходе
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])  # развернули доску в один список из 16 элементов
    
    third_line = board_list[8:12]           # третья строка
    last_line = board_list[12:16]           # четвёртая строка
    eval = eval_res(board)                  # максимальное число в матрице
    can_down = can_move(board, 'down')
    can_left = can_move(board, 'left')
    can_right = can_move(board, 'right')

    if board_list[12] < board_list[13]:
        corner_problem = True
    else:
        corner_problem = False

    if sum(third_line) > 4*sum(last_line) and can_down:
        # если третья строка содержит большие числа, чем четвёртая, и можно вниз, то вниз
        # такое нужно в случае вынужденного up, чтобы сразу вернуть вниз
        if echo:
            print('Go down after going up')
        return('2')
    
    last_line.reverse()
    if last_line != swipe_line(last_line):
        # если нижнюю строку можно схлопнуть влево, то влево
        if echo:
            print('Go left: swipeable last line')
        return('1')
    elif (third_line != swipe_line(third_line)) and \
        (max(third_line) < min(last_line)) and eval >= 128:
        # если нижняя строка не свайпается и третью можно вправо, то вправо
        if not (corner_problem and can_left):
            if echo:
                print('Go right: swipeable third line')
            return('3')
        else:
            if echo:
                print('Go left: swipeable third line and corner problem')
            return('1')
    else:
        pass        
    
    if can_down and last_line.count(0) > 0 and eval >= 128:
        # если в нижней строке нули и можно вниз, то лучше вниз
        if echo:
            print('Go down to cover zeros in last line')
        return('2')        
    
    # переходим к количественной оценке каждого варианта хода: вниз, влево, вправо
    dn_score = 0
    rd_score = 0
    ld_score = 0
    r_score = 0
    l_score = 0
    d_score = 0
    rr_score = 0
    rl_score = 0
    lr_score = 0
    ll_score = 0

    if can_down:
        dn_score = estimate_board(board, 'down')
        try_board_down = swipe_board(board, 'down')
        if can_move(try_board_down, 'right'):
            r_score = estimate_board(try_board_down, 'right')/2
        if can_move(try_board_down, 'left'):
            l_score = estimate_board(try_board_down, 'left')/2
        if can_move(try_board_down, 'down'):
            d_score = estimate_board(try_board_down, 'down')
        dn_score += max(r_score, l_score, d_score)
        dn_score += eval_monotocity(try_board_down)
        if eval_up_prob(try_board_down):
            dn_score //= m.log(eval, 2)
        dn_score = int(dn_score*1.1)    
        
    if can_right:
        r_score = estimate_board(board, 'right')
        try_board_right = swipe_board(board, 'right')
        if can_move(try_board_right, 'down'):
            rd_score = estimate_board(try_board_right, 'down')
        if can_move(try_board_right, 'right'):
            rr_score = estimate_board(try_board_right, 'right')/2
        if can_move(try_board_right, 'left'):
            rl_score = estimate_board(try_board_right, 'left')/2
        rd_score = max(rd_score, rr_score, rl_score)
        rd_score += r_score
        rd_score += eval_monotocity(try_board_right)
        if eval_up_prob(try_board_right):
            rd_score //= m.log(eval, 2)        
        if corner_problem and eval >= 16:
            rd_score //= 2
        rd_score = int(rd_score)       
            
    if can_left:
        l_score = estimate_board(board, 'left')
        try_board_left = swipe_board(board, 'left')
        if can_move(try_board_left, 'down'):
            ld_score = estimate_board(try_board_left, 'down')
        if can_move(try_board_left, 'right'):
            lr_score = estimate_board(try_board_left, 'right')/2
        if can_move(try_board_left, 'left'):
            ll_score = estimate_board(try_board_left, 'left')/2
        ld_score = max(ld_score, lr_score, ll_score)
        ld_score += l_score
        ld_score += eval_monotocity(try_board_left)
        if eval_up_prob(try_board_left):
            ld_score //= m.log(eval, 2)         
        ld_score = int(ld_score)
                
    # если нижняя строка свайпается вправо, то свайп вправо только при крайней необходимости
    last_line = board_list[12:16]
    if last_line != swipe_line(last_line):
        noright = True
    else:
        noright = False

    if can_down and (not can_left) and ((not can_right) or noright):
        # если можно вниз, а влево и вправо нельзя
        if echo:
            print('Go down by default')
        return('2')            

    if can_down and dn_score >= ld_score and (dn_score >= rd_score or noright):
        # если можно вниз и это лучше по рейтингу
        if echo:
            print(f'Go down because it is better: down {dn_score}, left {ld_score}, right {rd_score}')
            #t.sleep(30)
        return('2')
    
    if can_left and not can_right:
        if echo:
            print('Go left because right is not possible')
        return('1')
    elif can_right and not can_left:
        if echo:
            print('Go right because left is not possible')
        return('3')
    elif can_left and can_right:
        if (ld_score > rd_score) or (noright == True):
            if echo:
                print(f'Go left because it is better: down {dn_score}, left {ld_score}, right {rd_score}')
                #t.sleep(30)
            return('1')     # если свайп влево сулит больше выгоды или свайп вправо грозит последней строке
        else:
            if echo:
                print(f'Go right because it is better: down {dn_score}, left {ld_score}, right {rd_score}')
                #t.sleep(30)           
            return('3')     # если свайп вправо сулит больше выгоды и не грозит последней строке
    else:
        if echo:
            print('Go up because no other possible move')
        return('5')         # от безысходности вверх
 
def eval_res(board) -> int: # возвращает максимальное число на доске   
    board_list = []
    for line_num in range(4):
        board_list.extend(board[line_num])
    res = max(board_list)
    return(res)
    
# Основной текст программы     
current_move = ''       # текущий ход
echo = False            # включён ли вывод сообщений
sleep_time = 2          # пауза между шагами

step_array = []         # массив результатов (число ходов)
res_array = []          # массив результатов (наибольшее число на доске)
repeat_num = 100       # число повторов

for attempt in range(repeat_num):       # основной цикл по числу испытаний
    my_board=start_board()              # получили нулевую доску
    next_number(my_board)               # выбросили два числа на доску
    next_number(my_board)
    step_num = 0
    if echo:
        print(f'Step: {step_num}')
        print_board(my_board)
    while current_move != 's':
        step_num += 1
        if echo:
            t.sleep(sleep_time*step_num/500)
            print('')
            print(f'Step: {step_num}')
        
        current_move = decision_maker(my_board, echo)
        #current_move = input('Enter your move: 2 = down, 5 = up, 1 = left, 3 = right, 0 = stop: ')
        if current_move == '0':
            print('Thank you for the game!')
            break
        elif current_move == '2':
            if can_move(my_board, 'down'):
                my_board = swipe_board(my_board, 'down')
            else:
                print('You cant move down!')
                continue
        elif current_move == '5':
            if can_move(my_board, 'up'):
                my_board = swipe_board(my_board, 'up')
            else:
                print('You cant move up!')
                continue
        elif current_move == '1':
            if can_move(my_board, 'left'):
                my_board = swipe_board(my_board, 'left')
            else:
                print('You cant move left!')
                continue
        elif current_move == '3':
            if can_move(my_board, 'right'):
                my_board = swipe_board(my_board, 'right')
            else:
                print('You cant move right!')
                continue
        else:
            print('Wrong move!')
            continue
        next_number(my_board)
        if echo:
            print_board(my_board)   
        if you_win(my_board):
            if not echo and repeat_num == 1:
                print_board(my_board)
            if echo:
                print('Congratulations! You win!')
            break    
        if game_over(my_board):
            if not echo and repeat_num == 1:
                print_board(my_board)
                print(f'Max step is {step_num}')
                print(f'Max number is {eval_res(my_board)}')
            if echo:
                print('Sorry, game over!')
            break
    step_array.append(step_num)
    res_array.append(eval_res(my_board))

print(f'Average step amount: {int(sum(step_array)/len(step_array))}')
# print(f'Average max number: {int(sum(res_array)/len(res_array))}')
print(f'Best step amount: {max(step_array)}')
print(f'Best max number: {max(res_array)}')
print(f'Count results: {col.Counter(res_array)}')