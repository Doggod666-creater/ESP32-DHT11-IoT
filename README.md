![Platform](https://img.shields.io/badge/Platform-ESP32-blue?logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/Protocol-MQTT_3.1.1-orange?logo=eclipse-mosquitto&logoColor=white)
![C++](https://img.shields.io/badge/Language-C%2B%2B-00599C?logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![Arduino](https://img.shields.io/badge/IDE-Arduino-00979D?logo=arduino&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
# ESP32 智能环境监测系统 (IoT)

## 📖 项目简介
本项目基于 ESP32 开发板与 DHT11 温湿度传感器，实现了一套端到端的物联网数据采集与上云系统。设备端通过 MQTT 协议将真实环境数据实时推送至巴法云平台，实现数据的可视化监控。

## 🛠️ 硬件架构与软件栈
- **硬件**：ESP32-WROOM-32 核心板、DHT11 温湿度传感器、面包板及杜邦线。
- **开发环境**：Arduino IDE 2.x、WSL2 (Ubuntu)、Python 3。
- **核心技术**：C/C++ (嵌入式端)、Python (测试脚本)、MQTT 3.1.1 协议、WiFi。

## 🚀 核心功能与排障记录 (面试重点)
1. **数据异常过滤**：针对 DHT11 冷启动易产生 `0.0` 或 `NaN` 脏数据的问题，在代码中增加了有效性判断逻辑，确保上云数据 100% 准确。
2. **网络环境排障**：在初期的 OneNET 平台接入中，遇到 `rc=-2` (连接超时) 报错。通过编写 Python 脚本进行交叉验证 (控制变量法)，定位出校园网/手机热点屏蔽了 1883 及 8883 端口，随后果断切换至巴法云平台 (端口 9501) 成功跑通。
3. **系统稳定性**：实现了 WiFi 断线重连机制与 MQTT 保活机制，设备可长时间稳定在线。
4. - 自动化测试：基于 Python + Pytest 编写 MQTT 接口测试脚本，利用多线程模拟 50 台设备并发压测，自动输出 HTML 测试报告，保证云端接收成功率达 100%。
5. * 基于 Flask 构建后端 API，配合 ECharts 搭建全栈实时监控大屏，支持真实数据实时折线图与超阈值报警

## ⚙️ 如何使用
1. 克隆本仓库代码至本地。
2. 在 `src/esp32_dht11_bemfa.ino` 中填写你自己的 WiFi 账号、密码以及巴法云私钥。
3. 使用 Arduino IDE 编译并烧录至 ESP32。
4. 在巴法云控制台创建主题 `esp32room`，即可实时查看数据。

## 📸 运行效果
- 硬件连线图：见 `hardware_wiring.jpg`
- 串口日志：见 `serial_monitor.png`
