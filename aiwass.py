import json
import random
import discord
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime

# Função para carregar configurações
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Função para carregar texto
def load_texts():
    with open('sacred_texts.json', 'r') as f:
        return json.load(f)

# Função para pegar um verso de um livro, dado seu nome, versão, capítulo e versículo
def get_verse(book_title, version, chapter, verse):
    texts = load_texts()
    book = texts.get(book_title)
    if book and version in book['versions']:
        return book['versions'][version]['verses'].get(str(chapter), {}).get(str(verse))
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

# Comando para mostrar um verso específico, dado o livro, versão, capítulo e versículo
@bot.tree.command(name='verse', description='Mostra um verso específico')
async def get_verse_command(interaction: discord.Interaction, book_title: str, version: str, chapter: str, verse: int):
    verse_text = get_verse(book_title, version, chapter, verse)
    if verse_text:
        output = f"*{verse_text}*"
        await interaction.response.send_message(output)
    else:
        output = 'Verso não encontrado.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'verse', book_title, version, chapter, verse, output=output)  # Registra o output

# Comando para mostrar um verso aleatório, dado o livro e a versão
@bot.tree.command(name='random', description='Mostra um verso aleatório')
async def random_verse(interaction: discord.Interaction, book_title: str, version: str):
    texts = load_texts()
    book = texts.get(book_title)
    if book and version in book['versions']:
        verses = book['versions'][version]['verses']
        chapter = random.choice(list(verses.keys()))
        verse = random.choice(list(verses[chapter].keys()))
        verse_text = verses[chapter][verse]
        output = f"`{chapter}.{verse}`: *{verse_text}*"
        await interaction.response.send_message(output)
    else:
        output = 'Livro ou versão não encontrada.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'random', book_title, version, output=output)  # Registra o output

# Comando para mostrar informações sobre todos os livros da database
@bot.tree.command(name='books', description='Mostra informações sobre os livros disponíveis')
async def books(interaction: discord.Interaction):
    texts = load_texts()
    if texts:
        output = "Livros disponíveis:\n\n"
        for book_title, book_info in texts.items():
            author = book_info.get('author', 'Desconhecido')
            code = book_info.get('code', 'Desconhecido')
            year = book_info.get('year', 'Desconhecido')
            versions = ', '.join(book_info['versions'].keys())
            output += f"Título: **{book_title}**\nCódigo: *{code}*\nAutor: *{author}*\nAno: *{year}*\nVersões: *{versions}*\n\n"
        await interaction.response.send_message(output)
    else:
        output = 'Nenhum livro encontrado na base de dados.'
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'books', output=output)  # Registra o output

# Comando para mostrar versos que contenha o termo pesquisado
@bot.tree.command(name='search', description='Pesquisa por versos')
async def search_verses(interaction: discord.Interaction, book_title: str, version: str, keywords: str):
    texts = load_texts()
    if book_title not in texts:
        output = f"O livro '{book_title}' não existe."
        await interaction.response.send_message(output)
        log_interaction(interaction.user, 'search', book_title, version, keywords, output=output)
        return

    book = texts[book_title]
    if version not in book['versions']:
        output = f"A versão '{version}' não existe para o livro '{book_title}'."
        await interaction.response.send_message(output)
        log_interaction(interaction.user, 'search', book_title, version, keywords, output=output)
        return

    verses = book['versions'][version]['verses']
    results = []
    count = 0  # Contador de aparições
    for chapter, chapter_verses in verses.items():
        for verse, text in chapter_verses.items():
            if all(keyword.lower() in text.lower() for keyword in keywords.split()):
                results.append(f"`{chapter}.{verse}`: *{text}*")
                count += 1  # Incrementa o contador

    if results:
        response = f"**{count} ocorrência(s) de `{keywords}` em \"{book_title}\":**\n"
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
        output = f"Nenhum resultado encontrado para a pesquisa de {keywords} em \"{book_title}\" (versão {version})."
        await interaction.response.send_message(output)
    log_interaction(interaction.user, 'search', book_title, version, keywords, output=output)

# Autocompletes
@random_verse.autocomplete('book_title')
@get_verse_command.autocomplete('book_title')
@search_verses.autocomplete('book_title')
async def autocomplete_book_title(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book_titles = [book_title for book_title in texts.keys() if current.lower() in book_title.lower()]
    return [Choice(name=book_title, value=book_title) for book_title in book_titles]

@random_verse.autocomplete('version')
@get_verse_command.autocomplete('version')
@search_verses.autocomplete('version')
async def autocomplete_version(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book_title = next((option['value'] for option in interaction.data['options'] if option['name'] == 'book_title'), None)
    if book_title and book_title in texts:
        versions = texts[book_title]['versions'].keys()
        return [Choice(name=version, value=version) for version in versions if current.lower() in version.lower()]
    return []

@get_verse_command.autocomplete('chapter')
async def autocomplete_chapter(interaction: discord.Interaction, current: str) -> list[Choice]:
    texts = load_texts()
    book_title = next((option['value'] for option in interaction.data['options'] if option['name'] == 'book_title'), None)
    version = next((option['value'] for option in interaction.data['options'] if option['name'] == 'version'), None)
    if book_title and version and book_title in texts and version in texts[book_title]['versions']:
        chapters = texts[book_title]['versions'][version]['verses'].keys()
        return [Choice(name=chapter, value=str(chapter)) for chapter in chapters if str(current) in str(chapter)]
    return []

# Auth token
config = load_config()
TOKEN = config['DISCORD_TOKEN']
bot.run(TOKEN)