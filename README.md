# Jarvis v5.6-proxy

基于 Tauri + React + Python Flask 的现代化桌面 AI 助手。采用 Sidecar 架构，结合了 Python 强大的后端处理能力和 React 灵动的构建用户界面。

## 🚀 功能特性

- **智能对话**: 支持实时流式响应、Markdown 渲染、代码高亮及 Mermaid 图表显示。
- **记忆系统**: 具备长期记忆存储与检索能力，保持跨会话的上下文连贯性。
- **任务管理**: 集成提醒事项系统，支持自然语言提取和日历视图。
- **提示词管理**: 可创建、编辑和组织自定义系统提示词与模板。
- **多模型支持**: 统一的 LLM 提供层，支持 Gemini、GPT-5、Qwen 等多种模型（通过内部代理 API）。
- **本地优先**: 所有数据存储在本地 SQLite 数据库中，确保隐私与速度。
- **跨平台**: 基于 Tauri 构建，支持 macOS、Windows 和 Linux。

## 🏗 技术架构

Jarvis 采用 **Sidecar 架构**，前端应用管理独立的后端进程：

- **前端**: React 19 SPA，使用 Vite、TypeScript、Mantine UI v8 和 Tailwind CSS 构建。运行在 Tauri v2 webview 中。
- **后端**: Python Flask REST API，运行于 `127.0.0.1:3721`。处理业务逻辑、数据库交互和 LLM 编排。
- **通信**: 标准请求使用 HTTP/REST，实时对话流使用 Server-Sent Events (SSE)。

## 🛠 环境要求

- **Python**: 3.10 或更高版本
- **Node.js**: 18 或更高版本
- **Rust**: 最新稳定版 (通过 [rustup](https://rustup.rs/) 安装)

## ⚡ 快速开始

推荐使用提供的辅助脚本快速启动开发环境：

1.  **克隆仓库**
    ```bash
    git clone https://github.com/ericWanghy/jarvis.git
    cd jarvis
    ```

2.  **配置密钥**
    复制示例环境文件并填入你的 API 密钥：
    ```bash
    cp backend/.env.example backend/.env
    # 使用你喜欢的编辑器编辑 backend/.env
    ```

3.  **启动开发环境**
    ```bash
    ./start_dev.sh
    ```
    该脚本会自动：
    - 创建并配置 Python 虚拟环境
    - 安装后端和前端依赖
    - 同时启动后端服务器和前端应用进入开发模式

## 🔧 手动安装

如果你更喜欢单独运行各组件：

### 后端 (Python/Flask)

1.  进入后端目录：
    ```bash
    cd backend
    ```
2.  创建并激活虚拟环境：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
4.  运行服务器：
    ```bash
    python run.py
    ```
    API 服务将在 `http://127.0.0.1:3721` 启动。

### 前端 (Tauri/React)

1.  进入前端目录：
    ```bash
    cd frontend
    ```
2.  安装依赖：
    ```bash
    npm install
    ```
3.  启动应用：
    ```bash
    npm run tauri dev
    ```

## 📦 构建发布

打包为独立的桌面应用程序：

1.  **构建后端二进制文件**:
    ```bash
    cd backend
    pyinstaller backend.spec
    ```
    这将在 `backend/dist/backend` 生成独立的可执行文件。

2.  **准备前端资源**:
    将生成的后端二进制文件复制到 Tauri 二进制目录：
    ```bash
    # macOS Apple Silicon 示例
    cp backend/dist/backend ../frontend/src-tauri/binaries/backend-aarch64-apple-darwin
    ```
    *注意：请确保二进制文件名与 `tauri.conf.json` 中定义的目标平台后缀匹配。*

3.  **构建应用**:
    ```bash
    cd ../frontend
    npm run tauri build
    ```
    最终的安装包将位于 `frontend/src-tauri/target/release/bundle/`。

## 📂 目录结构

```
jarvis/
├── backend/                 # Python Flask 后端
│   ├── app/
│   │   ├── api/            # REST API 接口
│   │   ├── core/           # 核心逻辑 (Brain, Config, DB)
│   │   ├── models/         # SQLAlchemy 模型
│   │   └── services/       # 业务逻辑服务
│   ├── storage/            # SQLite 数据库
│   └── tests/              # Pytest 测试套件
├── frontend/                # React/Tauri 前端
│   ├── src/
│   │   ├── api/            # API 客户端
│   │   ├── components/     # React 组件
│   │   ├── context/        # 全局状态
│   │   └── src-tauri/      # Rust Tauri 配置
└── start_dev.sh            # 开发辅助脚本
```

## 🤝 贡献指南

1.  遵循 `CLAUDE.md` 中的编码规范。
2.  确保所有测试通过 (`pytest` 用于后端)。
3.  使用 `ruff` 和 `mypy` 进行 Python 代码检查和类型检查。
4.  前端代码使用 `prettier` 格式化。

## 📄 许可证

[MIT](LICENSE)
