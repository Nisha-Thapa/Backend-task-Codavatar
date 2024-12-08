from fastapi import __version__ as fastapi_ver
import art
from datetime import datetime

filler = "=".center(35, "=")
print(art.text2art("Cloud Telephony") + f"FastAPI {filler} {fastapi_ver}\n")
print(
    art.text2art("CodAvatar apps")
    + "\t\t\t\t\t\t ver-1.0 \n\t\t\t\t\t\t Cloud Telephony Services \n"
)
print(" Started on : ", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
