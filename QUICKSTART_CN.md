# 快速开始指南 - Kimi 研究助手

## 🚀 5分钟上手

### 1. 获取 API Key

访问 [Moonshot 控制台](https://platform.moonshot.cn/console/api-keys) 获取你的 API 密钥

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 API key
# 使用任何文本编辑器打开 .env
nano .env  # 或 vim .env 或其他编辑器
```

在 `.env` 文件中设置：
```bash
MOONSHOT_API_KEY=sk-your-actual-api-key-here
```

### 3. 安装依赖

```bash
# 推荐使用 uv（更快）
uv sync

# 或使用传统 pip
pip install openai python-dotenv
```

### 4. 运行研究助手

```bash
# 使用 uv
uv run research_agent/agent_kimi.py

# 或使用 python
python research_agent/agent_kimi.py
```

## 💡 使用示例

启动后，尝试这些查询：

```
研究2025年人工智能的最新进展

分析电动汽车市场的现状和未来趋势

Research quantum computing developments in 2025

What are the latest trends in renewable energy?
```

## 📁 查看结果

研究完成后，查看以下目录：

- `files/research_notes/` - 各个子主题的研究笔记
- `files/reports/` - 最终综合报告
- `logs/` - 会话记录和日志

## ⚙️ 工作原理

```
你的问题 → Kimi分解主题 → 联网搜索 → 保存笔记 → 生成报告
```

1. **主题分解**：AI 将你的问题分解为 2-4 个子主题
2. **联网搜索**：对每个子主题进行深度网络搜索
3. **保存笔记**：将研究发现保存到 markdown 文件
4. **生成报告**：综合所有发现，生成专业报告

## 🔧 常见问题

### API Key 错误
```
Error: MOONSHOT_API_KEY not found
```
**解决方案**：检查 `.env` 文件是否存在且正确设置了 API key

### 网络连接错误
```
Error: Connection timeout
```
**解决方案**：
1. 检查网络连接
2. 确认能访问 `api.moonshot.cn`
3. 如在国内，确保网络正常

### 模块未找到
```
ModuleNotFoundError: No module named 'openai'
```
**解决方案**：运行 `uv sync` 或 `pip install openai python-dotenv`

## 📊 API 使用说明

### 支持的模型
- `moonshot-v1-auto` - 自动选择最佳模型，支持联网搜索（推荐）
- `moonshot-v1-8k` - 8K 上下文窗口
- `moonshot-v1-32k` - 32K 上下文窗口
- `moonshot-v1-128k` - 128K 上下文窗口

### 修改模型
编辑 `research_agent/agent_kimi.py` 第 23 行：
```python
def __init__(self, api_key: str, model: str = "moonshot-v1-auto"):
```

## 🎯 高级用法

### 编程调用

```python
from research_agent.agent_kimi import KimiResearchAgent
import os

# 初始化
agent = KimiResearchAgent(
    api_key=os.environ.get("MOONSHOT_API_KEY")
)

# 执行研究
agent.process_research_request("研究区块链技术的应用")
```

### 自定义研究流程

```python
# 手动控制研究步骤
agent = KimiResearchAgent(api_key="your-key")

# 1. 研究特定子主题
results = agent.research_topic(
    topic="人工智能发展",
    subtopics=["大语言模型", "计算机视觉", "强化学习"]
)

# 2. 生成报告
report_path = agent.generate_report("人工智能发展")
print(f"报告保存在: {report_path}")
```

## 💰 费用说明

Kimi API 按 token 计费，价格相对实惠：
- 输入：约 ¥0.012 / 1K tokens
- 输出：约 ¥0.012 / 1K tokens

一次完整研究（包含联网搜索和报告生成）通常消耗 10K-50K tokens，费用约 ¥0.12-0.60。

## 🆚 版本对比

| 特性 | Kimi 版本 | Claude 版本 |
|------|----------|------------|
| 联网搜索 | ✓ 内置 | ✓ WebSearch工具 |
| 多代理 | 顺序执行 | 并行执行 |
| 中文支持 | ✓ 优秀 | 一般 |
| API费用 | 较低 | 较高 |
| 配置难度 | 简单 | 复杂 |

## 📞 获取帮助

- **API问题**：访问 [Moonshot平台](https://platform.moonshot.cn)
- **代码问题**：在 GitHub 提交 issue

## 🎉 开始研究吧！

现在你已经准备好了，开始使用 Kimi 研究助手探索任何你感兴趣的主题！
