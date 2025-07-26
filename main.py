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

def delall_keyboard():
  buttons = [
    [
        types.InlineKeyboardButton(text="Да", callback_data="task_yes"),
        types.InlineKeyboardButton(text="Нет", callback_data="task_no"),
    ]
  ]
  keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
  return keyboard


add_task_flag = False
del_task_flag = False
delall_task_flag_q = False
delall_task_flag = False


@dp.message(F.text)
async def message_handler(message: types.Message):
  user_message = message.text

  global add_task_flag 
  global del_task_flag
  global delall_task_flag
  global delall_task_flag_q 

  if user_message=='Список дел':
    await message.answer('Вот список ваших дел:')
    print(show_tasks())
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
    

@dp.callback_query(F.data.startswith("task_"))
async def callbacks(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    print(action)
    global add_task_flag
    global del_task_flag
    global delall_task_flag
    global delall_task_flag_q

    if action == "add":
        add_task_flag = True
        await callback.message.answer(f"Напишите здачу которую хотите добавить:")

    elif action == "del":
        pass
    elif action == "delall":
        delall_task_flag_q = True
        await callback.message.answer(f"Вы действительно хотите очистить список дел?", reply_markup=delall_keyboard())
    elif action == 'yes':
        delall_task_flag = True
        delete_all_tasks()
        await callback.message.answer('Ваш список дел очищен')
        show_tasks()
    elif action == 'no':
        delall_task_flag = False
        await callback.message.answer('Ну нет так нет')
        show_tasks()

    
    
       


 # Запуск бота
async def main():
     await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())
