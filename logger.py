import datetime

# Appends a message with a timestamp to the log file.
def log(message, file_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    try:
        with open(file_path, "a") as f:
            f.write(log_message)
            f.write("")
    except Exception as e:
        print(f"Error writing to log file: {e}")

