import re, os
import hashlib

from dotenv import load_dotenv
load_dotenv()
HASH_PASS_USER = os.getenv('HASH_PASS_USER')
regex_username = re.compile(r"^[a-zA-Z0-9]{3,30}$")
regex_email = re.compile(r"^[a-zA-Z0-9]{3,30}$")
regex_password = re.compile(r"^[a-zA-Z0-9]{3,30}$")

def checkRegex(pattern, content) -> bool:
    if re.fullmatch(pattern, content):
        return True
    else: return False

async def check_validate_login(email: str, password: str):
    if checkRegex(regex_email, email) == True and checkRegex(regex_password, password)==True:
        return True
    else: return False

async def check_validate_register(name: str, email: str, password: str):
    if checkRegex(regex_email, email) == True and checkRegex(regex_password, password)==True and \
        checkRegex(regex_username, name):
        return True
    else: return False

async def hash_password(password):
    passwords = password+ HASH_PASS_USER
    hasher = hashlib.sha256(passwords.encode())
    return hasher.hexdigest()

