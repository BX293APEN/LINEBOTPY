import json, requests

class JapanWeather:

    def __init__(
        self,
        weatherURL = "https://weather.tsukumijima.net/api/forecast/city/",
        areaID = {
            "北海":"016010",
            "青森":"020010",
            "岩手":"030010",
            "秋田":"050010",
            "宮城":"040010",
            "山形":"060010",
            "福島":"070010",
            "茨城":"080010",
            "栃木":"090010",
            "群馬":"100010",
            "千葉":"120010",
            "埼玉":"110010",
            "東京":"130010",
            "神奈川":"140010",
            "新潟":"150010",
            "富山":"160010",
            "石川":"170010",
            "福井":"180010",
            "長野":"200010",
            "岐阜":"210010",
            "山梨":"190010",
            "静岡":"220010",
            "愛知":"230010",
            "滋賀":"250010",
            "三重":"240010",
            "京都":"260010",
            "奈良":"290010",
            "兵庫":"280010",
            "大阪":"270000",
            "和歌山":"300010",
            "鳥取":"310010",
            "島根":"320010",
            "岡山":"330010",
            "広島":"340010",
            "山口":"350020",
            "香川":"370000",
            "徳島":"360010",
            "愛媛":"380010",
            "高知":"390010",
            "福岡":"400010",
            "大分":"440010",
            "宮崎":"450010",
            "佐賀":"410010",
            "長崎":"420010",
            "熊本":"430010",
            "鹿児島":"460010",
            "沖縄":"471010"
        }
    ):
        self.WEATHER_URL    = weatherURL
        self.AREA_ID        = areaID


    def get_weather_data(self, message):
        date_number = 0
        if "明日" in message:
            date_number = 1
        elif "明後日" in message:
            date_number = 2

        if "都" in message:
            prefecture = message.split("都")[0]
        elif "道" in message:
            prefecture = message.split("道")[0]
        elif "府" in message:
            prefecture = message.split("府")[0]
        elif "県" in message:
            prefecture = message.split("県")[0]
        else:
            prefecture = "東京"

        if ("神奈川" in prefecture) or ("和歌山" in prefecture) or ("鹿児島" in prefecture):
            prefecture = prefecture[-3:]
        else:
            prefecture = prefecture[-2:]

        city_id = self.AREA_ID.get(prefecture, "130010")
        url = f"{self.WEATHER_URL}{city_id}"

        weather_json_data = json.loads(requests.get(url).text)
        forecast = weather_json_data["forecasts"][date_number]

        weather_date = forecast["date"]
        weather_title = weather_json_data["title"]

        if date_number == 2:
            weather = forecast["telop"].replace("\u3000", "")
        else:
            weather = forecast["detail"]["weather"].replace("\u3000", "")

        temp_min = forecast["temperature"]["min"]["celsius"]
        temp_max = forecast["temperature"]["max"]["celsius"]
        temp = f"\n最高気温 : {temp_max}℃\n最低気温 : {temp_min}℃"

        rain = forecast["chanceOfRain"]
        chance_of_rain = (
            f"\n{'*' * 5} 降水確率 {'*' * 5}\n"
            f"0時～6時 : {rain['T00_06']}\n"
            f"6時～12時 : {rain['T06_12']}\n"
            f"12時～18時 : {rain['T12_18']}\n"
            f"18時～24時 : {rain['T18_24']}"
        )

        return f"{weather_date}の{weather_title}は{weather}{temp}{chance_of_rain}"
