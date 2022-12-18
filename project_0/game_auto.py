import numpy as np

def bisection_predict(number:int=1, max_num:int=1) -> int:
    """Угадываем число методом половинного деления отрезка

    Args:
        number (int, optional): Загаданное число. Умолчание = 1.
        max_num (int, optional): Максимально возможное число. Умолчание = 1.

    Returns:
        int: Число попыток
    """

    count = 0 # счётчик числа попыток
    current_number = max_num // 2 # начинаем поиск с середины диапазона
    step = max(current_number // 2, 1) # начальный шаг поиска четверть диапазона, но не меньше 1
    while True:
        count += 1
        if number == current_number:
            break # выход из цикла, если угадали
        elif number > current_number:
            current_number = current_number + step # если загаданное число больше, идём вверх на величину шага
        else:
            current_number = current_number - step # если загаданное число меньше, идём вниз на величину шага
        step = max(step // 2, 1) # уменьшаем шаг вдвое, но не меньше 1
    return(count)

def score_game(bisection_predict) -> int:
    """За какое количество попыток в среднем из 1000 подходов угадывает наш алгоритм

    Args:
        bisection_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """

    count_ls = [] # список для сохранения количества попыток
    np.random.seed(1) # фиксируем сид для воспроизводимости
    max_num = 100 # максимально возможное число
    random_array = np.random.randint(1, max_num + 1, size=(1000)) # загадали список чисел

    for number in random_array:
        count_ls.append(bisection_predict(number, max_num))

    score = int(np.mean(count_ls)) # находим среднее количество попыток

    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return(score)

# RUN
if __name__ == '__main__':
    score_game(bisection_predict)