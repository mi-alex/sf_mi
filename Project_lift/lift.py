import numpy as np
import collections as col
import statistics
import time as t

# Параметры модели
#np.random.seed(1)                          # seed - включить для повторяемости
height = 18                                 # высота дома в этажах
boarding = 5                                # продолжительность остановки лифта на этаже
intense_1 = 50                              # средняя частота вызовов с 1-го этажа
intense_n = intense_1 * (height-1)          # средняя частота вызовов с n-го этажа (кроме 1-го)
experiment = 100                            # продолжительность экспериментов (число пассажиров)
max_timer = 10000                           # продолжительность экспериментов (время)
repeat = 100                                # количество итераций
echo = False                                # выдавать ли сообщения
speed = 1                                   # задержка при работе в секундах / только для echo = True
total_res = []                              # итоговый массив результатов
mode = 2                                    # режим работы: 1 - последовательно, 2 - попутные вызовы

for iter in range(repeat):
    # Инициализация переменных
    cur_timer = 0                               # переменная (счётчик) для таймера
    cur_exp = 0                                 # переменная (счётчик) клиентов
    lift_position = 1                           # начальное положение лифта
    is_empty = True                                     # пустой лифт или нет  
    res_sum = 0                                 # сумма времени ожидания в итерации
    res_count = 0                               # количество испытаний в итерации 
    last_call = np.zeros(height, dtype=np.int16)        # время последнего вызова с каждого этажа
    floor_count = np.zeros(height, dtype=np.int16)      # счетчик клиентов с каждого этажа
    orders = col.deque()                                # очередь заказов
    results = col.deque()                               # таблица результатов
    cur_boarding = 0                            # счётчик времени посадки
    
    # Инициализация переменных mode = 1
    from_floor = 0                              # этаж отправления текущего заказа
    to_floor = 0                                # этаж назначения текущего заказа
    start_timer = 0                             # момент начала выполнения заказа
    exec_exp = 0                                # счётчик исполняемых заказов
    cur_order = []                                      # текущий заказ
    order_complete = True                               # статус текущего заказа
       
    # Инициализация переменных mode = 2
    exec_orders = col.deque()                                # очередь исполняемых заказов
    remove_orders = col.deque()
    status = 'waiting'

    # Генерация случайных интервалов для моделирования вызовов
    down_call = np.random.exponential(intense_n, (height-1, experiment))
    up_call = np.random.exponential(intense_1, (1, experiment))
    
    # Определение направления заказа
    def get_direction(order):
        if order[1] > order[2]:
            return('down')
        elif order[1] < order[2]:
            return('up')

    while ((exec_exp < experiment) or (not order_complete)) and (cur_timer < max_timer):
        cur_timer += 1              # время тикает на секунду
        message = f'T:{cur_timer}. '
        message += f'Лифт:{lift_position}. '
        
        # если пришло время для вызова вверх, добавляем его в очередь
        if cur_exp < experiment:
            if up_call[0, floor_count[0]] < cur_timer - last_call[0]:
                floor = np.random.randint(height-1) + 2
                orders.append([cur_timer, 1, floor])
                last_call[0] = cur_timer
                floor_count[0] += 1
                cur_exp += 1
                message += f'Вызов {cur_exp}: 1->{floor}. '
    
        # если пришло время для вызова вверх, добавляем его в очередь
        for floor in range(1, height):
            if cur_exp < experiment:
                if down_call[floor-1, floor_count[floor]] < cur_timer - last_call[floor]:
                    orders.append([cur_timer, floor+1, 1])
                    last_call[floor] = cur_timer
                    floor_count[floor] += 1  
                    cur_exp += 1
                    message += f'Вызов {cur_exp}: {floor+1}->1. '
        
        # mode = 1: просто последовательно берём заказы, не агрегируя их
        if mode == 1:
            if orders and order_complete:        
                cur_order = orders.popleft()
                exec_exp += 1
                order_complete = False
                start_timer = cur_order[0]
                from_floor = cur_order[1]
                to_floor = cur_order[2]
                cur_boarding = 0
                
            if orders:
                message += f'Очередь: {len(orders)}. '

            if not(orders) and order_complete:
                message += f'Ожидание. '
                
            if cur_order and not(order_complete):
                message += f'Исполняем {exec_exp}: {from_floor}->{to_floor}. '
                if is_empty:                                            # если лифт пустой
                    if lift_position > from_floor:                      # и выше этажа вызова, едем вниз
                        lift_position -= 1
                    elif lift_position < from_floor:                    # и ниже этажа вызова, едем вверх
                        lift_position += 1         
                    else:                                               # и на этаже вызова, грузимся
                        if cur_boarding < boarding:
                            cur_boarding += 1
                            message += f'Погрузка: {cur_boarding}. '
                        else:
                            cur_boarding = 0
                            is_empty = False
                            message += f'Погрузка завершена. '
                            if lift_position > to_floor:                # если выше целевого этажа, едем вниз
                                lift_position -= 1
                            elif lift_position < to_floor:              # если ниже целевого этажа, едем вверх
                                lift_position += 1         
                else:                                                   # лифт с пассажирами
                    if lift_position > to_floor:                        # и выше целевого этажа, едем вниз
                        lift_position -= 1
                    elif lift_position < to_floor:                      # и ниже целевого этажа, едем вверх
                        lift_position += 1
                    else:                                               # и на целевом этаже, выгружаемся
                        if cur_boarding < boarding:
                            cur_boarding += 1
                            message += f'Выгрузка: {cur_boarding}. '
                        else:
                            cur_boarding = 0
                            is_empty = True
                            cur_order = []
                            order_complete = True
                            results.append([exec_exp, start_timer, cur_timer])
                            message += f'Исполнили {exec_exp}: {from_floor}->{to_floor} за {cur_timer - start_timer}. '
        
        # со взятием попутных вызовов в гружёном состоянии
        elif mode == 2:
            if not(orders) and status == 'waiting':
                message += f'Ожидание. '
            
            if orders and status == 'waiting':                      # пришёл заказ в режиме ожидания
                cur_order = orders.popleft()                        # взяли первый из очереди
                cur_order.append(False)                             # прицепили статус погрузки False
                exec_orders.append(cur_order)                       # включили в исполняемые заказы
                if cur_order[1] > lift_position:                    # устанавливаем статус
                    status = 'empty_up'
                elif cur_order[1] < lift_position:
                    status = 'empty_down'
                elif (cur_order[1] == lift_position) and (cur_order[2] > lift_position):
                    status = 'boarding_up'
                elif (cur_order[1] == lift_position) and (cur_order[2] < lift_position):
                    status = 'boarding_down'
            
            if orders and (status == 'boarding_up' or status == 'full_up'): # попутный вызов наверх
                for order in orders:
                    if get_direction(order) == 'up' and order[1] >= lift_position:
                        order.append(False)
                        if exec_orders[-1][2] < order[2]:
                            exec_orders.append(order)
                        elif exec_orders[0][2] >= order[2]:
                            exec_orders.appendleft(order)
                        elif len(exec_orders) > 1:
                            for i in range(1, len(exec_orders)):
                                if exec_orders[i-1][2] < order[2] and exec_orders[i][2] >= order[2]:
                                    exec_orders.insert(i, order)
                        if order[1] == lift_position:
                            cur_boarding = 0
                for order in exec_orders:
                    if order in orders:
                        orders.remove(order)
            
            if orders and (status == 'boarding_down' or status == 'full_down'): # попутный вызов вниз
                for order in orders:
                    if get_direction(order) == 'down' and order[1] <= lift_position:
                        order.append(False)
                        if exec_orders[-1][1] >= order[1]:
                            exec_orders.append(order)
                        elif exec_orders[0][1] < order[1]:
                            exec_orders.appendleft(order)
                        elif len(exec_orders) > 1:
                            for i in range(1, len(exec_orders)):
                                if exec_orders[i-1][1] >= order[1] and exec_orders[i][1] < order[1]:
                                    exec_orders.insert(i, order)
                        if order[1] == lift_position:
                            cur_boarding = 0
                for order in exec_orders:
                    if order in orders:
                        orders.remove(order)                     
                  
            if status == 'empty_up':                # движение вверх в порожнем состоянии
                if lift_position < exec_orders[0][1]:
                    lift_position += 1
                elif lift_position > exec_orders[0][2]:
                    status = 'boarding_down'
                else:
                    status = 'boarding_up'
            
            if status == 'empty_down':              # движение вниз в порожнем состоянии
                if lift_position > exec_orders[0][1]:
                    lift_position -= 1
                elif lift_position > exec_orders[0][2]:
                    status = 'boarding_down'
                else:
                    status = 'boarding_up'
                        
            if status == 'boarding_up' or status == 'boarding_down': # процесс посадки
                if cur_boarding < boarding:
                    cur_boarding += 1
                    message += f'Погрузка: {cur_boarding}. '
                else:
                    cur_boarding = 0
                    message += f'Погрузка завершена. '
                    if lift_position < exec_orders[0][2]:
                        status = 'full_up'
                    elif lift_position > exec_orders[0][2]:
                        status = 'full_down'
                    for order in exec_orders:
                        if order[1] == lift_position:
                            order[3] = True
            
            if status == 'full_up':             # движение вверх в гружёном состоянии
                if (lift_position == exec_orders[0][1]) and (not exec_orders[0][3]):
                    status = 'boarding_up'
                elif lift_position < exec_orders[0][2]:
                    lift_position += 1
                else:
                    status = 'unboarding'
                 
            if status == 'full_down':           # движение вниз в гружёном состоянии
                need_stop = False
                for exec_order in exec_orders:
                    if (lift_position == exec_order[1]) and (not exec_order[3]):
                        need_stop = True
                if need_stop == True:
                    status = 'boarding_down'
                elif lift_position == exec_orders[0][2]:
                    status = 'unboarding'
                else:
                    lift_position -= 1
                    
            if status == 'unboarding':              # процесс выгрузки
                if cur_boarding < boarding:
                    cur_boarding += 1
                    message += f'Выгрузка: {cur_boarding}. '
                else:
                    cur_boarding = 0
                    message += f'Выгрузка завершена. '
                    for order in exec_orders:
                        if order[2] == lift_position:
                            exec_exp += 1
                            remove_orders.append(order)
                            results.append([exec_exp, order[0], cur_timer])
                            message += f'Исполнили {exec_exp}: {order[1]}->{order[2]} за {cur_timer - order[0]}. '
                    for order in remove_orders:
                        if order in exec_orders:
                            exec_orders.remove(order)
                    remove_orders.clear()
                    if not(exec_orders):
                        status = 'waiting'
                    elif get_direction(exec_orders[0]) == 'up':
                        status = 'full_up'
                    elif get_direction(exec_orders[0]) == 'down':
                        status = 'full_down'

        if echo:                                # логгирование (вывод сообщений), если режим включён
            if mode == 1:
                print(message) 
                t.sleep(speed)   
            elif mode == 2:
                message += f'{status}'
                print(message)
                print(f'Исполняются: {list(exec_orders)}. ')
                if orders or exec_orders:
                    t.sleep(5*speed)
                else:
                    t.sleep(speed)
 
    for item in results:                            # агрегирование результатов по итогам всех экспериментов
        res_count += 1
        res_sum += item[2] - item[1]

    if res_count > 0:
        res = round(res_sum/res_count, 2)
    else:
        res = 0

    if echo:
        #print(results)
        print(f'Средний результат для {res_count} перевозок: {res}')
    
    total_res.append(res)

print(f'Итого: {round(statistics.mean(total_res), 2)}')