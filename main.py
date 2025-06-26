import discord
from discord.ext import commands
import re
import difflib
import os
import unicodedata
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_REGISTRO_ID = int(os.getenv("CANAL_REGISTRO_ID"))
SOBRENATURAL_ROLE_ID = int(os.getenv("SOBRENATURAL_ROLE_ID"))
CARGO_REMOVER_ID = 1341006789059285063

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

modelo_regex = re.compile(
    r'nome\s*:\s*(.+?)\s+'
    r'nome\s+sobrenatural\s*:\s*(.+?)\s+'
    r'id\s*:\s*(.+?)\s+'
    r'raca\s*:\s*(.+?)\s+'
    r'(?:cla\s*:\s*(.*?)\s+)?'  # Clã opcional
    r'proficiencia\s*:\s*(.+?)(?:\s|$)',
    re.IGNORECASE | re.DOTALL
)

def encontrar_cargo_semelhante(nome_cargo_desejado, todos_os_cargos):
    nomes_dos_cargos = [role.name for role in todos_os_cargos]
    correspondencias = difflib.get_close_matches(nome_cargo_desejado, nomes_dos_cargos, n=1, cutoff=0.6)
    if correspondencias:
        return discord.utils.get(todos_os_cargos, name=correspondencias[0])
    return None

profissoes_validas = [
    "Gemólogo",
    "Herbalista",
    "Alquimista",
    "Ferreiro",
    "Joalheiro",
    "Mercador"
]

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != CANAL_REGISTRO_ID:
        return

    linhas = message.content.splitlines()

    try:
        nome_real = linhas[0].split(":", 1)[1].strip()
        nome_sobrenatural = linhas[1].split(":", 1)[1].strip()
        user_id = linhas[2].split(":", 1)[1].strip()
        raca = linhas[3].split(":", 1)[1].strip()

        if "clã" in linhas[4].lower() or "cla" in linhas[4].lower():
            cla = linhas[4].split(":", 1)[1].strip()
            proficiencia = linhas[5].split(":", 1)[1].strip()
        else:
            cla = None
            proficiencia = linhas[4].split(":", 1)[1].strip()
    except IndexError:
        await message.add_reaction("❌")
        await message.reply("❌ Registro incompleto.")
        return

    # Validações obrigatórias
    if not nome_real:
        await message.add_reaction("❌")
        await message.reply("❌ Registro incorreto. Nome não pode estar em branco.")
        return

    if not nome_sobrenatural:
        await message.add_reaction("❌")
        await message.reply("❌ Registro incorreto. Nome Sobrenatural não pode estar em branco.")
        return

    if not user_id:
        await message.add_reaction("❌")
        await message.reply("❌ Registro incorreto. ID não pode estar em branco.")
        return

    if not raca:
        await message.add_reaction("❌")
        await message.reply("❌ Registro incorreto. Raça não pode estar em branco.")
        return

    if not proficiencia:
        await message.add_reaction("❌")
        embed = discord.Embed(
            title="Opções válidas para Proficiência",
            description="\n".join(f"- {p}" for p in profissoes_validas),
            color=discord.Color.red()
        )
        await message.reply(embed=embed)
        return

    try:
        guild = message.guild
        cargos_a_setar = []

        # Verificar Clã (opcional)
        if cla:
            cargo_cla = encontrar_cargo_semelhante(cla, guild.roles)
            if cargo_cla:
                cargos_a_setar.append(cargo_cla)
            else:
                clas_disponiveis = [
                    role.name for role in guild.roles
                    if "cla" in remover_acentos(role.name.lower())
                ]
                sugestao = "\n".join(f"- {nome}" for nome in clas_disponiveis) or "Nenhum clã disponível no servidor."
                await message.add_reaction("❌")
                embed = discord.Embed(
                    title=f"Cargo '{cla}' não encontrado.",
                    description=f"Verifique se escreveu corretamente.\nAqui estão alguns clãs disponíveis:\n{sugestao}",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed)
                return

        # Verificar Proficiência (obrigatório)
        cargo_proficiencia = encontrar_cargo_semelhante(proficiencia, guild.roles)
        if cargo_proficiencia:
            cargos_a_setar.append(cargo_proficiencia)
        else:
            await message.add_reaction("❌")
            embed = discord.Embed(
                title=f"Proficiência '{proficiencia}' não encontrada.",
                description="Proficiências válidas:\n" + "\n".join(f"- {p}" for p in profissoes_validas),
                color=discord.Color.red()
            )
            await message.reply(embed=embed)
            return

        sobrenatural_cargo = guild.get_role(SOBRENATURAL_ROLE_ID)
        if sobrenatural_cargo:
            cargos_a_setar.append(sobrenatural_cargo)

        novo_apelido = f"{nome_sobrenatural} | {user_id}"
        await message.author.edit(nick=novo_apelido)
        await message.author.add_roles(*cargos_a_setar, reason="Registro automático")

        cargo_para_remover = guild.get_role(CARGO_REMOVER_ID)
        if cargo_para_remover and cargo_para_remover in message.author.roles:
            await message.author.remove_roles(cargo_para_remover, reason="Removido após registro")

        await message.add_reaction("✅")
        await message.reply("✅ Registro realizado com sucesso!")

    except discord.Forbidden:
        await message.reply("❌ Permissão insuficiente para alterar apelido ou cargos.")
    except Exception as e:
        await message.reply(f"❌ Erro: {e}")

bot.run(TOKEN)
