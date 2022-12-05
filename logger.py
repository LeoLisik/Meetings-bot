import datetime
import os.path

if not os.path.isdir("logs"):
    os.mkdir("logs")
log_path = f"logs\\log-{str(datetime.datetime.now()).replace(':', '.')[:-7]}.txt"
log_file = open(log_path, "w+")
log_file.write(f"Start log {str(datetime.datetime.now())[:-7]}\n")
log_file.close()
print(f"log: {log_path} created")


def default_log(message: str):
    print(f"{str(datetime.datetime.now())[:-7]}: {message}")
    log_file = open(log_path, 'a')
    log_file.write(f"{str(datetime.datetime.now())[:-7]}: {message}\n")
    log_file.close()
