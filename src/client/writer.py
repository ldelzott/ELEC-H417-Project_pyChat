from constants import FORMAT, HEADER


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    try:
        conn.send(send_length)
        conn.send(message)
    except Exception:
        conn.close()
