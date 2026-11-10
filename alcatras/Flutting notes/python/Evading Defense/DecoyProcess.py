import signal, sys
from setproctitle import setproctitle
from time import sleep

def terminated(signum, frame): 
    pass

decoy_name = "notepad"
setproctitle(decoy_name)


# Блокируем сигналы, без этого sigwaitinfo не работает
signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})

siginfo = signal.sigwaitinfo({signal.SIGINT, signal.SIGTERM})

with open("terminated.txt", "w+") as f:
    f.write("Process terminated by %d\n" % siginfo.si_pid)

sys.exit(0)