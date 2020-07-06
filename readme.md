# Prince

Prince is a simple discord bot to facilitate card games over discord.


## Installation
0. Create a bot on discord. Instructions [here.](https://discordpy.readthedocs.io/en/latest/discord.html)

1. Download and install python, if you don't already have it. You can get it [here.](https://www.python.org/downloads/)

2. Open terminal or command prompt (depending on your operating system) and`cd` into the directory (folder) you're planning on using.

3. Clone (ie download) the code.

4. Install the dependencies.
    1. You may need to install Visual C++ 14.0. Get it here [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
    ```bash
    pip install -r requirements.txt
    ```
5. Edit `config-template.json` for your values, and rename it to `config.json`

6. Run `python3 src/main.py`

7. Invite the bot to your server with the following permissions:
    1. View channels
    2. Send Messages
    3. Read Message History

## Usage
`!draw` - Draw the next card off the deck.
`!createdeck` - Create a new deck in this channel.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Any contributors wave any copyrights to the repository owner, to the extent possible by applicable law.

Software is provided ​“AS IS”. ExtraE113 makes no other warranties, express or implied, and hereby disclaims all implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose, to the extent possible by applicable law.