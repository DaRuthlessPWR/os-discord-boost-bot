import discord
from discord.ui import button
import json, httpx, tls_client, threading, time, random, hashlib, sys, os
from flask import request, Flask, jsonify
from keyauth import api

class Fore:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

#os.system("title " + "LEON BOOST BOT")

app = Flask(__name__)

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest


config = json.load(open("config.json", encoding="utf-8"))


class Booster:
    def __init__(self) -> None:
        self.proxy = self.getProxy()
        self.getCookies()
        self.client = tls_client.Session(
            client_identifier="chrome_107",
            ja3_string="771,4866-4867-4865-49196-49200-49195-49199-52393-52392-49327-49325-49188-49192-49162-49172-163-159-49315-49311-162-158-49314-49310-107-106-103-64-57-56-51-50-157-156-52394-49326-49324-49187-49191-49161-49171-49313-49309-49233-49312-49308-49232-61-192-60-186-53-132-47-65-49239-49235-49238-49234-196-195-190-189-136-135-69-68-255,0-11-10-35-16-22-23-49-13-43-45-51-21,29-23-30-25-24,0-1-2",
            h2_settings={
                "HEADER_TABLE_SIZE": 65536,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_HEADER_LIST_SIZE": 262144,
            },
            h2_settings_order=[
                "HEADER_TABLE_SIZE",
                "MAX_CONCURRENT_STREAMS",
                "INITIAL_WINDOW_SIZE",
                "MAX_HEADER_LIST_SIZE",
            ],
            supported_signature_algorithms=[
                "ECDSAWithP256AndSHA256",
                "PSSWithSHA256",
                "PKCS1WithSHA256",
                "ECDSAWithP384AndSHA384",
                "PSSWithSHA384",
                "PKCS1WithSHA384",
                "PSSWithSHA512",
                "PKCS1WithSHA512",
            ],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
            connection_flow=15663105,
            header_order=["accept", "user-agent", "accept-encoding", "accept-language"],
        )
        self.failed = []
        self.success = []
        self.captcha = []
        if config["proxyless"] == False:
            self.client.proxies = self.proxy

    def getProxy(self):
        try:
            proxy = random.choice(open("data/proxies.txt", "r").read().splitlines())
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        except Exception as e:
            pass

    def getCookies(self, session=None):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.5",
            "connection": "keep-alive",
            "host": "canary.discord.com",
            "referer": "https://canary.discord.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
            "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
        }
        response = httpx.get(
            "https://canary.discord.com/api/v9/experiments", headers=headers
        )
        self.dcfduid = response.cookies.get("__dcfduid")
        self.sdcfduid = response.cookies.get("__sdcfduid")
        self.cfruid = response.cookies.get("__cfruid")

    def boost(self, token, invite, guild):
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9",
            "authorization": token,
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": f"__dcfduid={self.dcfduid}; __sdcfduid={self.sdcfduid}; __cfruid={self.cfruid}; locale=en-US",
            "origin": "https://discord.com",
            "pragma": "no-cache",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
        }

        slots = httpx.get(
            "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots",
            headers=headers,
        )

        slot_json = slots.json()

        if slots.status_code == 401:
            self.failed.append(token)
            return

        if slots.status_code != 200 or len(slot_json) == 0:
            return

        r = self.client.post(
            f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={}
        )

        if r.status_code == 200:
            boostsList = []
            for boost in slot_json:
                boostsList.append(boost["id"])

            payload = {"user_premium_guild_subscription_slot_ids": boostsList}

            headers["method"] = "PUT"
            headers["path"] = f"/api/v9/guilds/{guild}/premium/subscriptions"

            boosted = self.client.put(
                f"https://discord.com/api/v9/guilds/{guild}/premium/subscriptions",
                json=payload,
                headers=headers,
            )

            if boosted.status_code == 201:
                self.success.append(token)
                return True
            else:
                self.failed.append(token)

        elif r.status_code == 400:
            self.failed.append(token)

        elif r.status_code != 200:
            print(r.json())

    def nick(self, token, guild, nick):
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9",
            "authorization": token,
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": f"__dcfduid={self.dcfduid}; __sdcfduid={self.sdcfduid}; __cfruid={self.cfruid}; locale=en-US",
            "origin": "https://discord.com",
            "pragma": "no-cache",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1KTSIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IFU7IFBQQyBNYWMgT1MgWDsgZGUtZGUpIEFwcGxlV2ViS2l0Lzg1LjguNSAoS0hUTUwsIGxpa2UgR2Vja28pIFNhZmFyaS84NSIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTgxODMyLCJjbGllbnRfZXZlbnRfc291cmNlIjoibnVsbCJ9",
        }

        payload = {"nick": nick}

        httpx.patch(
            f"https://discord.com/api/v9/guilds/{guild}/members/@me",
            headers=headers,
            json=payload,
        )

        httpx.patch(
            f"https://discord.com/api/v9/users/@me/profile",
            headers=headers,
            json={"bio": nick},
        )

    def nickThread(self, tokens, guild, nick):
        """"""
        threads = []

        for i in range(len(tokens)):
            token = tokens[i]
            t = threading.Thread(target=self.nick, args=(token, guild, nick))
            t.daemon = True
            threads.append(t)

        for i in range(len(tokens)):
            threads[i].start()

        for i in range(len(tokens)):
            threads[i].join()

        return True

    def thread(self, invite, tokens, guild):
        """"""
        threads = []

        for i in range(len(tokens)):
            token = tokens[i]
            t = threading.Thread(target=self.boost, args=(token, invite, guild))
            t.daemon = True
            threads.append(t)

        for i in range(len(tokens)):
            threads[i].start()

        for i in range(len(tokens)):
            threads[i].join()

        return {
            "success": self.success,
            "failed": self.failed,
            "captcha": self.captcha,
        }



