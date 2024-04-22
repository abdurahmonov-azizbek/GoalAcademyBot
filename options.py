from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from config import BOT, FollowChannels

# Majburiy a'zolikdagi kanallar uchun
ChannelsInlineKeyboard = InlineKeyboardBuilder()
count = 1
for channel in FollowChannels:
    ChannelsInlineKeyboard.row(
        InlineKeyboardButton(
            text=f"{count} - KANAL⚡️", 
            url=channel
        )
    )
    count += 1

ChannelsInlineKeyboard.row(
    InlineKeyboardButton(
        text="✅Tasdiqlash", 
        url=f"{BOT}?start=True"
    )
)
#

#Fanlar uchun 
SubjectsInlineKeyboard = InlineKeyboardBuilder()
SubjectsInlineKeyboard.row(
    InlineKeyboardButton(
        text="📕Ingliz tili",
        callback_data="English"
    )
)
SubjectsInlineKeyboard.row(
    InlineKeyboardButton(
        text="📕Matematika",
        callback_data="Math"
    )
)

SubjectsInlineKeyboard.row(
    InlineKeyboardButton(
        text="📕Rus tili",
        callback_data="Russian"
    )
)

SubjectsInlineKeyboard.row(
    InlineKeyboardButton(
        text="📕Dasturlash IT",
        callback_data="IT"
    )
)
#

#Ingliz tili uchun 
EnglishOptions = InlineKeyboardBuilder()
EnglishOptions.add(
    InlineKeyboardButton(
        text="🤩Boshlash",
        callback_data="StartEnglishTest"
    )
)

MathOptions = InlineKeyboardBuilder()
MathOptions.add(
    InlineKeyboardButton(
        text="🤩Boshlash",
        callback_data="StartMathTest"
    )
)