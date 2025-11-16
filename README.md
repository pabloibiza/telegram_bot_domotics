# Telegram Bot Domotics

A simple Telegram bot for home automation (domotics) that measures temperature and pressure using a BMP085 sensor. It allows users to interact via Telegram commands.

Future features: MQTT integration for controlling devices.

## Requirements

- Python 3
- Telegram bot token from BotFather
- Adafruit BMP085 sensor connected (e.g., via I2C)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pabloibiza/telegram_bot_domotics.git
   cd telegram_bot_domotics
   ```

2. Install dependencies:
   ```bash
   pip install pyTelegramBotAPI Adafruit-BMP085
   ```

3. Edit `telegram_bot.py` and set your `BOT_TOKEN` and `DEVELOPER_PASSWORD`.

## Usage

Run the bot:
```bash
python telegram_bot.py
```

Send commands to the bot in Telegram.

## Commands

- `hello`: Greeting
- `help`: Show help
- `temperature`: Get temperature in °C
- `pressure`: Get pressure in mbar
- `developer`: Enter developer mode (requires password)
- `logout`: Exit developer mode
- `log`: Send log file (developer only)

## License

MIT