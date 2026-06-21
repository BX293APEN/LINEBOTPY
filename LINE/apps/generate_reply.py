import json, random, csv
from .weather import JapanWeather
class GenerateReply:
    def __init__(self, replyFile = "replyword.json", emotionFile = "emotion.csv"):
        with open(replyFile, "r", encoding="UTF-8") as rf:
            self.reply_data = json.loads(rf.read())
        
        with open(emotionFile, "r", encoding="UTF-8", newline="") as ef: # CSVの改行変換はモジュールに任せる
            self.emotion = list(csv.reader(ef))
        
        self.weather = JapanWeather()

    def classify_message(self, message):

        # 逆接削除（1回目）
        for word in self.reply_data["keyWords"]["nevertheless"]:
            if word in message:
                message = message.split(word)[-1]

        if message == "":
            return "callme"

        for word in self.reply_data["keyWords"]["askName"]:
            if word in message:
                for fp in self.reply_data["keyWords"]["firstPerson"]:
                    if fp in message:
                        return "callyou"
                return "私は、ユウって名前だよ！\nよろしくね！！"

        # 逆接削除（2回目、GAS原文どおり重複している）
        for word in self.reply_data["keyWords"]["nevertheless"]:
            if word in message:
                message = message.split(word)[-1]


        for row in self.emotion:
            if row[0] in message:
                return row[1]

        for word in self.reply_data["keyWords"]["callYuu"]:
            if word in message:
                return "callme"

        for word in self.reply_data["keyWords"]["ansChar"]:
            if word in message:
                return "imp"

        for word in self.reply_data["keyWords"]["question"]:
            if word in message:
                return "callpen"

        return "notfound"
    
    def generate_message(self, message):
        reply_mean = self.classify_message(message)

        if reply_mean == "notfound":
            return "私、Botだから分かんないや"

        elif reply_mean == "callme":
            return "何？"

        elif reply_mean == "callpen":
            return "私、Botだから分かんないや\n管理者のPENに聞いて"

        elif reply_mean in ("usecmd", "lock", "chgun", "fav", "callyou", "help", "events"):
            return "その機能は未実装です"

        elif reply_mean in ("happy", "compli", "surp", "sad", "simoneta", "hukai", "adv", "ohayo"):
            # surp未生成
            choices = self.reply_data[reply_mean]
            return random.choice(choices)

        elif reply_mean == "health":
            return "元気だよ！ありがと(*´ω｀*)〜♪"

        elif reply_mean == "weather":
            return self.weather.get_weather_data(message)

        elif reply_mean in ("prof", "profen"):
            return self.reply_data[reply_mean]

        elif reply_mean == "おやすみ":
            return "おやすみzzz..."

        elif reply_mean == "おかえり":
            return "ただいま"

        elif reply_mean == "ただいま":
            return "おかえり"

        elif reply_mean == "ありがと":
            return "どういたしまして(*´ω｀*)〜♪"

        elif reply_mean in ("どうした", "どした"):
            return "反応しただけだよ"

        elif reply_mean == "imp":
            return "ありがと(*´ω｀*)〜♪"

        else:
            # self.emotion.csv からそのまま返ってきた固定文言など
            return reply_mean