bot = discord.Bot(intents=discord.Intents.all())


def getStock(filename: str):
    tokens = []
    for i in open(filename, "r").read().splitlines():
        if ":" in i:
            i = i.split(":")[2]
            tokens.append(i)
        else:
            tokens.append(i)
    return tokens


def getinviteCode(inv):
    if "discord.gg" not in inv:
        return inv
    if "discord.gg" in inv:
        invite = inv.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in inv:
        invite = inv.split("https://discord.gg/")[1]
        return invite


def checkInvite(invite: str):
    data = httpx.get(
        f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true"
    ).json()

    if data["code"] == 10006:
        return False
    elif data:
        return data["guild"]["id"]
    else:
        return False


@bot.event
async def on_ready():
    print(f"{Fore.BLUE} [BOT]: {bot.user} is online.{Fore.RESET}")


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="boost", description="Boost a server by using that command."
)
async def boost(
    ctx,
    invite: discord.Option(str, "Invite code of the server.", required=True),
    amount: discord.Option(
        int, "Amount of boosts (must be in numbers).", required=True
    ),
    months: discord.Option(int, "Number of months (1/3).", required=True),
    nick: discord.Option(str, "Nickname and bio.", required=True),
):
    await ctx.response.defer(ephemeral=False)

    if str(ctx.author.id) not in config["owners"]:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Missing permissions, you cannot use this command.",
                color=0xC80000,
            )
        )

    if amount % 2 != 0:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Number of boosts should be in numbers.",
                color=0xC80000,
            )
        )

    if months != 1 and months != 3:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Invalid months [VALID INPUTS: 1/3].",
                color=0xC80000,
            )
        )

    inviteCode = getinviteCode(invite)
    inviteData = checkInvite(inviteCode)

    if inviteData == False:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Invalid invite provided.",
                color=0xC80000,
            )
        )

    if months == 1:
        filename = "data/1m.txt"
    if months == 3:
        filename = "data/3m.txt"

    tokensStock = getStock(filename)
    requiredStock = int(amount / 2)

    if requiredStock > len(tokensStock):
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description=f"We don't have enough tokens in stock\nUse `/restock` command to restock.",
                color=0xC80000,
            )
        )

    boost = Booster()

    tokens = []

    for x in range(requiredStock):
        tokens.append(tokensStock[x])
        remove(tokensStock[x], filename)

    await ctx.respond(
        embed=discord.Embed(
            title="Boost Bot", description=f"Boosting....", color=0x5598D2
        )
    )

    start = time.time()
    status = boost.thread(inviteCode, tokens, inviteData)

    time_taken = round(time.time() - start, 2)

    await ctx.edit(
        embed=discord.Embed(
            title="**Boosts Successful**",
            description=f"**__Amount__ ->**  {amount} boosts \n**__Months__ ->** {months}m \n**__Server Link__ ->** .gg/{inviteCode} \n**__Tokens used__ ->** {requiredStock} \n**__Successfull tokens__ ->** {len(status['success'])} \n**__Failed tokens__ ->** {len(status['failed'])}\n**__Captcha tokens__ ->** {len(status['captcha'])} \n**__Time taken__ ->** {time_taken}s",
            color=0x5598D2,
        )
    )

    boost.nickThread(tokens, inviteData, nick)

    return True


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="addadmin", description="Add an admin to use the bot command."
)
async def addadmin(
    ctx,
    member: discord.Option(discord.Member, "The member you want to add.", required=True),
):
    await ctx.defer(ephemeral=False)
    if str(ctx.author.id) not in config["owners"]:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="You cannot use this command.",
                color=0xC80000,
            )
        )

    config["admins"].append(str(member.id))
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return await ctx.edit(
        embed=discord.Embed(
            title="Boost Bot",
            description=f"Added the member to admin successfully.",
            color=0x5598D2,
        )
    )


