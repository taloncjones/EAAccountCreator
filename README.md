# EA Account Creator

Automate the EA account creation process as much as possible. You will need to provide a gmail account and an app-specific password in an emailCredentials JSON file - this gmail account will be used as the base email address for all generated EA accounts. This script will use that base email address to randomly generate passwords, usernames, and push the output to a given Google Sheet for retrieval.

You'll need to setup an app-specific password for the given gmail account, create a Google Sheet and associated automation account with edit access to that sheet, and install the Chromedriver for your version of Chrome.

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



#### Setup Google Account

@Talon is going to fill this out with screenshots and step by step process



#### Usage

```
usage: main.py [-h] [--noop]
               driverType driverPath keyFile gsheetURL emailCredentials

positional arguments:
  driverType        Provide the type of selenium driver for this run e.g.
                    chrome
  driverPath        Provide the path of the selenium driver you'll use
  keyFile           Provide the generic account's key file that has Edit
                    access to the following GSheet
  gsheetURL         Provide the Google Sheet URL where account details will be
                    appended
  emailCredentials  Provide the email app's credentials to access and read
                    email

optional arguments:
  -h, --help        show this help message and exit
  --noop            Provide flag --noop if you want the operation to be a no-
                    op
```



#### Authors

* Talon Jones - [taloncjones](https://github.com/taloncjones) 



#### License 

This project is licensed under the [GNU General Public License v3.0](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.
