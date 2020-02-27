# EA Account Creator

Automate the EA account creation process as much as possible. You will be asked for a base email (e.g. base@gmail.com) which will be used for all created accounts (e.g. base+woeriuwyrieh@gmail.com), and a username (must be unique). The script will then randomly generate a password, create the account, and store the output to `accounts.txt` for future use.

## Getting Started

These instructions will allow you to run the EA Account Creator tool on your local machine.

### Prerequisites

If using [main.py](./main.py) install the following:

Install Selenium
> ```pip install selenium```

Download Chromedriver to the directory containing `main.py`
> Check your current Chrome version in Chrome by: Menu > Help > About Google Chrome  
> __Note:__ This may prompt your version of chrome to update to the latest.
>
> Download Chromedriver for your Chrome version here: https://chromedriver.chromium.org/downloads

## To-do:
- [x] Automate continuation after captcha completion: class='fc_meta_success_text'
- [ ] Bundle chromedriver and create .exe for Windows machines

## Author
- **Talon Jones** - [taloncjones](https://github.com/taloncjones)

## License