def remove(token: str, filename: str):
    tokens = getStock(filename)
    tokens.pop(tokens.index(token))
    f = open(filename, "w")

    for x in tokens:
        f.write(f"{x}\n")

    f.close()


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="sendtokens", description="Sends the tokens to the user."
)
async def sendtokens(
    ctx,
    member: discord.Option(discord.Member, "The member you want to send.", required=True),
    amount: discord.Option(int, "Amount of tokens to send.", required=True),
    months: discord.Option(int, "Number of months (1/3).", required=True),
):
    await ctx.defer(ephemeral=False)

    if str(ctx.author.id) not in config["owners"]:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Missing permissions, you cannot use this command.",
                color=0xC80000,
            )
        )

    if months != 1 and months != 3:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Invalid months [VALID INPUTS: 1/3].",
                color=0xC80000,
            )
        )

    if months == 1:
        filename = "data/1m.txt"
    if months == 3:
        filename = "data/3m.txt"

    tokensStock = getStock(filename)

    if amount > len(tokensStock):
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description=f"We don't have enough tokens in stock\nUse `/restock` command to restock.",
                color=0xC80000,
            )
        )

    tokens = []
    for x in range(amount):
        tokens.append(tokensStock[x])
        remove(tokensStock[x], filename)

    stuff = "\n".join(tokens)

    with open("result.txt", "w") as file:
        file.write(stuff.format("\n", "\n"))

    with open("result.txt", mode="rb") as f:
        await member.send(
            embed=discord.Embed(
                title="Boost Bot",
                description=f"Thanks for using our services.",
                color=0x5598D2,
            ),
            file=discord.File(f),
        )

    return await ctx.edit(
        embed=discord.Embed(
            title="Boost Bot",
            description=f"Sent {amount}x tokens.",
            color=0x5598D2,
        )
    )


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="website", description="It will send a website link."
)
async def website(
    ctx,
):
    return await ctx.respond(
        embed=discord.Embed(
            title="Website",
            description=f"Website: {config['kys.lol']}",
            color=0x5598D2,
        )
    )


