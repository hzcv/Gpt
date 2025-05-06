from instagrapi import Client
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASS")
OWNER_USERNAMES = ["your_username"]  # users to ignore

# Login
cl = Client()
cl.login(USERNAME, PASSWORD)

print(f"✅ Logged in as {USERNAME}")

# Store last message IDs to avoid duplicate replies
replied_messages = set()

while True:
    try:
        threads = cl.direct_threads(amount=10)
        for thread in threads:
            if not thread.is_group:
                continue

            messages = cl.direct_messages(thread.id, amount=5)
            for message in reversed(messages):  # oldest to newest
                if message.id in replied_messages:
                    continue

                sender = message.user.username
                if sender == USERNAME or sender in OWNER_USERNAMES:
                    continue

                # Custom reply
                reply1 = f"@{sender} Oy msg mt kr yrr"
                cl.direct_send(reply1, thread_ids=[thread.id])
                print(f"🗯️ Sent custom reply to {sender} in '{thread.title}'")

                time.sleep(1)

                # Affiliate+ API reply
                url = f"https://api.affiliateplus.xyz/api/chatbot?message={requests.utils.quote(message.text)}&botname={USERNAME}&ownername=Diwas Atreya"
                res = requests.get(url).json()
                if "message" in res:
                    cl.direct_send(res["message"], thread_ids=[thread.id])
                    print(f"🤖 Sent bot reply: {res['message']}")

                replied_messages.add(message.id)
                time.sleep(2)

        time.sleep(10)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(15)
