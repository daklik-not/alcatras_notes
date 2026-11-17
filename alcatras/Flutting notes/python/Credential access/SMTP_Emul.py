# /// script
# requires-python = ">=3.10"
# dependencies = ["aiosmtpd"]
# ///

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword
import time


def authenticator(server, session, envelope, mechanism, auth_data):
    # isinstance проверяет, принадлежит ли обьект нужному классу
    if isinstance(auth_data, LoginPassword):
        print({auth_data.login.decode()},{auth_data.password.decode()})
        return AuthResult(success=True)
    return AuthResult(success=False, handled=False)

class Handler:
    # Короче этот обьект ведет диалог с клиентом
    # типо например HELLO
    async def handle_DATA(self, server, session, envelope):
        return '250 Messsage accepted for delivery'

if __name__ == '__main__':
    controller = Controller(
        Handler(), 
        hostname="127.0.0.1", 
        port = 25,
        authenticator = authenticator,
        auth_require_tls = False
    )
    controller.start()
    # обьект Controller создает фоновый поток, в котором поднимает
    # асинхронный сервер
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()