@bot.slash_command(guild_ids=config["dev-guilds"], name="pp", description="It will send the paypal.")
async def pp(
    ctx,
):
    return await ctx.respond(
        embed=discord.Embed(
            title="Paypal",
            description=f"PayPal: {config['pp']}",
            color=0x5598D2,
        )
    )


@bot.slash_command(guild_ids=config["dev-guilds"], name="ltc", description="It will send the litecoin address.")
async def ltc(
    ctx,
):
    return await ctx.respond(
        embed=discord.Embed(
            title="Litecoin",
            description=f"Litecoin: {config['ltc']}",
            color=0x5598D2,
        )
    )


@bot.slash_command(guild_ids=config["dev-guilds"], name="btc", description="It will send the bitcoin address.")
async def btc(
    ctx,
):
    return await ctx.respond(
        embed=discord.Embed(
            title="Bitcoin",
            description=f"Bitcoin: {config['bitcoin']}",
            color=0x5598D2,
        )
    )

class MyView(discord.ui.View):
    @discord.ui.button(label="", row=1, style=discord.ButtonStyle.grey, emoji='<:a_boost_blue:1161233858516222033>')
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="__Boost Commands__",
            description="**/boost | /restock | /stock | /sendtokens**",
            color=0x5598D2,
        ))
    @discord.ui.button(label="", row=1, style=discord.ButtonStyle.grey, emoji="<:Utility:1161242180757758064>")
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title='__Others Commands__',
            description='**/pp | /btc | /ltc | /ca | /website**',
            color=0x5598D2,
        ))
    @discord.ui.button(label="", row=1, style=discord.ButtonStyle.grey, emoji="<:KingC:1161241153245552751>")
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title='__Owner Commands__',
            description='**/addadmin | /addowner**',
            color=0x5598D2,
        ))

@bot.slash_command(guild_ids=config["dev-guilds"], name="help", description="It will show the help menu.")
async def help(ctx):
    await ctx.respond(
        embed=discord.Embed(
            title="Help Menu",
            description="**It will show the bot all commands!**",
            color=0x5598D2
            ),
            view=MyView()
    )


@bot.slash_command(guild_ids=config["dev-guilds"], name="ca", description="It will send the cashapp.")
async def ca(
    ctx,
):
    return await ctx.respond(
        embed=discord.Embed(
            title="Cashapp",
            description=f"CashApp: {config['cashapp']}",
            color=0x5598D2,
        )
    )


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="addowner", description="Add a member as a owner."
)
async def addowner(
    ctx,
    member: discord.Option(discord.Member, "The member you want to add.", required=True),
):
    await ctx.defer(ephemeral=False)
    if str(ctx.author.id) not in config["owners"]:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="You cannot use this command.",
                color=0xC80000,
            )
        )

    config["owners"].append(str(member.id))
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return await ctx.edit(
        embed=discord.Embed(
            title="Boost Bot",
            description=f"Added owner successfully",
            color=0x5598D2,
        )
    )


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="stock", description="Display the stock of boosts and tokens."
)
async def stock(
    ctx,
    type: discord.Option(int, "Number of months (1/3).", required=True),
):
    await ctx.defer(ephemeral=False)

    if type != 1 and type != 3 and type != 0:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Invalid type. [1/3] are valid inputs.",
                color=0xC80000,
            )
        )

    if type == 1:
        fileName = "data/1m.txt"
    elif type == 3:
        fileName = "data/3m.txt"

    stock = len(open(fileName, "r").readlines())

    return await ctx.edit(
        embed=discord.Embed(
            title=f"**__{type} months tokens__**",
            description=f"\n -> ``We have`` **{stock}** ``tokens and`` **{stock * 2}** ``boosts in stock``",
            color=0x5598D2,
        )
    )


