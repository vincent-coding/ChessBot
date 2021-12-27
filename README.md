# ChessBot
A bot to play chess for you on [chess.com](https://chess.com/)

## DISCLAIMER
This bot has been coded for purely educational purposes and not for any nefarious purpose, or for the purpose of harming anyone.<br />
I am not responsible, nor do I take responsibility for the consequences of the use of this bot and code by anyone.

**WARNING**: This bot may result in the suspension of your chess.com account. So use it at your own risk. I will not be held responsible in any way.

## How does it work?
The bot uses [selenium](https://www.selenium.dev/) to control the browser. For the chess part the bot uses the open-source engine [Stockfish](https://github.com/official-stockfish/Stockfish).

## Prerequisites
To use the bot properly you need the following software:
- Python 3.6 or higher
- Stockfish 
- Gecko Driver
You can see the configuration with which I developed the bot in the **[Additional information](https://github.com/vincent-coding/ChessBot#additional-information)** section.

## How to install
Just open a terminal and do:
```
git clone https://github.com/vincent-coding/ChessBot
```
Enter in the folder then created then edit the file .env (it is the file which contains the configuration of the bot)
```
USERNAME  = <Your chess.com username (NOT YOUR EMAIL)>
PASSWORD  = <Your chess.com password>
STOCKFISH = <The path to the stockfish binary file>
RUN_COUNT = <The number of games the bot will play before stopping>

THREAD_COUNT = <The number of threads used to perform the calculations>
DEPTH        = 10
```
Once this is done, all that remains is to install the modules necessary for the bot to function properly.
```
pip3 install -r requirements.txt
```
Launch the bot, 
```
python3 ChessBot.py
```
**and let the magic happen**.

### Additional information
Develop and test with:
```
Python 3.9.9
Stockfish 14.1 - Linux x64
Gecko Driver (0.30.0)
```
