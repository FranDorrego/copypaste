import os
import json
import requests
import shutil

# Configuración
MAILDIR_BASE = "/data/domains"
WEBHOOK_URL = "https://tu-webhook.com/endpoint"
LIMIT = 50

def get_new_emails():
    emails = []
    for root, dirs, files in os.walk(MAILDIR_BASE):
        if root.endswith("new"):
            for file in files:
                if len(emails) >= LIMIT:
                    return emails
                email_path = os.path.join(root, file)
                emails.append(email_path)
    return emails

def parse_email(email_path):
    with open(email_path, "r", encoding="utf-8") as email_file:
        lines = email_file.readlines()

    headers = {}
    body = []
    in_body = False

    for line in lines:
        if in_body:
            body.append(line.strip())
        elif line == "\n":
            in_body = True
        else:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()

    return {
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "body": "\n".join(body)
    }

def send_emails(emails):
    response = requests.post(WEBHOOK_URL, json=emails)
    return response.status_code == 200

def mark_as_read(email_paths):
    for email_path in email_paths:
        cur_path = email_path.replace("/new/", "/cur/")
        os.makedirs(os.path.dirname(cur_path), exist_ok=True)
        shutil.move(email_path, cur_path)

def main():
    new_emails = get_new_emails()
    if not new_emails:
        print("No hay correos nuevos para procesar.")
        return

    parsed_emails = [parse_email(email) for email in new_emails]
    if send_emails(parsed_emails):
        mark_as_read(new_emails)
        print(f"Se procesaron y enviaron {len(parsed_emails)} correos correctamente.")
    else:
        print("Error al enviar los correos al webhook.")

if __name__ == "__main__":
    main()
