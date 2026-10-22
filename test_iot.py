import paho.mqtt.client as mqtt
import time
import threading
import pytest

# ====== 你的巴法云参数 ======
CLIENT_ID = "5690cb50ba06be16f90ef3975b08ee9e"
TOPIC = "esp32room"
SERVER = "bemfa.com"
PORT = 9501

# ====== 测试用例 1：单设备连接测试 ======
def test_single_device_connect():
    """测试单台设备是否能正常连接到MQTT服务器"""
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    try:
        client.connect(SERVER, PORT, 60)
        assert True 
    except Exception as e:
        assert False, f"连接失败: {e}"
    finally:
        client.disconnect()

# ====== 测试用例 2：50台设备并发发送压力测试 ======
def test_concurrent_devices_publish():
    """测试50台模拟设备同时发送数据，验证云端处理能力"""
    success_count = 0
    lock = threading.Lock()

    def simulate_device(device_num):
        nonlocal success_count
        c_id = f"{CLIENT_ID}-{device_num}"
        client = mqtt.Client(client_id=c_id, protocol=mqtt.MQTTv311)
        try:
            client.connect(SERVER, PORT, 10)
            payload = f"【测试设备 {device_num}】Temp:28.5,Humi:60.0"
            client.publish(TOPIC, payload)
            with lock:
                success_count += 1
            client.disconnect()
        except Exception:
            pass

    threads = []
    for i in range(1, 51):
        t = threading.Thread(target=simulate_device, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n并发压测完成，成功发送设备数：{success_count}")
    assert success_count >= 45, "并发测试失败，成功率过低"
