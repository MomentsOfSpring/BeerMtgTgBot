# 🍺 Beer MTG Bot 🍺

A Telegram bot for organizing weekly MTG meetups. 
The bot helps manage polls, table reservations, and participant notifications.
Special VLADOSTAS feature for your friends


## Features

- Automatic weekly poll creation
- Participant vote tracking
- Automatic table count calculation
- Bartender reservation notifications
- New member management
- Automatic group rules delivery
- Task scheduler for automation


## Technologies

- Python 3.9.13
- pyTelegramBotAPI
- APScheduler


## Requirements

- Python 3.8 or higher
- Python package manager
- Telegram Bot Token
- Telegram ID's


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/beer_bot.git
cd beer_bot
```

2. Create and activate a virtual environment:
```bash
# From the project root directory
python -m venv .venv
source .venv/bin/activate  # for Linux/Mac
# or
.venv\Scripts\activate  # for Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add:
```
BOT_TOKEN = "your_telegram_bot_token"
```


## Configuration

Main settings are located in `bot/config.py`:
- `TOKEN` - Telegram Bot token (@botfather)
- `MAGIC_CHAT_ID` - Group-Chat Telegram ID
- `BOSS` - MAIN Administrator ID
- `BARTENDER` - Bartender ID
- `VLADA`, `STAS` - Your friend user ID


## Usage

### Bot Commands

#### Main commands:
- `/start` or `/help` - show help
- `/invite` - get invite link
- `/rules` - show group rules

#### Manual start commands:
- `/pollnow` - manually start poll
- `/pollres` - get poll results
- `/gameon` - manually trigger notification (and unpin all polls)


### Automatic Features

- Weekly poll creation
- Bartender notifications for reserve
- Table count calculation
- "Beer Love" Test for new members


## 📁 Project Structure

```
beerbot/
├── bot/
│   ├── bot.py           # Main bot file (start here)
│   ├── bot_instance.py  # Bot initialization
│   ├── config.py        # Configuration
│   ├── handlers.py      # Command handlers
│   ├── callbacks.py     # Callback handlers
│   ├── commands.py      # Bot commands
│   ├── polls.py         # Poll logic
│   ├── common.py        # Common functions
│   └── vlada_utils.py   # VLADA utilities
├── img/                 # Images
├── text/               # Text files
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Authors

- [@MomentsOfSpring](https://github.com/MomentsOfSpring)

