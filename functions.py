import json
import random
from main import bot
from config import *

async def CheckFollow(userId) -> bool:
    for channel in TgChannels:
        member = await bot.get_chat_member(channel, userId)
        if member.status not in ('creator', 'member', 'administrator'):
            return False
    
    return True

def GetRandomQuestion(subjectName):
    try:
        questionsList = json.loads(open(f"questions/{subjectName}.json").read())
        question = questionsList[random.randint(0, len(questionsList)-1)]
        return question
    except:
        return 

def GetTestNum() -> int:
    s = open('num.txt')
    return int(s.read())

def SetTestNum(num: int) -> None:
    s = open("num.txt", "w")
    s.write(str(num))
    s.close()