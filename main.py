from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dbsettings import *



TOKEN = "8206501566:AAElICXCaVACUJSxOyQiYtskPgVCuvIJ8ew"  # Замени на свой токен

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
  await message.answer("Приветствую господин. Я ваш личный бот для заметок. 😊👍")
  await message.answer_sticker('CAACAgIAAxkBAAEBetpog_BZgfckilNf3NpYUmmN4-RmCQACZRUAAujW4hK1-GT64wxohzYE')

  kb = [
        [types.KeyboardButton(text="Список дел")],
        [types.KeyboardButton(text="Список проектов")],
        [types.KeyboardButton(text="Заметки")]

  ]
  keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
  await message.answer('Выберите опцию ниже:', reply_markup=keyboard)
  

def tasks_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить задачу", callback_data="task_add"),
            types.InlineKeyboardButton(text="Удалить задачу", callback_data="task_del"),
        ],
        [types.InlineKeyboardButton(text="Очистить список", callback_data="task_delall")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


add_task_flag = False


@dp.message(F.text)
async def message_handler(message: types.Message):
  user_message = message.text

  global add_task_flag 
   
  if user_message=='Список дел':
    await message.answer('Вот список ваших дел:')

    await message.answer(show_tasks(), reply_markup=tasks_keyboard())
    # await message.answer_sticker('CAACAgIAAxkBAAEBeuFohDr4GbtTpzyFs32Vib9_BA9-_gACbBUAAujW4hL2f3MiSHgDODYE')
  elif user_message=='Список проектов':
    pass
  elif user_message=='Заметки':
     pass
  else:
    if add_task_flag:
      add_task(user_message)
      await message.answer('Задача добавлена')
      await message.answer(show_tasks(), reply_markup=tasks_keyboard())
      add_task_flag = False
    else:
      await message.answer('Не понял зачем вы это написали. Выберите нужную опцию')
    

user_data = {}

@dp.callback_query(F.data.startswith("task_"))
async def callbacks(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    global add_task_flag

    if action == "add":
        print('asdasdas')
        add_task_flag = True
        await callback.message.answer(f"Напишите здачу которую хотите добавить:")

    elif action == "del":
        pass
    elif action == "delall":
        pass


 # Запуск бота
async def main():
     await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())