@bot.slash_command(
    guild_ids=config["dev-guilds"], name="restock", description="Add the tokens in the stock."
)
async def restock(
    ctx,
    type: discord.Option(int, "Number of months (1/3).", required=True),
    file: discord.Option(discord.Attachment, "Attachment", required=True),
):
    await ctx.defer(ephemeral=False)

    if (
        str(ctx.author.id) not in config["owners"]
        and str(ctx.author.id) not in config["admins"]
    ):
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Missing permissions, you cannot use this command.",
                color=0xC80000,
            )
        )

    if type != 1 and type != 3 and type != 0:
        return await ctx.respond(
            embed=discord.Embed(
                title="**ERROR**",
                description="Invalid type. [1/3] are valid inputs.",
                color=0xC80000,
            )
        )

    if type == 1:
        fileName = "data/1m.txt"
    elif type == 3:
        fileName = "data/3m.txt"

    content = await file.read()

    stuff = content.decode().split("\r\n")
    before = getStock(fileName)

    for x in range(len(before)):
        stuff.append(before[x])

    cute = "\n".join(stuff)
    text = cute.replace("b'", "").replace("'", "")

    print(text)

    with open(fileName, "w") as file:
        file.write(text + "\n")

    return await ctx.edit(
        embed=discord.Embed(
            title="Boost Bot",
            description=f"Restocked successfully",
            color=0x5598D2,
        )
    )


orders_sellapp = []
orders_sellix = []


@app.route("/sellix", methods=["POST"])
def sellix():
    data = request.json
    if data in orders_sellix:
        pass
    elif data not in orders_sellix:
        threading.Thread(
            target=sellixshit,
            args=[
                data,
            ],
        ).start()
        orders_sellix.append(data)
    return jsonify({"message": f"We've recieved your order"}), 200


