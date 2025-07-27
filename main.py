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
        [
            types.InlineKeyboardButton(text="Очистить список", callback_data="task_delall"),
            types.InlineKeyboardButton(text="Изменить задачу", callback_data="task_update"),
         
        ]
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
update_task_flag = False

@dp.message(F.text)
async def message_handler(message: types.Message):
  user_message = message.text

  global add_task_flag 
  global del_task_flag
  global update_task_flag
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
    elif del_task_flag:
      try:
        if user_message in show_tasks_ids():
          delete_task(user_message)
          await message.answer(f'Задача под номером {user_message} удалена')
          del_task_flag = False
          await message.answer(show_tasks(), reply_markup=tasks_keyboard())
        else:
          await message.answer('Задачи с таким номером нет')
      except Exception:
         await message.answer('Введите целое число существующего номера задачи.')
         await message.answer(show_tasks(), reply_markup=tasks_keyboard())
    elif update_task_flag:
      if ' ' not in user_message:
        await message.answer('Между номером и задачей должен быть пробел.')
        await message.answer(show_tasks(), reply_markup=tasks_keyboard())
      else:
        updating_text = user_message.split()
        updated_text_id = updating_text[0]
        updating_text_task = updating_text[1::]

        updated_text_task = ''
        for i in updating_text_task:
          updated_text_task+=i+' '
        if updated_text_id in show_tasks_ids():
          update_task(updated_text_id, updated_text_task)
          await message.answer(f'Ваша задача под номером {updated_text_id} была изменена')
          update_task_flag=False
          await message.answer(show_tasks(), reply_markup=tasks_keyboard())
        else:
          await message.answer('Задачи с таким номером нет. Вы че изменить хотите то')
          await message.answer(show_tasks(), reply_markup=tasks_keyboard())
    else:
      await message.answer('Не понял зачем вы это написали. Выберите нужную опцию')
    

@dp.callback_query(F.data.startswith("task_"))
async def callbacks(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    print(action)
    global update_task_flag
    global add_task_flag
    global del_task_flag
    global delall_task_flag
    global delall_task_flag_q

    if action == "add":
        add_task_flag = True
        await callback.message.answer(f"Напишите здачу которую хотите добавить:")

    elif action == "del":
        del_task_flag = True
        await callback.message.answer(f"Напишите номер задачи которую хотите удалить:")
    elif action == "delall":
        delall_task_flag_q = True
        await callback.message.answer(f"Вы действительно хотите очистить список дел?", reply_markup=delall_keyboard())
    elif action == 'update':
        update_task_flag = True
        await callback.message.answer('Напишите номер задачи которую хотите изменить и новую задачу, через пробел')
    elif action == 'yes':
        delall_task_flag = True
        delete_all_tasks()
        await callback.message.answer('Ваш список дел очищен')
        await callback.message.answer(show_tasks())
    elif action == 'no':
        delall_task_flag = False
        await callback.message.answer('Ну нет так нет')
        await callback.message.answer(show_tasks())

    
    
       


 # Запуск бота
async def main():
     await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())
