import socket
import threading
# Messaggio simulato in formato Syslog

def worker_test():
    
    
    msg2 = "Don't try this at home"
    msg3 = "asd"*1024*10
    msg4 = ""
    msg5 = "<q>q q q: q"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:            
            sock.sendto(msg5.encode('utf-8'), ("127.0.0.1", 5140))

    except Exception as e:
        print(f"Error Stacktrace: {e}")
    finally:
        print("closing thread")
        sock.close()

def avvia_testing_server():

    msg = "<q>q q q: q"
    msg1 = "<r>r r r: r"

    thread_test = threading.Thread(target=worker_test, daemon=True)
    thread_test.start()
    print("Thread1 avviato")
    thread_test1 = threading.Thread(target=worker_test, daemon=True)
    thread_test1.start()
    print("Thread2 avviato")


avvia_testing_server()


