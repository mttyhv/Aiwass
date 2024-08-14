# Sacred Texts Discord Bot

This is a Discord bot that allows users to retrieve and display verses from various texts. The bot supports commands for fetching specific verses, retrieving random verses, searching for terms within texts, and listing available books.

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
    git clone https://github.com/yourusername/sacred-texts-discord-bot.git
    cd sacred-texts-discord-bot
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
