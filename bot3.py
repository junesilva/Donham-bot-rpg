import discord
from discord.ext import commands
import config
from comandos import (
    carregar_dados, gravar_dados, verificar_admin, adicionar_jogador,
    exibir_jogador, remover_jogador, gravar_vidas, carregar_vidas, atualizar_vida
)
import asyncio
import traceback
from frontend import generate_player_card
import random
from characters import racas_dict, classes_dict
import json
import os
import unidecode

intents = discord.Intents.all()
intents.guilds = True
intents.members = False
intents.messages = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

@bot.command()
async def start(ctx):
    jogador = ctx.author
    dados = carregar_dados()
    
    if jogador in dados:
        await ctx.send("Jogador encontrado. Seu perfil já existe.")
    else:
        await ctx.send("Jogador não encontrado. Criando um novo perfil...")
        await ctx.send("Por favor, escolha um nome para o seu personagem:")

        def check(m):
            return m.author == jogador

        try:
            nome_personagem = await bot.wait_for('message', check=check, timeout=30)
            nome_personagem = nome_personagem.content
            nome_personagem_sem_acentos = unidecode.unidecode(nome_personagem)
            dados[jogador] = {"nome_personagem": nome_personagem_sem_acentos}
            await ctx.send(f"Perfil criado! Seu nome de personagem é: {nome_personagem}")
            await asyncio.sleep(2)
            await ctx.send(f"Raças disponíveis: {', '.join(racas_dict.keys())}")
            await asyncio.sleep(2)
            await ctx.send(f"Classes disponíveis: {', '.join(classes_dict.keys())}")
        except asyncio.TimeoutError:
            await ctx.send("Tempo limite excedido. Por favor, execute o comando novamente.")

@bot.command()
async def novojogo(ctx):
    jogador = ctx.author
    dados = carregar_dados()

    if jogador not in dados:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        await ctx.send("Criando um novo perfil...")
        await ctx.send("Por favor, escolha um nome para o seu novo personagem:")

        def check(m):
            return m.author == jogador

        try:
            nome_personagem = await bot.wait_for('message', check=check, timeout=30)
            nome_personagem = nome_personagem.content
            nome_personagem_sem_acentos = unidecode.unidecode(nome_personagem)
            dados[jogador] = {"nome_personagem": nome_personagem_sem_acentos}
            await ctx.send(f"Novo perfil criado! Seu nome de personagem é: {nome_personagem}")
            await asyncio.sleep(2)
            await ctx.send(f"Raças disponíveis: {', '.join(racas_dict.keys())}")
            await asyncio.sleep(2)
            await ctx.send(f"Classes disponíveis: {', '.join(classes_dict.keys())}")
        except asyncio.TimeoutError:
            await ctx.send("Tempo limite excedido. Por favor, execute o comando novamente.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    jogador = message.author
    dados = carregar_dados()

    if jogador in dados:
        await bot.process_commands(message)  # Executa os comandos normalmente
    else:
        await message.channel.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")

@bot.command()
async def escolherraca(ctx, raca):
    jogador = ctx.author
    dados = carregar_dados()

    if jogador not in dados:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        raca = raca.lower()

        if raca not in racas_dict:
            await ctx.send("Raça inválida. Por favor, escolha uma raça disponível.")
        else:
            dados[jogador]["raca"] = raca
            await ctx.send(f"Raça escolhida: {raca.capitalize()}")

@bot.command()
async def escolherclasse(ctx, classe):
    jogador = ctx.author
    dados = carregar_dados()

    if jogador not in dados:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        classe = classe.lower()

        if classe not in classes_dict:
            await ctx.send("Classe inválida. Por favor, escolha uma classe disponível.")
        else:
            dados[jogador]["classe"] = classe
            await ctx.send(f"Classe escolhida: {classe.capitalize()}")

@bot.command()
async def perfil(ctx):
    jogador = ctx.author
    dados = carregar_dados()

    if jogador not in dados:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        nome_personagem = dados[jogador]["nome_personagem"]
        raca = dados[jogador].get("raca", "Não escolhida")
        classe = dados[jogador].get("classe", "Não escolhida")

        card = generate_player_card(nome_personagem, raca, classe)
        await ctx.send(f"Nome do personagem: {nome_personagem}\n"
                       f"Raça: {raca.capitalize()}\n"
                       f"Classe: {classe.capitalize()}", file=discord.File(card, "card.png"))

@bot.command()
async def resetarperfil(ctx):
    jogador = ctx.author
    dados = carregar_dados()

    if jogador not in dados:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        del dados[jogador]
        await ctx.send("Perfil resetado com sucesso.")

@bot.command()
async def sair(ctx):
    jogador = ctx.author
    if jogador in dados:
        del jogadores[jogador]
        await ctx.send("Perfil removido. Você pode criar um novo perfil usando o comando `!start`.")
    else:
        await ctx.send("Jogador não encontrado. Não há perfil para remover.")

@bot.command()
async def gerar(ctx):
    jogador = ctx.author
    if jogador not in jogadores:
        await ctx.send("Jogador não encontrado. Execute o comando `!start` para criar um novo perfil.")
    else:
        perfil_jogador = jogadores[jogador]
        nome_personagem = perfil_jogador.get("nome_personagem")
        raca = perfil_jogador.get("raca")
        classe = perfil_jogador.get("classe")

        if nome_personagem and raca and classe:
            card = generate_player_card(nome_personagem, raca, classe)
            await ctx.send(file=discord.File(card, "player_card.png"))
        else:
            await ctx.send("Perfil incompleto. Por favor, escolha uma raça e uma classe.")

bot.run(config.TOKEN)