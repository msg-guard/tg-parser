# Telegram Chat Exporter

A Python-based tool for exporting chat history from Telegram channels, groups, and private chats into JSON format.

## 🛠️ Tech Stack

- [Python 3.10+](https://docs.python.org/3/) - High-level programming language with a focus on code readability
- [Telethon](https://docs.telethon.dev/) - Python library to interact with Telegram's API
- [Rich](https://rich.readthedocs.io/) - Library for rich text and beautiful formatting in the terminal
- [aiofiles](https://github.com/Tinche/aiofiles) - Asynchronous file operations
- [asyncio](https://docs.python.org/3/library/asyncio.html) - Library for writing asynchronous code

## 📋 Requirements

- Python 3.10 or higher
- Telegram API credentials (API ID and API Hash)

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd telegram-chat-exporter
   ```

2. **Get Telegram API credentials**

   You'll need to obtain API credentials from Telegram:
    1. Visit https://my.telegram.org/auth
    2. Log in with your phone number
    3. Go to "API development tools"
    4. Create a new application
    5. Note your API ID and API Hash

## 📋 Usage

Export messages from a Telegram chat:

```bash
uv run python -m parser.cli --api_id YOUR_API_ID --api_hash YOUR_API_HASH --chat_id CHAT_ID
```

### Arguments

- `--api_id` - Your Telegram API ID (required)
- `--api_hash` - Your Telegram API Hash (required)
- `--chat_id` - Target chat ID or username to export (required)
- `--limit` - Maximum number of messages to export (optional)

### Chat ID formats

The tool supports various formats for the `chat_id` parameter:

- Username (e.g., `telegram`)
- Numeric ID (e.g., `123456789`)
- Channel ID with -100 prefix (e.g., `-1001234567890`)

## 📊 Output

Exported messages are saved as JSON files with the following naming convention:

```
CHAT_NAME_TIMESTAMP.json
```

The JSON output contains the following fields for each message:

- `id` - Message ID
- `date` - Message timestamp in YYYY-MM-DD HH:MM:SS format
- `sender_id` - Sender's Telegram ID
- `sender_name` - Sender's display name
- `text` - Message content

## 🧪 Development

### Project Structure

```
telegram-chat-exporter/
├── api/               # Telegram API interaction
│   ├── client.py      # Client and message fetching
│   └── entities.py    # Entity resolution utilities
├── models/            # Data models
│   └── message.py     # Message formatting
├── utils/             # Utility functions
│   ├── file.py        # File operations
│   └── logging.py     # Logging configuration
└── cli.py             # Command-line interface
```

### First-time Setup

When running the tool for the first time, you'll need to authenticate with Telegram. The tool will prompt you to enter
the verification code sent to your Telegram account.

After successful authentication, a session file will be created to keep you logged in for future runs.
