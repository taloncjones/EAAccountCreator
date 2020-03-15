# EA Account Creator

Automate the EA account creation process as much as possible. You will be asked for a base email (e.g. base@gmail.com) which will be used for all created accounts (e.g. base+woeriuwyrieh@gmail.com), and a username (must be unique). The script will then randomly generate a password, create the account, and push the output to a given Google Sheet.

#### Installation

Download Chromedriver to the directory containing `main.py`
> Check your current Chrome version in Chrome by: Menu > Help > About Google Chrome  
> __Note:__ This may prompt your version of chrome to update to the latest.
>
> Download Chromedriver for your Chrome version here: https://chromedriver.chromium.org/downloads



Install required packages:

```
pip install -r requirements.txt
```



#### Usage

```
usage: main.py [-h] [--noop] baseEmail driverType driverPath keyFile gsheetURL

positional arguments:
  baseEmail   Provide the base email address from which others will be
              generated
  driverType  Provide the type of selenium driver for this run e.g. chrome
  driverPath  Provide the path of the selenium driver you'll use
  keyFile     Provide the generic account's key file that has Edit access to
              the following GSheet
  gsheetURL   Provide the Google Sheet URL where account details will be
              appended

optional arguments:
  -h, --help  show this help message and exit
  --noop      Provide flag --noop if you want the operation to be a no-op,
              meaning it won't actually connect to Adobe Analytics to pull
              fresh data, but will run all other functions.
```



#### Authors

* Talon Jones - [taloncjones](https://github.com/taloncjones) 



#### License 

This project is licensed under the [GNU General Public License v3.0](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.
