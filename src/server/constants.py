SERVER_HOST_NAME = 'localhost'
SERVER_PORT = 5050

HEADER = 64
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
LOGIN_MESSAGE = "!login"
SIGNUP_MESSAGE = "!signup"
PRINT_USER_COMMAND = "!LIST"
START_SESSION = "!TALK"
BACK_COMMAND = "!BACK"
GET_PUBLIC_KEY = '!GETRSA' # Also used on client side

DUMMY_USER = {"id": 1, "username": 'dummy_username'}


# SCREENS
AUTH_SCREEN = "auth_screen"
MAIN_SCREEN = "main_screen"
CHAT_SCREEN = "chat_screen"