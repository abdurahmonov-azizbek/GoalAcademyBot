import requests
import json


res = requests.get(f"https://localhost:7047/api/Users/exist/6095810791", verify=False).content
print("mana ___\n\n\n")
print(res)
