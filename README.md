# Everything Toolbox Guidance

**Language / 语言:**

- [English](README.md) &nbsp; | &nbsp; [中文 Chinese](README_CN.md)

## ☺️ Introduction

- This toolbox contains a miscellaneous collection of tools, including system cleaning, media handling, console effects, and calculating utilities.

- These code are originally written for my personal use. I use it on Ubuntu 22.04 and 24.04 , but most tools (except `.sh`) probably work on other systems as well. If you would like supports for other OS, e.g. Windows, please kindly post an "ISSUE".

## 🧠 Utilities

### Calculator Tools (`calc/`)

#### `calc/curriculum_planning.py`

- **Curriculum Planning Calendar**: Interactive tool for planning course schedules.
- **Schedule Conflict Detection**: Finds all valid course schedules where no time slots conflict.
- **Required/Optional Courses**: Supports both required and optional courses with flexible tutorial selection.
- **Calendar Visualization**: Displays weekly calendars (DAY 1-5) with 7 time slots per day, showing course schedules in ASCII format.

#### `calc/grade_percentile.py`

- **Grade Percentile Calculator**: Computes percentile rank for scores in a truncated normal distribution.
- **Visualization**: Plots the distribution with 5-point bins and marks the user's score position.
- **Customizable Parameters**: Supports custom mean, standard deviation, score, and bounds.

#### `calc/machine_learning.py`

- **Entropy Calculator**: Interactively computes binary entropy for probability values.
- **Partition Entropy**: Computes weighted entropy across partitions (e.g., for decision trees).
- **Cross Entropy Loss**: Implements cross-entropy loss for model evaluation.

#### `calc/hash.py`

- **HMAC Hash**: Maps integers to deterministic 6-digit codes using HMAC-SHA256.

#### `calc/number_systems.py`

- **Interactive number systems**: Menu-driven base, fixed-point, floating-point, BCD, and Gray code conversion in the terminal; enter `x` to go back or exit.
- **Base conversion**: Convert integers or decimals between bases 2, 8, 10, and 16 (non-terminating fractions end with `...`); source and target bases must differ.
- **Fixed point (Ua.b / Qa.b)**: Choose unsigned `U` or two's-complement signed `Q`, then set integer bits `a` and fractional bits `b`; decimal ↔ fixed-point bit patterns (`a+b` binary bits, or hex / `0x`-prefixed hex of the same width).
- **Floating point (IEEE 754 single precision)**: 32-bit layout (1 sign, 8 exponent, 23 fraction); decimal ↔ 32-bit binary or 8-digit hex.
- **Binary coded decimal (8421 BCD)**: Non-negative decimal integers ↔ BCD bit patterns (one 4-bit nibble per decimal digit, 0–9 only); optional spaces or `0b` prefix on input.
- **Gray code**: Binary ↔ reflected Gray code (bit width preserved); input accepts spaces or `0b` prefix.
- **Input validation**: Invalid input is rejected with a retry prompt; after each conversion you can run another.

    ```shell
    python3 calc/number_systems.py
    ```

### Media Tools (`media/`)

#### `media/pdf_handling.py`

- **Merge PDFs**: Guides the user through selecting PDFs from the `input/` directory and merges them into a single file in the `output/` directory.
- **Interactive Selection**: Allows users to select multiple PDFs interactively and merge them in order.

#### `media/para.py`

- **Paragraph Wrapper**: Converts each line of a plain-text file into an HTML `<p>` tag.
- **Blank Lines**: Outputs `<br>` for empty lines instead of wrapping them in `<p>`.
- **Default Output**: If no output file is given, writes to `<input-stem>_paragraphed<suffix>` (e.g. `article.txt` → `article_paragraphed.txt`).

    ```shell
    python3 media/para.py input.txt
    python3 media/para.py input.txt output.html
    ```

### Console Tools (`console/`)

#### `console/console_effect.py`

- **Typing Simulation**: Creates either word-wise or character-wise typewriter-style output with adjustable speed—ideal for CLI storytelling or dramatic logging.

#### `console/scr.sh`

- **Script Logger**: Records terminal sessions using the `script` command.
- **Timestamped Logs**: Saves logs with timestamps and optional comments to `~/logging/` directory.
- **Automatic Naming**: Generates filenames in format `MMdd_HHmm_comment.log`.

#### `console/task_scheduler.py`

- **Script Scheduler**: Runs a list of shell scripts in rotation with a configurable wait interval between runs.

#### `console/task_timer.py`

- **One-Shot Timer**: Waits until a target time today, then runs a shell script once and exits.
- **Required Arguments**: `script_path`, `hour` (0–23), and `minute` (0–59) must be provided on the command line.
- **Already Passed**: If the target time has already passed today, the script logs a message and exits without running.

    ```shell
    python3 console/task_timer.py /path/to/script.sh 3 30
    ```

### System Tools (`sys/`)

#### `sys/clean.sh`

- **System Cleanup**: Interactive system clean-up script for **Ubuntu 22.04**. Can choose to clean:
  - User cache (`~/.cache/*`)
  - System logs older than 7 days
  - APT cache and unnecessary packages
  - Conda cache and unnecessary packages
- **Space Reporting**: Shows how much space was saved by each cleanup operation.

#### `sys/ssh_host.sh`

- **SSH Host Setup**: Configures SSH server on Ubuntu systems.
- **Firewall Configuration**: Sets up UFW firewall rules for SSH access.
- **Secure Mode**: Optional IP-based access restriction for enhanced security.
- **Service Management**: Enables and starts SSH service automatically.

#### `sys/scp-tar.sh`

- **SSH Tar Transfer**: Fast file/directory transfer between local and remote hosts via SSH using tar and gzip compression.
- **Bidirectional**: Supports upload (local → remote) and download (remote → local).
- **Progress Display**: Shows transfer progress when `pv` is installed on the local machine.
- **Flexible Paths**: Supports `server:/path`, `user@server:/path`, and local paths.

#### `sys/check_data_usage.py`

- **Bandwidth Monitor**: Queries the JustMySocks API for bandwidth usage statistics.
- **CSV Logging**: Optionally saves usage records to `sys/output/data_usage.csv`.
- **Environment**: Requires the `CHECK_API` environment variable to be set.

#### `sys/check_pid.sh`

- **Process Inspector**: Displays detailed info for given PIDs (executable, cwd, command, user, parent process tree, elapsed time, etc.).

---

## 🚀 Getting Started

1. Install Python dependencies:

    ```shell
    pip install -r requirements.txt
    ```

2. On Ubuntu, install `pv` for transfer progress in `sys/scp-tar.sh` (optional but recommended):

    ```shell
    sudo apt install pv
    ```

3. Some bash files need to be run as root:

    ```shell
    sudo ./file_name.sh
    ```

## 📋 Requirements

- Python 3.x
- See `requirements.txt` for Python dependencies:
  - PyPDF2
  - scipy
  - matplotlib
- `requests` (for `sys/check_data_usage.py`)
- System packages on Ubuntu:
  - `pv` — transfer progress display for `sys/scp-tar.sh` (`sudo apt install pv`)

## 👤 Author

**Yimeng (Rosalind)**

- GitHub: [@TeenSpirit1107](https://github.com/TeenSpirit1107)
- Email: yimengteng@link.cuhk.edu.cn
