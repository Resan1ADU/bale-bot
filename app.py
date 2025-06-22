from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "284732595:GJk9LDRWVpJWIszKrGycHvsDndylPJ3dQqlwtaBG"
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# لینک کانال‌ها
channels = {
    "همدلی مردم": {
        "سفید": "https://ble.ir/channel_hamdeli_white",
        "خاکستری": "https://ble.ir/channel_hamdeli_gray"
    },
    "حمایت چهره های داخلی": {
        "سفید": "https://ble.ir/channel_dakheli_white",
        "خاکستری": "https://ble.ir/channel_dakheli_gray"
    },
    "حمایت چهره ها ی خارجی": {
        "سفید": "https://ble.ir/channel_khareji_white",
        "خاکستری": "https://ble.ir/channel_khareji_gray"
    },
    "اصابت ها": {
        "سفید": "https://ble.ir/channel_esabat_white",
        "خاکستری": "https://ble.ir/channel_esabat_gray"
    },
    "تاثیرات ضربات موشکی ایران": {
        "سفید": "https://ble.ir/channel_tasir_white",
        "خاکستری": "https://ble.ir/channel_tasir_gray"
    },
}

user_state = {}

def send_message(chat_id, text, keyboard=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {"keyboard": keyboard, "resize_keyboard": True} if keyboard else {}
    }
    requests.post(f"{API_URL}/sendMessage", json=payload)

@app.route('/', methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message["chat"]["id"]

    if text == "/start":
        send_message(chat_id, 
            "سلام به ربات رسان مدیا خوش اومدی ))\nاین ربات برای مدیریت محتوا است.\nبرای سهولت کار شما می‌تونید از طریق منوی زیر به کانال‌های محتوا دسترسی پیدا کنید",
            keyboard=[["همدلی مردم"], ["حمایت چهره های داخلی"], ["حمایت چهره ها ی خارجی"], ["اصابت ها"], ["تاثیرات ضربات موشکی ایران"]]
        )
        return jsonify({"ok": True})

    elif text in channels:
        user_state[chat_id] = text
        send_message(chat_id, "لطفاً نوع محتوا را انتخاب کنید:", keyboard=[["سفید"], ["خاکستری"]])
        return jsonify({"ok": True})

    elif text in ["سفید", "خاکستری"]:
        topic = user_state.get(chat_id)
        if topic and topic in channels:
            link = channels[topic].get(text)
            if link:
                send_message(chat_id, f"به این کانال مراجعه کنید:\n{link}")
        else:
            send_message(chat_id, "لطفاً ابتدا از منوی اصلی موضوع را انتخاب کنید.")
        return jsonify({"ok": True})

    else:
        send_message(chat_id, "لطفاً از منوی زیر استفاده کنید.")
        return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(port=5000)
