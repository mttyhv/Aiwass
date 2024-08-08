import os
import json
import random
import discord
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para carregar texto
def load_texts():
    with open('sacred_texts.json', 'r') as f:
        return json.load(f)

# Função para pegar um verso de um livro, dado seu nome, versão, capítulo e versículo
def get_verse(book, version, chapter, verse):
    texts = load_texts()
    book_data = texts.get(book)
    if book_data and version in book_data['versions']:
        return book_data['versions'][version]['verses'].get(str(chapter), {}).get(str(verse))
    return None

# Função para registrar inputs e outputs do usuário em um arquivo .log
def log_interaction(user, command, *args, output=None, **kwargs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('logs.log', 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] User: {user}, Command: {command}, Args: {args}, Kwargs: {kwargs}, Output:\n{output}\n\n")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Acusa quando o BOT está online!
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()  # sincroniza os comandos da árvore

### Comandos
# Comando para mostrar um verso específico, dado o livro, versão, capítulo e versículo
@bot.tree.command(name='verse', description='Mostra um verso específico')
async def get_verse_command(interaction: discord.Interaction, book: str, language: str, chapter: str, verse: int):
    verse_text = get_verse(book, language, chapter, verse)
    if verse_text:
        output = f"*{verse_text}*"
        await interaction.response.send_message(output)
    else:
        output = 'Verso não encontrado.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'verse', book, version, chapter, verse, output=output)  # Registra o output

# Comando para mostrar um verso aleatório, dado o livro e a versão
@bot.tree.command(name='random', description='Mostra um verso aleatório')
async def random_verse(interaction: discord.Interaction, book: str, language: str):
    texts = load_texts()
    book_data = texts.get(book)
    if book_data and language in book_data['versions']:
        verses = book_data['versions'][language]['verses']
        chapter = random.choice(list(verses.keys()))
        verse = random.choice(list(verses[chapter].keys()))
        verse_text = verses[chapter][verse]
        output = f"`{chapter}.{verse}:`\n*{verse_text}*"
        await interaction.response.send_message(output)
    else:
        output = 'Livro ou versão não encontrada.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'random', book, language, output=output)  # Registra o output

# Comando para mostrar informações sobre todos os livros da database
@bot.tree.command(name='books', description='Mostra informações sobre os livros disponíveis')
async def books(interaction: discord.Interaction):
    texts = load_texts()
    if texts:
        output = ""
        for book, book_info in texts.items():
            author = book_info.get('author', 'Desconhecido')
            code = book_info.get('code', 'Desconhecido')
            year = book_info.get('year', 'Desconhecido')
            description = book_info.get('description', 'Desconhecido')
            versions = ', '.join(version for version in book_info['versions'].keys())
            links_str = ""
            for version, version_info in book_info['versions'].items():
                link = version_info.get('link')
                if link:
                    links_str += f"[[{version}]({link})] "

            output += f"## **{book}**\n`Código:` {code}\n`Autor:` {author}\n`Ano:` {year}\n`Versões:` {links_str}\n`Descrição:` *{description}*\n"
        await interaction.response.send_message(output)
    else:
        output = 'Nenhum livro encontrado na base de dados.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'books', output=output)  # Registra o output

# Comando para mostrar versos que contenha o termo pesquisado
@bot.tree.command(name='search', description='Pesquisa por versos')
async def search_verses(interaction: discord.Interaction, book: str, language: str, keywords: str):
    texts = load_texts()
    if book not in texts:
        output = f"O livro '{book}' não existe."
        await interaction.response.send_message(output)
        log_interaction(interaction.user, 'search', book, language, keywords, output=output)
        return

    book_data = texts[book]
    if language not in book_data['versions']:
        output = f"A versão '{language}' não existe para o livro '{book}'."
        await interaction.response.send_message(output)
        log_interaction(interaction.user, 'search', book, language, keywords, output=output)
        return

    verses = book_data['versions'][language]['verses']
    results = []
    count = 0  # Contador de aparições
    for chapter, chapter_verses in verses.items():
        for verse, text in chapter_verses.items():
            if all(keyword.lower() in text.lower() for keyword in keywords.split()):
                results.append(f"`{chapter}.{verse}:`\n*{text}*")
                count += 1  # Incrementa o contador

    if results:
        response = f"**{count} ocorrência(s) de `{keywords}` em \"{book}\":**\n"
        message_limit = 1900
        current_message = response

        for result in results:
            if len(current_message + result) <= message_limit:
                current_message += "\n" + result + "\n"
            else:
                if not interaction.response.is_done():  # Primeira mensagem
                    await interaction.response.send_message(current_message)
                else:
                    await interaction.followup.send(current_message)
                current_message = result + "\n" # Começa uma nova mensagem

        # Envia a última mensagem, se houver
        if current_message:
            if not interaction.response.is_done():
                await interaction.response.send_message(current_message)
            else:
                await interaction.followup.send(current_message)
        output = "Resultados enviados!"
    else:
        output = f"Nenhum resultado encontrado para a pesquisa de {keywords} em \"{book}\"."
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'search', book, version, keywords, output=output)

### Autocompletes
@random_verse.autocomplete('book')
@get_verse_command.autocomplete('book')
@search_verses.autocomplete('book')
async def autocomplete_book(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    books = [book for book in texts.keys() if current.lower() in book.lower()]
    return [Choice(name=book, value=book) for book in books]

@random_verse.autocomplete('language')
@get_verse_command.autocomplete('language')
@search_verses.autocomplete('language')
async def autocomplete_version(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book = next((option['value'] for option in interaction.data['options'] if option['name'] == 'book'), None)
    if book and book in texts:
        languages = texts[book]['versions'].keys()
        return [Choice(name=language, value=language) for language in languages if current.lower() in language.lower()]
    return []

@get_verse_command.autocomplete('chapter')
async def autocomplete_chapter(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book = next((option['value'] for option in interaction.data['options'] if option['name'] == 'book'), None)
    language = next((option['value'] for option in interaction.data['options'] if option['name'] == 'language'), None)
    if book and language and book in texts and language in texts[book]['versions']:
        chapters = texts[book]['versions'][language]['verses'].keys()
        return [Choice(name=chapter, value=str(chapter)) for chapter in chapters if str(current) in str(chapter)]
    return []

@get_verse_command.autocomplete('verse')
async def autocomplete_verse(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book = next((option['value'] for option in interaction.data['options'] if option['name'] == 'book'), None)
    language = next((option['value'] for option in interaction.data['options'] if option['name'] == 'language'), None)
    chapter = next((option['value'] for option in interaction.data['options'] if option['name'] == 'chapter'), None)
    if book and language and chapter and book in texts and language in texts[book]['versions'] and str(chapter) in texts[book]['versions'][language]['verses']:
        verses = texts[book]['versions'][language]['verses'][str(chapter)].keys()
        return [Choice(name=verse, value=int(verse)) for verse in verses if str(current) in str(verse)]
    return []

# Auth token
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)