Autor apl1978 github.com/apl1978/

# A Treasure hunt game
The game is dedicated to the 1984 book "Practise your BASIC" by G. Waters and N.Cutler, which I have loved since childhood and thanks to which I became a programmer.

There are 2 files in the project - main.py - fully working game code, launched in the console. Written as close as possible to the code from the book. tg_bot.py - telegram bot with this game.
The code is somewhat rewritten, but the meaning of the game remains the same.

## Settings
Rename the config.py.example file to config.py. Set the token variable to the token that BotFather will issue. Enter your telegram id in the admin_id variable.
Rename the game_stat.db3.example file to game_stat.db3 and move it to the game folder.

## Third-party libraries
pyTelegramBotAPI

# Игра Поиски сокровищ
Игра посвящена книге "Осваиваем микрокомпьютер" Г.Уотерс, Н.Катлер 1989г (русское издание книги "Practise your BASIC" by G. Waters and N.Cutler 1984 года),
которую я люблю с детства и благодаря которой я и стал программистом.

В проекте 2 файла - main.py - полностью рабочий код игры, запускается в консоли. Написан макисмально похоже на код из книги. tg_bot.py - телеграмбот с этой игрой.
Код несколько переписан, но смысл игры остался прежним.

## Настройки
Файл config.py.example переименовать в config.py. В переменную token прописать токен, который выдаст BotFather. В переменную admin_id прописать свой id телеграм.
Файл game_stat.db3.example переименовать в game_stat.db3 и переместить в папку game.

## Сторонние библиотеки
pyTelegramBotAPI
