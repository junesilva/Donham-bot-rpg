import disnake
from disnake.ext import commands
from disnake.ui import Button, View

from functions import get_character_name, get_race, get_class, save_player_data, get_player_data, load_player_data, format_profile, generate_progress_bar, get_random_weapon_and_armor, get_joke

import config
import asyncio
import traceback
import random
from characters import races_dict, classes_dict
import json
import os
import unidecode

intents = disnake.Intents.all()
intents.guilds = True
intents.members = False
intents.messages = True

client = commands.Bot(
    command_prefix=config.PREFIX,
    intents=intents,
    help_command=None)

@client.event
async def on_ready():
    activity = disnake.Game(name= 'RPG', type = 3)
    await client.change_presence(status=disnake.Status.online, activity=activity)
    print(f"Bot connected as {client.user.name}")


@client.slash_command(name="help", description="Botão de ajuda para novos usuários.")
async def help(inter):
    await inter.response.send_message("""
!help - Mostra esse menu.
!start - Inicia a criação de um novo personagem.
!perfil - Exibe o perfil do jogador.
!ping - Exibe a latência do bot no servidor.
    """)

@client.slash_command(name="start", description="Inicia a criação de um novo personagem.")
async def start(inter):
    existing_profile = get_player_data(inter.author.id)
    if existing_profile is not None:
        await inter.response.send_message("Parece que você já tem um perfil! Cada usuário só pode ter 1 perfil ativo.")
        return

    await inter.response.send_message("Vamos criar um novo personagem!")

    character_name = await get_character_name(inter, client)
    race = await get_race(inter)
    character_class = await get_class(inter)

    player_data = {
        "id": inter.author.id,
        "name": character_name,
        "race": race,
        "class": character_class
    }

    save_player_data(inter.author.id, player_data)

    await inter.response.send_message("Personagem criado com sucesso! Tente o comando ' /perfil ' ou ' !perfil '.")

@client.slash_command(name="perfil", description="Exibe o perfil do jogador.")
async def perfil(inter):
    player_id = str(inter.author.id)
    player_data = get_player_data(player_id)

    if not player_data:
        await inter.response.send_message("Você ainda não possui um perfil. Crie um personagem primeiro usando o comando '/start'.")
        return

    # Carregar dados de armas e armaduras do arquivo JSON
    with open("weapons_armors.json", "r", encoding="utf-8") as f:
        weapons_armors_data = json.load(f)

    # Obter a classe do jogador
    player_class = player_data["class"]

    # Verificar se a classe existe no arquivo JSON
    if player_class not in weapons_armors_data["classes"]:
        await inter.response.send_message("Classe inválida.")
        return

    # Obter uma arma e uma armadura aleatórias para a classe do jogador
    class_data = weapons_armors_data["classes"][player_class]
    weapons = class_data.get("armas")
    armors = class_data.get("armaduras")

    if weapons and armors:
        weapon = random.choice(weapons)
        armor = random.choice(armors)

        # Atualizar o perfil do jogador com a arma e a armadura escolhidas
        player_data["weapon"] = weapon
        player_data["armor"] = armor

        # Atualizar as informações de XP e nível
        player_data["xp"] = 0  # Defina o valor inicial de XP aqui
        player_data["level"] = 1  # Defina o valor inicial de nível aqui

        # Salvar os dados atualizados no arquivo players.json
        save_player_data(inter.author.id, player_data)

        profile_embed = format_profile(player_data)
        await inter.response.send_message(embed=profile_embed)
    else:
        await inter.response.send_message("Não foi possível obter uma arma e uma armadura para a classe do jogador.")

@client.slash_command(name="ping", description="Ping!")
async def ping(inter):
    latency = client.latency
    await inter.response.send_message(f"Pong 🏓! Meu ping é {round(latency * 1000)}ms. {get_joke()}")

client.run(config.TOKEN)