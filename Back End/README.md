**本目录为后端源代码，包括Flask、关键帧提取、人脸区域检测、换脸检测模型**

## 环境

------

- Python  3.6
- MySQL 5.7
- Windows 10

## 相关依赖

------

详见 requirements.txt

## 目录结构

------

```bash
├── cache                      # 上传文件缓冲区
├── classification             # 换脸检测模型目录
├── compression_detection      # 视频画质检测目录
├── image                      # 快速检测结果目录
├── result                     # 深度检测结果目录
│── screenshot                 # 采集网页快照目录
├── utils                      # 后端利用工具目录
├── video                      # 采集网站视频目录
├── db_config.py               # 数据库配置
├── exts.py                    # Flask模型层中间件
├── main.py                    # Flask主程序
├── models.py                  # 模型层定义
├── setting.py                 # 全局常量定义
├── requirements.txt           # 相关依赖
└── openh264-1.7.0-win64.dll   # OpenCV依赖
```

## 启动方法

------

### 1.	安装依赖

```bash
pip install -r requirements.txt
```

### 2.	安装FFmpeg

详见 http://ffmpeg.org/

### 3.	配置db_config.py

### 4.	启动项目

```bash
python main runserver -r -d --threaded
```