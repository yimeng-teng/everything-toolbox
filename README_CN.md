# Everything Toolbox 使用手册

**Language / 语言:**

- [English](README.md) &nbsp; | &nbsp; [中文 Chinese](README_CN.md)

## ☺️ 简介

- 本工具箱包含多种工具，包括系统清理、媒体处理、控制台特效和计算实用程序，功能杂项齐全。

- 这些代码最初是为我个人使用而编写。我在 Ubuntu 22.04 和 24.04 上使用，但除 `.sh` 脚本外，大多数工具也应该适用于其他系统。如果你希望支持其他操作系统（如 Windows），欢迎通过 ISSUE 反馈。

## 🧠 工具

### 计算工具 (`calc/`)

#### `calc/curriculum_planning.py`

- **课程规划日历**：用于规划课程表的交互式工具。
- **时间冲突检测**：查找所有没有时间冲突的有效课程安排。
- **必修/选修课程**：支持必修和选修课程，具有灵活的教程选择。
- **日历可视化**：以 ASCII 格式显示每周日历（DAY 1-5），每天有 7 个时间段，显示课程安排。

#### `calc/grade_percentile.py`

- **成绩百分位计算器**：计算截断正态分布中分数的百分位排名。
- **可视化**：绘制分布图，使用 5 分区间并标记用户的分数位置。
- **可自定义参数**：支持自定义均值、标准差、分数和边界。

#### `calc/machine_learning.py`

- **熵计算器**：交互式计算概率值的二进制熵。
- **分区熵**：计算跨分区的加权熵（例如，用于决策树）。
- **交叉熵损失**：实现用于模型评估的交叉熵损失。

#### `calc/hash.py`

- **HMAC 哈希**：使用 HMAC-SHA256 将整数映射为确定性的 6 位数字码。

#### `calc/number_systems.py`

- **交互式数制工具**：在终端中选择进制转换、定点、浮点、BCD 或 Gray 码转换；输入 `x` 可返回上一级或退出。
- **进制转换**：在 2 / 8 / 10 / 16 之间互转整数或小数（非终止小数以 `...` 结尾）；源进制与目标进制不能相同。
- **定点（Ua.b / Qa.b）**：先选无符号 `U` 或补码有符号 `Q`，再输入整数位 `a` 与小数位 `b`；支持十进制 ↔ 定点位串（`a+b` 位二进制，或对应长度十六进制 / `0x` 前缀）。
- **浮点（IEEE 754 单精度）**：32 位（1 符号 + 8 指数 + 23 尾数）；支持十进制 ↔ 32 位二进制或 8 位十六进制表示。
- **二进制编码的十进制（8421 BCD）**：非负十进制整数 ↔ BCD 位串（每位十进制数字占 4 位，nibble 仅允许 0–9）；输入可含空格或 `0b` 前缀。
- **Gray 码（反射二进制）**：二进制 ↔ Gray 码（位宽保持不变）；输入可含空格或 `0b` 前缀。
- **输入校验**：非法输入会提示并重试；完成一次转换后可继续下一次。

    ```shell
    python3 calc/number_systems.py
    ```

### 媒体工具 (`media/`)

#### `media/pdf_handling.py`

- **合并 PDF**：引导用户从 `input/` 目录中选择 PDF 文件，并将它们合并到 `output/` 目录中的单个文件。
- **交互式选择**：允许用户交互式选择多个 PDF 并按顺序合并它们。

#### `media/para.py`

- **段落包装**：将纯文本文件的每一行转换为 HTML `<p>` 标签。
- **空行处理**：空行输出 `<br>`，而不是包在空的 `<p>` 标签中。
- **默认输出**：未指定输出文件时，写入 `<输入文件名>_paragraphed.<扩展名>`（例如 `article.txt` → `article_paragraphed.txt`）。

    ```shell
    python3 media/para.py input.txt
    python3 media/para.py input.txt output.html
    ```

### 控制台工具 (`console/`)

#### `console/console_effect.py`

- **打字效果**：创建逐词或逐字符的打字机风格输出，速度可调——非常适合 CLI 故事叙述或戏剧性日志记录。

#### `console/scr.sh`

- **脚本记录器**：使用 `script` 命令记录终端会话。
- **带时间戳的日志**：将带时间戳和可选注释的日志保存到 `~/logging/` 目录。
- **自动命名**：生成格式为 `MMdd_HHmm_comment.log` 的文件名。

#### `console/task_scheduler.py`

- **脚本调度器**：按列表循环运行 shell 脚本，每次运行后可配置等待间隔。

#### `console/task_timer.py`

- **单次定时器**：等待到今天的指定时刻，执行一次 shell 脚本后退出。
- **必填参数**：命令行必须提供 `script_path`、`hour`（0–23）和 `minute`（0–59）。
- **时间已过**：若今天的目标时刻已过，脚本会记录提示并退出，不执行目标脚本。

    ```shell
    python3 console/task_timer.py /path/to/script.sh 3 30
    ```

### 系统工具 (`sys/`)

#### `sys/clean.sh`

- **系统清理**：适用于 **Ubuntu 22.04** 的交互式系统清理脚本。可以选择清理：
  - 用户缓存 (`~/.cache/*`)
  - 超过 7 天的系统日志
  - APT 缓存和不必要的包
  - Conda 缓存和不必要的包
- **空间报告**：显示每次清理操作节省了多少空间。

#### `sys/ssh_host.sh`

- **SSH 主机设置**：在 Ubuntu 系统上配置 SSH 服务器。
- **防火墙配置**：为 SSH 访问设置 UFW 防火墙规则。
- **安全模式**：可选的基于 IP 的访问限制，以增强安全性。
- **服务管理**：自动启用并启动 SSH 服务。

#### `sys/scp-tar.sh`

- **SSH 压缩传输**：通过 SSH 使用 tar 和 gzip 压缩，在本地与远程主机之间快速传输文件或目录。
- **双向传输**：支持上传（本地 → 远程）和下载（远程 → 本地）。
- **进度显示**：在本地安装 `pv` 后可显示传输进度。
- **灵活路径**：支持 `server:/path`、`user@server:/path` 和本地路径。

#### `sys/check_data_usage.py`

- **带宽监控**：查询 JustMySocks API 获取带宽使用统计。
- **CSV 记录**：可选择将使用记录保存到 `sys/output/data_usage.csv`。
- **环境变量**：需要设置 `CHECK_API` 环境变量。

#### `sys/check_pid.sh`

- **进程检查器**：显示指定 PID 的详细信息（可执行文件、工作目录、命令、用户、父进程树、运行时长等）。

---

## 🚀 开始使用

1. 安装 Python 依赖项：

    ```shell
    pip install -r requirements.txt
    ```

2. 在 Ubuntu 上安装 `pv`，用于 `sys/scp-tar.sh` 的传输进度显示（可选但推荐）：

    ```shell
    sudo apt install pv
    ```

3. 某些 bash 文件需要以 root 权限运行：

    ```shell
    sudo ./file_name.sh
    ```

## 📋 要求

- Python 3.x
- 查看 `requirements.txt` 了解 Python 依赖项：
  - PyPDF2
  - scipy
  - matplotlib
- `requests`（用于 `sys/check_data_usage.py`）
- Ubuntu 系统包：
  - `pv` — `sys/scp-tar.sh` 的传输进度显示（`sudo apt install pv`）

## 👤 作者

**Yimeng (Rosalind)**

- GitHub: [@TeenSpirit1107](https://github.com/TeenSpirit1107)
- 邮箱: yimengteng@link.cuhk.edu.cn

