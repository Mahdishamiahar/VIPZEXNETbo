import threading
import time
import queue

class Message:
    def __init__(self, author_guid, text):
        self.author_guid = author_guid
        self.text = text

class Robot:
    def __init__(self, token):
        self.token = token
        self.handlers = []
        self.message_queue = queue.Queue()
        self.running = False

    def on_message(self, func):
        """
        ثبت هندلر پیام جدید
        """
        self.handlers.append(func)
        return func

    def send_message(self, user_guid, text, inline_buttons=None):
        """
        ارسال پیام به کاربر
        اینجا فقط برای تست چاپ می‌شود، در نسخه واقعی باید به API متصل شود
        """
        print(f"[ارسال پیام] به کاربر {user_guid}: {text}")
        if inline_buttons:
            print(f"  دکمه‌های تعاملی: {inline_buttons}")

    def _simulate_receiving_messages(self):
        """
        شبیه‌سازی دریافت پیام (برای تست بدون API واقعی)
        """
        test_messages = [
            Message("user123", "/start"),
            Message("user123", "سلام"),
            Message("user456", "/start"),
            Message("user456", "دستور نامشخص"),
        ]

        for msg in test_messages:
            self.message_queue.put(msg)
            time.sleep(1)  # شبیه‌سازی فاصله زمانی دریافت پیام‌ها

    def _message_loop(self):
        """
        حلقه اصلی دریافت پیام‌ها و اجرای هندلرها
        """
        while self.running:
            try:
                msg = self.message_queue.get(timeout=1)
            except queue.Empty:
                continue

            msg_dict = {
                'author_guid': msg.author_guid,
                'text': msg.text
            }

            for handler in self.handlers:
                try:
                    handler(msg_dict)
                except Exception as e:
                    print(f"خطا در هندلر پیام: {e}")

    def run(self):
        """
        شروع ربات و اجرای حلقه دریافت پیام‌ها
        """
        self.running = True

        # اجرای شبیه‌سازی دریافت پیام‌ها در ترد جداگانه
        threading.Thread(target=self._simulate_receiving_messages, daemon=True).start()

        print("ربات در حال اجرا است...")

        self._message_loop()