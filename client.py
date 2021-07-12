from os import read, write
import socket
import select
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8000))


name = None  # 자신의 이름을 저장할 변수


while True:
    read, write, fail = select.select((s, sys.stdin), (), ())
    # (사용자의 키보드 입력을 기다림(엔터를 칠 때까지))

    for desc in read:
        if desc == s:
            # 만약 서버에서 온 메시지라면 : 메시지 출력
            data = s.recv(4096)
            print(data.decode())

            if name is None:  # 처음 접속했다면 :
                name = data.decode()  # 부여받은 이름 저장
                s.send(f"{name} 님이 접속하셨습니다.".encode())
                # 다른 사람들에게 접속 사실 알림
        else:
            # 만약 사용자가 입력한 메시지라면 : 사용자가 입력한 문자열을 읽어 서버에 전송
            msg = desc.readline()
            msg = msg.replace("\n", "")
            s.send(f"{name} >> {msg}".encode())
            # 메시지를 보낼 때 자신의 이름도 함께 보냄.
