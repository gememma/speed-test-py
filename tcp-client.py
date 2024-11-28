# tcp-client.py
# adapted from https://realpython.com/python-sockets

import socket
from time import perf_counter

HOST = "127.0.0.1"  # the server's hostname or IP address
PORT = 80  # the port used by the server


def speed_test(message) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # start timer
        time_start = perf_counter()

        # connect and send data
        s.connect((HOST, PORT))
        s.sendall(message)

        # receive reply
        data = s.recv(1024)
        time = perf_counter() - time_start

        return time


def multi_test():
    messages = [
        b"1",
        b"still tiny",
        b"yep still too small cmon let's get into it",
        b"A copypasta is a block of text copied and pasted to the Internet and social media. Copypasta containing controversial ideas or lengthy rants are often posted for humorous purposes, to provoke reactions from those unaware that the posted text is a meme.",
        b"If gar has a million fans, then I am one of them. If gar has ten fans, then I am one of them. If gar has only one fan then that is me. If gar has no fans, then that means I am no longer on earth. If the world is against gar, then I am against the world. If gar has a million fans, then I am one of them. If gar has ten fans, then I am one of them. If gar has only one fan then that is me. If gar has no fans, then that means I am no longer on earth. If the world is against gar, then I am against the world.",
        b"The FitnessGram TM Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start.",
    ]

    total_speed = 0
    print(f"=== MULTI TEST")

    # speed test for each string
    for msg in messages:
        time = speed_test(msg)
        speed = (len(msg) * 2 + 8) / time

        # print each time / size / speed
        print(f"{time:.4f} secs, {len(msg)} bytes, {speed:.1f} b/s")
        total_speed += speed

    # print avg speed
    avg = total_speed / len(messages)
    print(f"Average speed: {avg:.1f} bytes/sec")


# blocks the socket until all the need data is given
# from https://stackoverflow.com/a/78963001
def recvall(self, length):
    received = 0
    res = b""
    while received < length:
        res += self.recv(length - received)
        received = len(res)
    return res


def speed_test_with_recvall(message) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # start timer
        time_start = perf_counter()

        # connect and send data
        s.connect((HOST, PORT))
        bytes_sent = s.send(message)

        # receive reply
        socket.socket.recvall = recvall  # socket class is patched
        data = s.recvall(len(message) + 200)
        time = perf_counter() - time_start

        # check all bytes were received
        print(f"recv {len(data)} bytes")

        return (time, bytes_sent)


def single_test():
    with open("warandpeace.txt", "r") as f:
        content = f.readlines()
    data = "".join(content)
    msg = str.encode(data)

    print(f"=== SINGLE TEST")
    (time, bytes_sent) = speed_test_with_recvall(msg)
    speed = (bytes_sent * 2 + 100) / time

    # print each time / size / speed
    print(f"{time:.4f} secs, {bytes_sent * 2 + 100} bytes, {speed:.1f} b/s")


# run either the single test (longer message received in multiple parts)
# or the multi test (six shorter messages) or multiple
single_test()
multi_test()
