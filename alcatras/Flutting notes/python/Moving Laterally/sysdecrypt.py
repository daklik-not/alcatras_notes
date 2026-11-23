from pathlib import Path
import win32crypt

BASE = Path(r"E:\chrome_cookie")


def main():
    key = (BASE / "hexkey.txt").read_text().strip()
    out = BASE / "system_decrypted.hex"
    try:
        decrypted_blob = win32crypt.CryptUnprotectData(bytes.fromhex(key))[1]
        out.write_text(decrypted_blob.hex())
    except Exception as e:
        out.write_text("ERROR: " + str(e))

if __name__ == "__main__":
    main()
