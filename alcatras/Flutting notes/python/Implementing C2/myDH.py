import socket

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

def recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("peer closed early")
        buf.extend(chunk)
    return bytes(buf)

class myDH:
    def __init__(
        self,
        conn: socket.socket,
        public_key: x25519.X25519PublicKey | None = None,
    ):
        self.conn = conn
        self.public_key = public_key
        self.private_key: x25519.X25519PrivateKey | None = None
        self.peer_public_bytes: bytes

    def self_keys_init(self):
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_general_secret(self):
        general_secret = self.private_key.exchange(
            x25519.X25519PublicKey.from_public_bytes(self.peer_public_bytes)
        )
        return general_secret
    
    def sendDH(self) -> None:
        if self.public_key is None:
            raise ValueError("public key is not initialized")

        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        packet = len(public_bytes).to_bytes(1, "big") + public_bytes
        self.conn.sendall(packet)

    def acceptDH(self):
        key_len = recv_exact(self.conn, 1)[0]
        self.peer_public_bytes = recv_exact(self.conn, key_len)


   
