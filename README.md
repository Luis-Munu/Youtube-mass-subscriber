# Youtube-mass-subscriber
This project automates the subscription process to multiple channels in Youtube using Selenium and Python.

### Installation
 - Clone the repository to your local machine.
 - Install the required packages using pip install -r requirements.txt.
 - Download the appropriate version of the ChromeDriver for your system, [usually from here](https://chromedriver.chromium.org/downloads), and place it in the project directory if the given one does not work.

### Usage
 - Set the language on which the script will work by changing the variable "language" in subscription.py, by default it's set to work on Spanish (es) but english (en) is also valid.
 - Set the URLs you want to subscribe to in urls.txt, by default the tool subscribes to science channels of [PrejudiceNeutrino's list](https://github.com/PrejudiceNeutrino/YouTube_Channels).
 - Run the script by opening a command console and entering ```python subscription.py``` and enter your credentials, the bot will do the rest.

### License
This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the LICENSE file for details.
