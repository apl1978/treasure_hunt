""" A Treasure hunt game / Игра Поиски сокровищ
The game is dedicated to the 1984 book "Practise your BASIC" by G. Waters and N.Cutler, which I have loved since
childhood and thanks to which I became a programmer.
The code rewritten in Python style.
Игра посвящена книге "Осваиваем микрокомпьютер" Г.Уотерс, Н.Катлер 1989г., которую я люблю с детства и благодаря которой
я и стал программистом.
Код переписан в Python стиле.
autor apl1978 github.com/apl1978/"""

import random

MOVEMENTS_AVAILABLE = 28

N = [2, 0, 0, 3, 7, 1, 2]
E = [7, 3, 0, 0, 4, 5, 4]
S = [6, 7, 4, 5, 0, 0, 5]
W = [0, 1, 2, 7, 6, 0, 1]

CAVE_DESCRIPTIONS = [
    'Холодная и мокрая', 'Темная и закоптелая', 'Туманная и призрачная',
    'Грязная и мрачная', 'Пустая и страшная',
    'Наполненная ужасными призраками', 'Наполненная жуткими привидениями'
]  #DS

TREASURE_DESCRIPTIONS = [
    'Ящик с золотом', 'Ящик жевательной резинки', 'Ящик сандвичей',
    'Ящик мусора', 'Ящик с медом', 'Ящик с драгоценными камнями',
    'Ящик с монетами'
]  #TS


class Hunter:

  def __init__(self):
    self.movements = 0  #m
    self.carry = False  #c
    self.cave = 0  #r
    self.treasure_location = [1, 2, 3, 4, 5, 6, 7]  #T

  def done(self):
    return all(x == self.treasure_location[0] for x in self.treasure_location)

  def move(self, route):
    x = 0
    if route == 'N':
      x = N[self.cave - 1]
    elif route == 'E':
      x = E[self.cave - 1]
    elif route == 'S':
      x = S[self.cave - 1]
    elif route == 'W':
      x = W[self.cave - 1]
    if x != 0:
      self.cave = x
    return x

  def locate(self):
    vtext = 'Вы несете:'
    if self.carry:
      k = self.treasure_location.index(999)
      text = f'{vtext} {TREASURE_DESCRIPTIONS[k]}\n'
    else:
      text = f'{vtext} Ничего\n'
    text += 'В пещерах находятся:\n'
    text += '\n'.join(
        f'{self.treasure_location[k]} : {TREASURE_DESCRIPTIONS[k]}'
        for k in range(7) if self.treasure_location[k] != 999)
    return text

  def grab(self):
    if self.carry:
      text = 'Нельзя переносить больше одного ящика'
    else:
      trs = [k for k in range(7) if self.treasure_location[k] == self.cave]
      if trs:
        y = trs[-1]
        self.treasure_location[y] = 999
        text = f'Хорошо. Вы перенесете {TREASURE_DESCRIPTIONS[y]}'
        self.carry = True
      else:
        text = 'Эта пещера пуста'
    return text

  def put(self):
    if self.carry:
      k = self.treasure_location.index(999)
      text = f'{TREASURE_DESCRIPTIONS[k]} поставлен в пещере {self.cave}'
      self.treasure_location[k] = self.cave
      self.carry = False
    else:
      text = 'Вы ничего не несете'
    return text


def printhelp():
  strhelp = f'''
Семь пещер образуют лабиринт. В каждой пещере находится ящик с сокровищами. Вы должны собрать все сокровища в одну пещеру за {MOVEMENTS_AVAILABLE} движений.

Эти команды понятны компьютеру:
HELP: Информация о правилах игры
N, E, S, W: двигаться в направлении N (север), E (восток), S (юг), W (запад)
GRAB: Поднять сокровище
PUT: Положить сокровище
LOCATE: Вывести текущее расположение сокровищ

'''
  print(strhelp)


def cave_description(r, T):
  vtext = '\n'.join([TREASURE_DESCRIPTIONS[k] for k in range(7) if T[k] == r])
  if vtext == '':
    vtext = 'Ничего'
  text = f'Вы в пещере {r}\nЭто {CAVE_DESCRIPTIONS[r - 1]} пещера\nВ ней находится:\n{vtext}'
  return text


if __name__ == '__main__':
  hunter = Hunter()
  printhelp()
  hunter.cave = random.randint(1, 7)
  text = cave_description(hunter.cave, hunter.treasure_location)
  print(text)
  hunter.movements = 0
  while (hunter.movements < MOVEMENTS_AVAILABLE) and (not hunter.done()):
    ans = input('Что вы намерены делать?')
    if ans == 'HELP':
      printhelp()
    elif ans == 'N' or ans == 'E' or ans == 'S' or ans == 'W':
      x = hunter.move(ans)
      if x == 0:
        print('Нельзя идти в эту сторону')
    elif ans == 'GRAB':
      text = hunter.grab()
      print(text)
    elif ans == 'PUT':
      text = hunter.put()
      print(text)
    elif ans == 'LOCATE':
      text = hunter.locate()
      print(text)
    hunter.movements += 1

    if hunter.done():
      print('Отличная работа. Вы перенесли все сокровища')
      print(f'в пещеру {hunter.cave} за {hunter.movements} движений')
      break

    if hunter.movements >= MOVEMENTS_AVAILABLE:
      print('К сожалению, вы превысили допустимый лимит движений')
      break

    if ans == 'N' or ans == 'E' or ans == 'S' or ans == 'W':
      text = cave_description(hunter.cave, hunter.treasure_location)
      print(text)
    else:
      print(f'Вы еще в пещере {hunter.cave}')
