import discord
from discord.ext import commands

token = "MTI0ODcyMDc4MDIzNDMzMDE1Mw.G0W0_X.t2XUtToTtrgKJgcIxhglv-LbvC58X9HVTz-eTo"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

numicon = [
    "0️⃣",
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟",
]
weeks = [
    "목요일",
    "금요일",
    "토요일",
    "일요일",
    "월요일",
    "화요일",
    "수요일",
]

times = [
    "04시~06시",
    "06시~08시",
    "08시~10시",
    "10시~12시",
    "12시~14시",
    "14시~16시",
    "16시~18시",
    "18시~20시",
    "20시~22시",
    "22시~24시",
]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.command(name="야")
async def msg(ctx):
    await ctx.send("호")


class Dropdown(discord.ui.Select):

    def __init__(self):
        voteOptions = [
            discord.SelectOption(label="요일", description="요일 투표 생성"),
            discord.SelectOption(label="시간", description="시간 투표 생성"),
        ]
        super().__init__(placeholder="투표 생성",
                         min_values=1,
                         max_values=1,
                         options=voteOptions)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "요일":
            des = ""

            for i in range(len(weeks)):
                des += f"  {numicon[i]} {weeks[i]}  "
                if i == 3:
                    des += "\n"

            embed = discord.Embed(title="요일 투표",
                                  description="참여 가능한 요일의 이모지를 클릭해주세요.")
            embed.add_field(name="요일", value=des)

            await interaction.response.send_message(embed=embed,
                                                    ephemeral=False)
            msg = await interaction.original_response()
            for i in range(len(weeks)):
                await msg.add_reaction(f"{numicon[i]}")

        elif self.values[0] == "시간":
            des = ""

            for i in range(len(times)):
                des += f"  {numicon[i]} {times[i]}  "
                if i == 3 or i == 7:
                    des += "\n"

            embed = discord.Embed(title="시간 투표",
                                  description="참여 가능한 시간의 이모지를 클릭해주세요.")
            embed.add_field(name="시간", value=des)

            await interaction.response.send_message(embed=embed,
                                                    ephemeral=False)
            msg = await interaction.original_response()
            for i in range(len(times)):
                await msg.add_reaction(f"{numicon[i]}")


class DropdownView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


@bot.tree.command(name="투표", description="투표를 시작합니다.")
async def lang(interaction: discord.Interaction):
    await interaction.response.send_message("투표 종류를 선택하세요.",
                                            view=DropdownView(),
                                            ephemeral=True)


bot.run(token)
