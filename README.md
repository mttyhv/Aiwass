# Sacred Texts Discord Bot

This is a Discord bot that allows users to retrieve and display verses from various sacred texts. The bot supports commands for fetching specific verses, retrieving random verses, searching for terms within texts, and listing available books.

## Features

- **Fetch Specific Verse:** Retrieve a specific verse from a book by specifying the book name, language, chapter, and verse.
- **Random Verse:** Fetch a random verse from a specified book and language.
- **Search Verses:** Search for specific keywords within a book and retrieve all verses containing those terms.
- **List Available Books:** Display information about all available books in the database.

## Setup

### Prerequisites

- Python 3.8 or higher
- `discord.py` library
- `python-dotenv` library

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mttyhv/Aiwass.git
    cd Aiwass
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root and add your Discord bot token:
    ```
    DISCORD_TOKEN=your_discord_bot_token
    ```

4. Prepare the `sacred_texts.json` file in the following structure:
    ```json
    {
        "Book Name": {
            "code": "Some Code",
            "class": "Some Class",
            "author": "Author Name",
            "year": "Year of Publication",
            "description": "Brief description of the book",
            "versions": {
                "Version Name": {
                    "link": "URL to the version",
                    "verses": {
                        "Chapter Number": {
                            "Verse Number": "Verse Text"
                        }
                    }
                }
            }
        }
    }
    ```

### Running the Bot

To start the bot, run:

```bash
python aiwass.py
```

The bot will connect to Discord and be ready to accept commands.

## Commands

### `/verse`
Retrieve a specific verse from a book.

- **Arguments:**
  - `book`: Name of the book.
  - `language`: Language version of the book.
  - `chapter`: Chapter number.
  - `verse`: Verse number.

### `/random`
Retrieve a random verse from a specified book and language.

- **Arguments:**
  - `book`: Name of the book.
  - `language`: Language version of the book.

### `/search`
Search for specific keywords within a book.

- **Arguments:**
  - `book`: Name of the book.
  - `language`: Language version of the book.
  - `keywords`: Keywords to search for.

### `/books`
Display information about all available books in the database.

## Logging

The bot logs all user interactions in a `logs.log` file. Each log entry includes the user, command, arguments, and the output generated by the bot.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss the changes you'd like to make.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py) - The Python framework for interacting with the Discord API.
- [dotenv](https://pypi.org/project/python-dotenv/) - For managing environment variables.
```

### Instructions for Use
1. Replace `yourusername` in the clone command with your actual GitHub username.
2. Include the `requirements.txt` file that lists the necessary Python packages (`discord.py` and `python-dotenv`, for example).
3. Create and upload your `sacred_texts.json` file to the repository or provide instructions on how it can be created.

This `README.md` should provide enough information for others to understand, set up, and contribute to the project.
