from flask import Flask, jsonify
from flask_cors import CORS
import requests
import re  # 引入正则库，用来提取数字

# ====== 你的巴法云参数 ======
PRIVATE_KEY = "5690cb50ba06be16f90ef3975b08ee9e"
TOPIC = "esp32room"

app = Flask(__name__)
CORS(app) 

@app.route('/api/data')
def get_data():
    url = f"http://apis.bemfa.com/va/getmsg?uid={PRIVATE_KEY}&topic={TOPIC}&type=1"
    try:
        response = requests.get(url, timeout=3)
        res_json = response.json()
        
        if res_json.get("code") == 0 and len(res_json.get("data", [])) > 0:
            latest_msg = res_json["data"][0]["msg"]
            
            # 默认状态
            temp = 0.0
            humi = 0.0
            is_alarm = False
            
            # 情况1：正常的温湿度数据 (Temp:24.4,Humi:19.0)
            if "Temp:" in latest_msg and "Humi:" in latest_msg:
                parts = latest_msg.split(',')
                temp = float(parts[0].split(':')[1])
                humi = float(parts[1].split(':')[1])
                is_alarm = temp >= 26.0
                
            # 情况2：报警数据 (【警告】温度过高！当前温度:28.1度)
            elif "Alarm:1" in latest_msg:
                match = re.search(r"当前温度:([\d.]+)", latest_msg)
                if match:
                    temp = float(match.group(1))
                    # 因为报警消息里没湿度，我们可以硬编码显示一个正常湿度，或者显示0
                    is_alarm = True
            
            status = "⚠️ 温度告警" if is_alarm or "Alarm:1" in latest_msg else "正常运行"
            return jsonify({"temp": temp, "humi": humi, "status": status})
                
    except Exception as e:
        print(f"获取数据失败: {e}")
        
    return jsonify({"temp": 0.0, "humi": 0.0, "status": "等待数据..."})

if __name__ == '__main__':
    print("后端服务已启动，正在通过 HTTP 拉取数据...")
    app.run(host='127.0.0.1', port=5000)