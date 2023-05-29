import disnake
import os
import random
import json
import asyncio
import time

from disnake.ext import commands
import characters
from characters import races_dict, classes_dict

async def get_character_name(inter, client):
    await inter.response.send_message("Qual é o nome do seu personagem?")
    try:
        def check(message):
            return message.author == inter.user and message.channel == inter.channel

        name_inter = await client.wait_for("message", check=check, timeout=60)  # Aguarda 60 segundos por uma nova mensagem
        character_name = name_inter.content
        return character_name
    except asyncio.TimeoutError:
        await inter.response.send_message("Tempo esgotado. Tente novamente.")
        return None

async def get_race(inter):
    races_dict = characters.races_dict

    races_msg = "Escolha uma raça:\n"
    for race_key, race_data in races_dict.items():
        races_msg += f"\n**{disnake.utils.escape_markdown(race_key)}**:\n"
        races_msg += f"{disnake.utils.escape_markdown(race_data['description'])}\n"
        races_msg += f"Habilidades Primárias: {race_data['habilidades_primarias']}\n"
        if race_data['bonus_habilidades']:
            races_msg += f"Bônus de Habilidades: {race_data['bonus_habilidades']}\n"
        if race_data['bonus_caracteristicas']:
            races_msg += f"Bônus de Características: {race_data['bonus_caracteristicas']}\n"

    races_msg += "\nDigite o nome da raça para selecioná-la."

    embed = disnake.Embed(color=disnake.Color.gold(), description=races_msg)
    await inter.send(embed=embed)

    try:
        def check(message):
            return message.author == inter.author and message.channel == inter.channel

        race_msg = await inter.bot.wait_for('message', check=check, timeout=60)  # Aguarda 60 segundos por uma nova mensagem
        chosen_race = race_msg.content.lower()  # Converte a raça para letras minúsculas

        for race_key in races_dict.keys():
            if chosen_race.lower() == race_key.lower():
                return race_key

        await inter.send("Raça inválida.")
        return None
    except asyncio.TimeoutError:
        await inter.send("Tempo esgotado. Tente novamente.")
        return None

async def get_class(inter):
    classes_dict = characters.classes_dict

    classes_msg = "Escolha uma classe:\n"
    for class_key, class_data in classes_dict.items():
        classes_msg += f"\n**{disnake.utils.escape_markdown(class_key)}**:\n"
        classes_msg += f"{disnake.utils.escape_markdown(class_data['description'])}\n"
        classes_msg += f"Vida: {class_data['vida']}\n"

    classes_msg += "\nDigite o nome da classe para selecioná-la."

    embed = disnake.Embed(color=disnake.Color.gold(), description=classes_msg)
    await inter.send(embed=embed)

    try:
        def check(message):
            return message.author == inter.author and message.channel == inter.channel

        class_msg = await inter.bot.wait_for('message', check=check, timeout=60)  # Aguarda 60 segundos por uma nova mensagem
        chosen_class = class_msg.content.lower()
        for class_key in classes_dict.keys():
            if chosen_class.lower() == class_key.lower():
                return class_key

        await inter.send("Classe inválida.")
        return None
    except asyncio.TimeoutError:
        await inter.send("Tempo esgotado. Tente novamente.")
        return None

def get_player_data(player_id):
    with open("players.json", "r") as file:
        players_data = json.load(file)

    return players_data.get(str(player_id))

def save_player_data(player_id, player_data):
    filename = "players.json"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            players_data = json.load(file)
    else:
        players_data = {}

    players_data[str(player_id)] = player_data

    with open(filename, "w") as file:
        json.dump(players_data, file)

def load_player_data(file_path):
    with open(file_path, "r") as file:
        player_data = json.load(file)
    return player_data

def calculate_next_level_xp(level):
    if level is None:
        return 0  # or any default value you want to use

    base_xp = 5  # Base XP value
    common_ratio = 1.5  # Common ratio for the geometric progression
    next_level_xp = base_xp * (common_ratio ** level)
    return int(next_level_xp)

def format_profile(player_data):
    name = player_data.get("name")
    race = player_data.get("race")
    character_class = player_data.get("class")
    level = player_data.get("level")
    xp = player_data.get("xp")
    weapon = player_data.get("weapon")
    armor = player_data.get("armor")

    # Calculate progress towards next level
    next_level_xp = calculate_next_level_xp(level)
    if xp is None:
        xp = 0  # or any default value you want to use
    progress = xp - next_level_xp 
    progress_bar = generate_progress_bar(progress)

    embed = disnake.Embed(title="Perfil", color=0xcc0000)
    embed.add_field(name="Nome", value=name, inline=False)
    embed.add_field(name="Raça", value=race, inline=False)
    embed.add_field(name="Classe", value=character_class, inline=False)
    embed.add_field(name="Nível", value=level, inline=False)
    embed.add_field(name="XP", value=f"{xp}/{next_level_xp} {progress_bar}", inline=False)
    embed.add_field(name="Arma", value=weapon, inline=False)
    embed.add_field(name="Armadura", value=armor, inline=False)

    return embed

