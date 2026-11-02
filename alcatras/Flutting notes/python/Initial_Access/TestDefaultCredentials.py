import paramiko
import telnetlib
import smtplib
import socket
import ftplib
import ssl
import paramiko
import smtplib
import ssl
import socket


host = "127.0.0.1"
sshport = 22
telnetport = 23

def ssh_login(host, username, password, port=22, timeout=5):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=username, password=password,
                       timeout=timeout, banner_timeout=timeout, auth_timeout=timeout,
                       look_for_keys=False, allow_agent=False)
        return "SSH login successful"
    except paramiko.AuthenticationException:
        return "SSH login failed"
    except (paramiko.SSHException, OSError) as e:
        print(f"error {host}: {e}")
        return None
    finally:
        client.close()

def telnet_login(host, port, username, password, timeout=5):
    """True — пустили, False — неверный пароль, None — ошибка связи."""
    tn = None                                    # ← до try, иначе finally упадёт
    try:
        tn = telnetlib.Telnet(host, port, timeout=timeout)
        tn.read_until(b"login: ", timeout=timeout)
        tn.write((username + "\r\n").encode())
        tn.read_until(b"Password: ", timeout=timeout)
        tn.write((password + "\r\n").encode())

        idx, _, _ = tn.expect(
            [b"Last login", b"Login incorrect", b"Login failed", b"Access denied"],
            timeout=timeout,
        )
        if idx == 0:
            return True
        if idx > 0:
            return False
        return None                              # -1: таймаут, ответ не распознали
    except (socket.timeout, OSError, EOFError):
        return None
    finally:
        if tn is not None:                       # ← соединение могло не открыться
            tn.close()

def ftp_login(host, username, password, timeout=15, port=21):
    with ftplib.FTP_TLS(timeout=timeout) as ftps:
        try:
            ftps.connect(host, port)
            ftps.login(username, password)
            return f"Succesful login for {username}:{password}"
        except ftplib.error_perm as e:
            code = int(str(e)[:3])
            #print(repr(e))
            if code == 530 and "Login incorrect" in repr(e):
                return f"Bad credentials for {username}:{password}"
            return f"Some problem with connection"
        except Exception as e:
            return f"Some problem with connection"
        finally:
            try:
                ftps.close()
            except Exception:
                pass
        


def smtp_login(host, username, password, timeout=15):
    
    try:
        server = smtplib.SMTP(host, 587, timeout=timeout)
        server.ehlo() # EHLO - получение расширений от сервера
        server.starttls()
        server.ehlo() # обьект server разберется как ему обрабатывать эти расширения
        server.login(username, password)
        return f'Succesful login for {username}:{password}'
    except smtplib.SMTPAuthenticationError as e:
        code  = e.smtp_code
        if code == 535:
            return f"Bad credentials for {username}:{password}"
        else:
            return f"Some problem with authentication"
    except Exception as e:
        return f"Some problem occured"
    finally:
        try:
            server.close()
        except Exception:
            pass

        



with open("default.txt", "r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        print(ssh_login(host, username, password, port=sshport))
        print(smtp_login("smtp.ethereal.email", username, password))
        print(telnet_login(host, telnetport, username, password))
        print(ftp_login(host, username, password))



