
import json

# Đọc file JSON gốc
with open("C:/Users/thean/Documents/REL_Project/Data/train/train_converted.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Gom lại thành các đoạn hội thoại
conversations = []
current_convo = []

for message in raw_data:
    if message["role"] == "user":
        # Bắt đầu hội thoại mới
        current_convo = [message]
    elif message["role"] == "assistant":
        # Kết thúc hội thoại
        if current_convo:
            current_convo.append(message)
            conversations.append(current_convo)
            current_convo = []

# Ghi lại thành file JSON mới
with open("data_full.json", "w", encoding="utf-8") as f:
    json.dump(conversations, f, indent=2, ensure_ascii=False)
