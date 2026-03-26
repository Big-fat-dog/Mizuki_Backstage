# 🚀 Mizuki Backstage - 极速启动的智能后端服务

基于 FastAPI 打造的高性能后端，集成自动浏览器启动功能，让本地上传文章至github仓库体验如丝般顺滑！✨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/) [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 💡 为什么选择 Mizuki Backstage？

厌倦了手动修改文件来上传文章之博客？Mizuki Backstage专为**高效开发**而生：

- ⚡ **秒级启动**：运行即服务，无需等待。
- 🌐 **自动唤醒**：执行命令后自动打开浏览器直达界面，告别手动输入 `localhost`。
- 🛠️ **现代架构**：基于业界最快的 Python 框架 **FastAPI**，异步高性能。
- 🎨 **前后端分离**：清晰的文件结构，方便后续扩展 Vue/React 前端。

---

## 🎬 快速开始**(5 分钟上手)**

### 一、获取代码
首先，将项目克隆到本地：

```
git clone https://github.com/<你的用户名>/mizuki_backend.git
cd mizuki_backend
```

### 二、创建并激活虚拟环境 (推荐 ⭐)
为了隔离依赖，避免污染全局环境，强烈建议使用虚拟环境。

Windows (PowerShell):

```
python -m venv venv
.\venv\Scripts\activate
```

macOS / Linux:

```
python3 -m venv venv
source venv/bin/activate
```

💡 **成功标志**：命令行前出现 `(venv)` 字样。

### 三、**安装依赖**

使用锁定的依赖文件进行安装：

```
pip install -r requirements.txt
```

### 四、配置环境变量
本项目需要读取 .env 文件来获取 GitHub Token 等配置。

复制模板

```
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

编辑 .env 文件：
用文本编辑器打开 .env，填入你的真实信息：

```
# GitHub 个人访问令牌 (需勾选 repo 权限)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 目标仓库信息
REPO_NAME=你的仓库名
BRANCH_NAME=main
CONTENT_PATH=src/content/posts
```

如何获取 Token？
前往 GitHub Settings -> Developer settings -> Generate new token (classic)，勾选 repo 范围，生成后复制粘贴。

### 五、**启动服务**

一切就绪！运行主程序：

```
python main.py
```

🎉 **见证奇迹**：

- 终端将显示服务器启动日志。
- **系统会自动弹出默认浏览器**，直达 `http://127.0.0.1:8000`！

🛠️ 技术栈
Backend: FastAPI - 现代、高性能 Web 框架
Server: Uvicorn - 闪电般的 ASGI 服务器
Env Management: python-dotenv - 环境变量加载
Language: Python 3.8+

Made with ❤️ by Fatdog