def sellixshit(data):
    """"""
    invite = ""
    title = data["data"]["product_title"].lower()

    split_parts = title.split(" | ")

    amount = int(split_parts[0].split()[0])
    months = int(split_parts[1].split()[0])

    if amount == None or months == None:
        return

    for i in data["data"]["custom_fields"]:
        if i == config["sellix"]["invite_field_name"]:
            invite = data["data"]["custom_fields"][i]

    order_id = data["data"]["uniqid"]
    email = data["data"]["customer_email"]
    product = data["data"]["product_title"]

    inviteCode = getinviteCode(invite)
    inviteData = checkInvite(inviteCode)

    embeds_data = {
        "embeds": [
            {
                "title": "**Sellix Order**",
                "description": f"**Order ID: **{order_id}\n**Email: **{email}\n**Product: **{product}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n**Invite: **[{inviteCode}](https://discord.gg/{inviteCode})",
            }
        ]
    }

    response = httpx.post(
        config["sellix"]["orders"],
        data=json.dumps(embeds_data),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 204:
        """"""
    else:
        print(response.json())

    if inviteData == False:
        return print(f"[ERROR]: Invalid invite was provided for order: {order_id}")

    if months == 1:
        filename = "data/1m.txt"
    if months == 3:
        filename = "data/3m.txt"

    tokensStock = getStock(filename)
    requiredStock = int(amount / 2)

    if requiredStock > len(tokensStock):
        return print(
            f"[ERROR]: We didn't had enough boosts to satisfy order: {order_id}"
        )

    tokens = []

    for x in range(requiredStock):
        tokens.append(tokensStock[x])
        remove(tokensStock[x], filename)

    cool = Booster()
    status = cool.thread(inviteCode, tokens, inviteData)
    success = status["success"]
    failed = status["failed"]

    print(
        f"{Fore.GREEN}[+]: Attempted to do {Fore.BLUE}{amount}x{Fore.RESET} {Fore.GREEN}boosts for {order_id} order id. {Fore.RESET} {Fore.CYAN}\n[-]: Successfully did {Fore.RESET}{len(success)}x boost. {Fore.CYAN}\n[-]: Failed to do {Fore.RESET}{len(failed)}x boosts.\n\n    Results \n[Success]: {success}\n[Failed]: {failed} \n\n"
    )

    completed_data = {
        "embeds": [
            {
                "title": "**Sellix Completion**",
                "description": f"**Order ID: **{order_id}\n**Email: **{email}\n**Product: **{product}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n**Invite: **[{inviteCode}](https://discord.gg/{inviteCode}) \n\n**[SUCCESS]**: {success} \n**[FAILED]**: {failed}",
            }
        ]
    }

    response = httpx.post(
        config["sellapp"]["orders"],
        data=json.dumps(completed_data),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 204:
        """"""
    else:
        print(response.json())


@app.route("/sellapp", methods=["POST"])
def sellapp():
    data = request.json
    order_id = data["invoice"]["id"]

    if order_id in orders_sellapp:
        pass
    elif order_id not in orders_sellapp:
        threading.Thread(
            target=sellshit,
            args=[
                data,
            ],
        ).start()
        orders_sellapp.append(order_id)
    return jsonify({"message": f"We've recieved your order"}), 200


def sellshit(data):
    """"""
    invite = ""

    for i in data["additional_information"]:
        if i["label"] == config["sellapp"]["invite_field_name"]:
            invite = i["value"]

    title = data["listing"]["title"]

    split_parts = title.split(" | ")

    amount = int(split_parts[0].split()[0])
    months = int(split_parts[1].split()[0])

    if amount == None or months == None:
        return

    inviteCode = getinviteCode(invite)
    inviteData = checkInvite(inviteCode)

    order_id = data["invoice"]["id"]
    email = data["invoice"]["payment"]["gateway"]["data"]["customer_email"]
    product = data["listing"]["title"]

    embeds_data = {
        "embeds": [
            {
                "title": "**SellApp Order**",
                "description": f"**Order ID: **{order_id}\n**Email: **{email}\n**Product: **{product}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n**Invite: **[{inviteCode}](https://discord.gg/{inviteCode})",
            }
        ]
    }

    response = httpx.post(
        config["sellapp"]["orders"],
        data=json.dumps(embeds_data),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 204:
        """"""
    else:
        print(response.json())

    if inviteData == False:
        return print(f"[ERROR]: Invalid invite was provided for order: {order_id}")

    if months == 1:
        filename = "data/1m.txt"
    if months == 3:
        filename = "data/3m.txt"

    tokensStock = getStock(filename)
    requiredStock = int(amount / 2)

    if requiredStock > len(tokensStock):
        return print(
            f"[ERROR]: We didn't had enough boosts to satisfy order: {order_id}"
        )

    tokens = []

    for x in range(requiredStock):
        tokens.append(tokensStock[x])
        remove(tokensStock[x], filename)

    cool = Booster()
    status = cool.thread(inviteCode, tokens, inviteData)
    success = status["success"]
    failed = status["failed"]

    print(
        f"{Fore.GREEN}[+]: Attempted to do {Fore.BLUE}{amount}x{Fore.RESET} {Fore.GREEN}boosts for {order_id} order id. {Fore.RESET} {Fore.CYAN}\n[-]: Successfully did {Fore.RESET}{len(success)}x boost. {Fore.CYAN}\n[-]: Failed to do {Fore.RESET}{len(failed)}x boosts.\n\n    Results \n[Success]: {success}\n[Failed]: {failed} \n\n"
    )

    completed_data = {
        "embeds": [
            {
                "title": "**SellApp Completion**",
                "description": f"**Order ID: **{order_id}\n**Email: **{email}\n**Product: **{product}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n**Invite: **[{inviteCode}](https://discord.gg/{inviteCode}) \n\n**[SUCCESS]**: {success} \n**[FAILED]**: {failed}",
            }
        ]
    }

    response = httpx.post(
        config["sellapp"]["orders"],
        data=json.dumps(completed_data),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 204:
        """"""
    else:
        print(response.json())

def serve():
    app.run(host="0.0.0.0", port=config["port"])

def startServer():
    server = threading.Thread(target=serve)
    server.start()

startServer();
bot.run(config["token"])