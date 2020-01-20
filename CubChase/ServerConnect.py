import socket
from _thread import *
import sys

#server = '' #"192.168.1.100"
port = 5555

server = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Waiting for a connection, Server Started")
#print(server_ip)
print(server)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(400,400),(500,400)]
names = ["none", "none"]
ready = ["0", "0"]


def threaded_client(conn, player):
    while currentPlayer != 2:
        pass

    #posalji pocetnu poziciju
    message = make_pos(pos[player]) + "," + str(player)
    conn.send(str.encode(message))

    #primi ime od igraca
    #name = conn.recv(2048).decode()
    #names[player] = name

    #while names[0] == "none" or names[1] == "none":
        #pass

    #kada oba imena stignu, posalji im ime protivnika
    #reply = ""
    #if player == 0:
        #reply += names[1]
    #else:
        #reply += names[0]
    #conn.send(str.encode(reply))

    while True:
        # sacekaj ready poruku
        print("Waiting for ready signal from " + str(player))
        try:
            rec = conn.recv(2048).decode()
        except:
            break

        if rec == "ready":
            ready[player] = "1"
            print(rec + " " + str(player))

        while ready[0] == "0" or ready[1] == "0":
            pass

        conn.send(str.encode("go"))
        reply = ""
        levelChanged = False
        while not levelChanged:
            try:
                data = conn.recv(2048).decode()
                if data == "finished":
                    levelChanged = True
                    ready[player] = "0"
                    print("Level passed from " + str(player))
                else:
                    data = read_pos(data)
                    pos[player] = data

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        if player == 1:
                            reply = pos[0]
                        else:
                            reply = pos[1]

                        print("Received: ", data)
                        print("Sending : ", reply)

                    conn.sendall(str.encode(make_pos(reply)))

            except:
                break

    print("Lost connection")
    conn.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1