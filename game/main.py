import random

N = [2, 0, 0, 3, 7, 1, 2]
E = [7, 3, 0, 0, 4, 5, 4]
S = [6, 7, 4, 5, 0, 0, 5]
W = [0, 1, 2, 7, 6, 0, 1]

DS = ['Холодная и мокрая',
      'Темная и закоптелая',
      'Туманная и призрачная',
      'Грязная и мрачная',
      'Пустая и страшная',
      'Наполненная ужасными призраками',
      'Наполненная жуткими привидениями']

T = [1, 2, 3, 4, 5, 6, 7]
TS = ['Ящик с золотом',
      'Ящик жевательной резинки',
      'Ящик сандвичей',
      'Ящик мусора',
      'Ящик с медом',
      'Ящик с драгоценными камнями',
      'Ящик с монетами']

m = 0
c = 0
f = 0
r = 0


def printhelp():
    strhelp = '''
Семь пещер образуют лабиринт. В каждой пещере находится ящик с сокровищами. Вы должны собрать все сокровища в одну пещеру за 28 движений.

Эти команды понятны компьютеру:
HELP: Информация о правилах игры
N, E, S, W: двигаться в направлении N (север), E (восток), S (юг), W (запад)
GRAB: Поднять сокровище
PUT: Положить сокровище
LOCATE: Вывести текущее расположение сокровищ

'''
    print(strhelp)


def cave_description():
    fl = 0
    print(f'Вы в пещере {r}')
    print(f'Это {DS[r - 1]} пещера')
    print('В ней находится:')
    for k in range(7):
        if T[k] == r:
            print(TS[k])
            fl = 1
    if fl == 0:
        print('Ничего')


def move(route):
    global r
    x = 0
    if route == 'N':
        x = N[r - 1]
    elif route == 'E':
        x = E[r - 1]
    elif route == 'S':
        x = S[r - 1]
    elif route == 'W':
        x = W[r - 1]
    if x == 0:
        print('Нельзя идти в эту сторону')
    else:
        r = x


def grab():
    global c
    y = -1
    if c == 1:
        print('Нельзя переносить больше одного ящика')
    else:
        for k in range(7):
            if T[k] == r:
                y = k
        if y == -1:
            print('Эта пещера пуста')
        else:
            T[y] = 999
            print(f'Хорошо. Вы перенесете {TS[y]}')
            c = 1


def put():
    global c
    if c == 0:
        print('Вы ничего не несете')
    else:
        for k in range(7):
            if T[k] == 999:
                print(f'{TS[k]} поставлен в пещере {r}')
                T[k] = r
                c = 0


def locate():
    vtext = 'Вы несете:'
    if c == 0:
        print(f'{vtext} Ничего')
    else:
        for k in range(7):
            if T[k] == 999:
                print(f'{vtext} {TS[k]}')
    print('В пещерах находятся:')
    for k in range(7):
        if T[k] != 999:
            print(f'{T[k]} : {TS[k]}')


if __name__ == '__main__':
    printhelp()
    r = random.choice(T)
    cave_description()
    while True:
        ans = input('Что вы намерены делать?')
        if ans == 'HELP':
            printhelp()
        elif ans == 'N' or ans == 'E' or ans == 'S' or ans == 'W':
            move(ans)
        elif ans == 'GRAB':
            grab()
        elif ans == 'PUT':
            put()
        elif ans == 'LOCATE':
            locate()
        m += 1

        w = T[0]
        for k in range(1, 7):
            if w != T[k]:
                f = 1
        if f == 1:
            f = 0
        else:
            print('Отличная работа. Вы перенесли все сокровища')
            print(f'в пещеру {r} за {m} движений')
            break

        if m > 28:
            print('К сожалению, вы превысили допустимый лимит движений')
            break

        if ans == 'N' or ans == 'E' or ans == 'S' or ans == 'W':
            cave_description()
        else:
            print(f'Вы еще в пещере {r}')
