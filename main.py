import asyncio
import logging
import sys
from datetime import datetime, timedelta
from urllib.request import BaseHandler
import requests

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Poll, PollAnswer
from aiogram.methods.send_poll import SendPoll

from config import *
from functions import *
from options import *

from magic_filter import F


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    userId = message.from_user.id
    if await CheckFollow(userId=userId):
        await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\nQuyidagilardan kerakligini tanlang!", reply_markup=SubjectsInlineKeyboard.as_markup())
    else:
        await message.answer("Siz kanallarimizga obuna bo'lmagansiz!❌", reply_markup=ChannelsInlineKeyboard.as_markup())


@dp.message(Command("set"))
async def SetTestNum(msg: Message):
    if msg.from_user.id != ADMINID:
        return

    info = msg.text.split()
    if len(info) == 1:
        await msg.reply("Siz qiymatni kiritmadingiz, quyidagicha yozish kerak edi: /set 10 (istalgan qiymat)")
        return
    
    if str.isdigit(info[1]) == False:
        await msg.reply("Qiymat son ko'rinishida bo'lishi shart!")
        return
    
    SetTestNum(info[1])
    await msg.reply(f"Test soni {info[1]} ga o'zgartirildi )")



@dp.callback_query(F.data == "English")
async def EnglishMenu(callback: CallbackQuery):
    await callback.message.answer(f"📕Ingliz tili \n♾ Testlar soni - {GetTestNum()}\n", reply_markup=EnglishOptions.as_markup())

@dp.callback_query(F.data == "Math")
async def MathMenu(callback: CallbackQuery):
    await callback.message.answer(f"📕Matematika\n♾ Testlar soni - {GetTestNum()}\n", reply_markup=MathOptions.as_markup())

@dp.callback_query(F.data == "StartEnglishTest")
async def StartEnglishTest(callback: CallbackQuery):
    await callback.answer(html.bold("Kuting, tayyorlanmoqda ... "))
    userId = callback.from_user.id
    response = requests.get(f"https://localhost:7047/api/Users/exist/{userId}", verify=False)
    userExists = False

    if 'false' in str(response.content):
        userExists = False
    else:
        userExists = True

    print(f"User exists: {userExists}")
    if userExists:
        await bot.send_message(userId, html.bold("Siz avval ishtirok etgansiz!\n Faqat bir marotaba ishtirok etish mumkin..."))
        return

    #save the user
    userModel = {
        "telegramId": str(userId)
    }

    headers = {
        "Content-Type": "application/json"
    }

    url = "https://localhost:7047/api/Users"
    requests.post(url=url, json=userModel, headers=headers, verify=False)
    ##

    for questionCount in range(1, GetTestNum() + 1):
        try:
            question = GetRandomQuestion("english")
            poll = await bot.send_poll(
                chat_id=callback.from_user.id,
                question=f"{questionCount}. {question["question"]}",
                options=question["options"],
                type="quiz",
                close_date=datetime.now() + timedelta(seconds=question["sec"]),
                allows_multiple_answers=False,
                is_anonymous=False,
                correct_option_id=question["correct"],
                protect_content=True
            )
            await asyncio.sleep(question['sec'])

            dctPoll = dict(dict(poll)["poll"])

            pollModel = {
                "pollId": f"{dctPoll['id']}",
                "correctOptionId":  dctPoll["correct_option_id"]
            }
            requests.post(url="https://localhost:7047/api/Polls", json=pollModel, headers=headers, verify=False)
        except Exception:
            print(f"Exception occured: {Exception}")
            
    await bot.send_message(userId, "Natija hisoblanyapti...")
    res = requests.get(f"https://localhost:7047/api/Users/result/{userId}", verify=False)

    await bot.send_message(userId, f"Tabriklanmiz🎉\nSiz {str(res.content).replace('b', '')} ta savolga to'g'ri javob berdingiz.")

@dp.callback_query(F.data == "StartMathTest")
async def StartEnglishTest(callback: CallbackQuery):
    await callback.answer(html.bold("Kuting, tayyorlanmoqda ... "))
    userId = callback.from_user.id
    response = requests.get(f"https://localhost:7047/api/Users/exist/{userId}", verify=False)
    userExists = False

    if 'false' in str(response.content):
        userExists = False
    else:
        userExists = True

    if userExists:
        await bot.send_message(userId, html.bold("Siz avval ishtirok etgansiz!\n Faqat bir marotaba ishtirok etish mumkin..."))
        return

    #save the user
    userModel = {
        "telegramId": str(userId)
    }

    headers = {
        "Content-Type": "application/json"
    }

    url = "https://localhost:7047/api/Users"
    requests.post(url=url, json=userModel, headers=headers, verify=False)
    ##

    for questionCount in range(1, GetTestNum() + 1):
        try:
            question = GetRandomQuestion("math")
            poll = await bot.send_poll(
                chat_id=callback.from_user.id,
                question=f"{questionCount}. {question["question"]}",
                options=question["options"],
                type="quiz",
                close_date=datetime.now() + timedelta(seconds=question["sec"]),
                allows_multiple_answers=False,
                is_anonymous=False,
                correct_option_id=question["correct"],
                protect_content=True
            )
            await asyncio.sleep(question['sec'])

            dctPoll = dict(dict(poll)["poll"])

            pollModel = {
                "pollId": f"{dctPoll['id']}",
                "correctOptionId":  dctPoll["correct_option_id"]
            }
            requests.post(url="https://localhost:7047/api/Polls", json=pollModel, headers=headers, verify=False)
        except Exception:
            print(f"Exception occured: {Exception}")
            
    await bot.send_message(userId, "Natija hisoblanyapti...")
    res = requests.get(f"https://localhost:7047/api/Users/result/{userId}", verify=False)

    await bot.send_message(userId, f"Tabriklanmiz🎉\nSiz {str(res.content).replace('b', '')} ta savolga to'g'ri javob berdingiz.")


@dp.poll_answer()
async def poll_res(pollAnswer: PollAnswer):
    try:
        dctPoll = dict(pollAnswer)
        poll_id = dctPoll['poll_id']
        option_id = dctPoll['option_ids'][0]
        user_id = dctPoll['user'].id

        answerModel = {
            "pollId": str(poll_id),
            "optionId": int(option_id),
            "telegramId": str(user_id)
        }

        headers = {
            "Content-Type": "application/json"
        }

        url = "https://localhost:7047/api/UserAnswers"
        res = requests.post(url=url, json=answerModel, headers=headers, verify=False)
        print("Response status code : ", res.status_code)

    except:
        print("Javob saqlanmadi ... )))")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
