from twisted.internet import protocol, reactor
import names
from colorama import Fore, Back

# 어떤 사용자가 보낸 메시지를 다른 사용자에게 전달
transports = set()  # 클라이언트를 저장할 변수
users = set()  # 사용자의 이름을 저장할 변수

COLORS = [
    "\033[31m",  # RED
    "\033[32m",  # GREEN
    "\033[33m",  # YELLOW
    "\033[34m",  # BLUE
    "\033[35m",  # MAGENTA
    "\033[36m",  # CYAN
    "\033[37m",  # WHITE
    "\033[4m",  # UNDERLINE
]


class Chat(protocol.Protocol):
    def connectionMade(self):
        # self.transport.write("connected!".encode())
        # 클라이언트에게 connected 메시지 전송

        name = names.get_first_name()  # 랜덤한 이름 생성
        color = COLORS[len(users) % len(COLORS)]
        # 랜덤한 색상 저장
        users.add(name)  # users에 추가

        transports.add(self.transport)  # 사용자가 접속하면 transport(클라이언트) 추가

        self.transport.write(f"{color}{name}\033[0m".encode())  # 사용자가 접속하면 이름 부여

        print(f"현재 접속자 수 : {len(users)}명")

    def dataReceived(self, data):
        for t in transports:  # 모든 클라이언트를 하나씩 돌면서(for 루프) :
            if self.transport is not t:  # 만일 내가 보낸 메시지가 아니라면 :
                t.write(data)  # 메시지를 전달
        print(data.decode("utf-8"))


class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()


print("🔒 Server Started!")
reactor.listenTCP(8000, ChatFactory())
reactor.run()