def generate_progress_bar(progress):
    bar_length = 6  # Tamanho fixo da barra de progresso
    filled_length = int(progress * bar_length)
    empty_length = bar_length - filled_length

    progress_bar = "█" * filled_length + "░" * empty_length
    return f"[{progress_bar}]"

def load_monster_data():
    with open("monsters.json", "r") as file:
        monster_data = json.load(file)
    return monster_data.get("monsters")

def load_task_data():
    with open("tasks.json", "r") as file:
        task_data = json.load(file)
    return task_data.get("tasks")

def defeat_monster(player_id, monster_name):
    monsters = load_monster_data()
    for monster in monsters:
        if monster["name"].lower() == monster_name.lower():
            xp = monster["xp"]
            if award_xp(player_id, xp):
                return f"You defeated the {monster_name} and gained {xp} XP!"
            else:
                return "Player not found."
    return f"No monster found with the name {monster_name}."

def award_xp(player_id, xp):
    player_data = get_player_data(player_id)
    if player_data is not None:
        current_xp = player_data.get("xp", 0)
        player_data["xp"] = current_xp + xp
        save_player_data(player_id, player_data)
        return True
    return False

def get_random_weapon_and_armor(player_class):
    with open("weapons_armors.json", "r") as file:
        weapons_armors_data = json.load(file)

    if player_class in weapons_armors_data:
        class_data = weapons_armors_data[player_class]
        weapons = class_data.get("weapons")
        armors = class_data.get("armors")

        if weapons and armors:
            weapon = random.choice(weapons)
            armor = random.choice(armors)
            return weapon, armor

    return None, None

def get_joke():
    jokes = [
        "Qual é o dado mais indeciso? O dú-bado!",
        "Por que o mago não sai de casa? Porque ele está sempre conjurado!",
        "Qual é o calçado favorito dos personagens de RPG? As botas de Elfo!",
        "Qual é o prato favorito dos orcs? Braço de frango!",
        "O que um elfo disse para o outro? 'Vamos dar um arco para essa conversa!'",
        "Por que o ladino sempre carrega um lenço? Porque ele gosta de dar o 'golpe baixo'!",
        "Qual é o animal preferido dos aventureiros? O rato do computador!",
        "Por que o guerreiro comprou uma máquina de costura? Porque ele queria fazer pontos!",
        "O que o orc disse para o mago? 'Você é um feiticeiro-córnio!'",
        "Qual é a bebida favorita dos bardos? O suco de lira-lima!",
        "Por que o paladino nunca fica doente? Porque ele tem imunidade divina!",
        "O que o gnomo disse para o dragão? 'Você é tão escamoso que parece uma escama-bole!'",
        "Qual é o feitiço preferido do bruxo? 'Escuridão, meu amigo!'",
        "Por que o clérigo não abre uma padaria? Porque ele já tem muitos pães!",
        "O que o ranger disse para a natureza? 'Vamos falar em árvores?'",
        "Qual é o bicho que todo mestre de RPG tem medo? O 'des-gatinho'!",
        "Por que o druida é bom em economia? Porque ele sabe como fazer o dinheiro 'crescer'!",
        "O que o dragão disse para o aventureiro? 'Hoje você vira churrasco!'",
        "Qual é o reino preferido dos jogadores de RPG? O Reino da Imaginação!",
        "Por que o gnomo é bom em resolver problemas? Porque ele tem um 'gnomcomputador'!",
        "O que a fada disse para o troll? 'Para de ser tão 'trollado'!",
        "Qual é o feitiço favorito do necromante? 'Levanta-defunto'!",
        "Por que o bardo não gosta de nadar? Porque ele tem medo de afogar as cordas vocais!",
        "O que o mago falou para o aprendiz? 'Você ainda tem muito 'mage-nésio' para tomar!'",
        "Qual é o sabor de sorvete favorito dos jogadores de RPG? O 'RPGelado'!",
        "Por que o guerreiro tem uma vida tão difícil? Porque ele vive 'espada-dinha'!",
        "O que o lich disse para o aventureiro? 'Vamos dar um 'abraçaço'!'",
        "Qual é o prato favorito do clérigo? A 'soparção' divina!",
        "Por que o mago não gosta de chuva? Porque ele prefere feitiços 'ensolarados'!",
        "O que o gnomo disse para o gigante? 'Você é tão alto que nem 'gnomostra' sua cabeça!'",
        "Qual é a cidade favorita dos elfos? 'Elfe-querque'!",
    ]

    return random.choice(jokes)
