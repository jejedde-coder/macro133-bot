import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORY_ID = 1559937702621872198

# Helper function to create a ticket channel
async def create_ticket(interaction, game_name, prefix):
    await interaction.response.send_message("⏳ Creating your ticket, please wait...", ephemeral=True)
    
    guild = interaction.guild
    member = interaction.user
    channel_name = f"{prefix}-ticket-{member.name.lower()}"
    
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    if existing_channel:
        await interaction.edit_original_response(content=f"You already have an open ticket: {existing_channel.mention}")
        return

    category = guild.get_channel(CATEGORY_ID)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    
    try:
        ticket_channel = await guild.create_text_channel(
            channel_name, 
            overwrites=overwrites, 
            category=category
        )
        await ticket_channel.send(f"{member.mention} Welcome! Please state your mouse model for the **{game_name}** script.")
        await interaction.edit_original_response(content=f"✅ Ticket created successfully! Head over to {ticket_channel.mention}.")
    except discord.Forbidden:
        await interaction.edit_original_response(content="❌ Error: The bot is missing **Manage Channels** permission on this server or inside this category!")

# Master Shop View (All 5 buttons together)
class AllGamesShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apex Legends", style=discord.ButtonStyle.green, emoji="🎮", row=0, custom_id="shop_apex_btn")
    async def apex_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Apex Legends", "apex")

    @discord.ui.button(label="Counter-Strike 2", style=discord.ButtonStyle.green, emoji="🎯", row=0, custom_id="shop_cs2_btn")
    async def cs2_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Counter-Strike 2", "cs2")

    @discord.ui.button(label="PUBG", style=discord.ButtonStyle.green, emoji="🪖", row=1, custom_id="shop_pubg_btn")
    async def pubg_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "PUBG", "pubg")

    @discord.ui.button(label="WARDOGS", style=discord.ButtonStyle.green, emoji="🛡️", row=1, custom_id="shop_wardogs_btn")
    async def wardogs_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "WARDOGS", "wardogs")

    @discord.ui.button(label="Delta Force", style=discord.ButtonStyle.green, emoji="🔫", row=1, custom_id="shop_delta_btn")
    async def delta_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Delta Force", "deltaforce")

# Individual Ticket Views (For individual !game commands)
class ApexTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket_apex_single")
    async def cb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Apex Legends", "apex")

class Cs2TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket_cs2_single")
    async def cb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Counter-Strike 2", "cs2")

class PubgTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket_pubg_single")
    async def cb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "PUBG", "pubg")

class WardogsTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket_wardogs_single")
    async def cb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "WARDOGS", "wardogs")

class DeltaTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket_delta_single")
    async def cb(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "Delta Force", "deltaforce")

@bot.event
async def on_ready():
    bot.add_view(AllGamesShopView())
    bot.add_view(ApexTicketView())
    bot.add_view(Cs2TicketView())
    bot.add_view(PubgTicketView())
    bot.add_view(WardogsTicketView())
    bot.add_view(DeltaTicketView())
    print(f"Logged in successfully as {bot.user}!")

# Individual Game Commands (with GIFs)
@bot.command(name='apex')
async def apex_script(ctx):
    file = discord.File("apex.gif", filename="apex.gif")
    embed = discord.Embed(title="🎮 Apex Legends Script", description="Universal Compatibility : working with any mouse and any gun", color=0xff5500)
    embed.add_field(name="Notice", value="✅ UNDETECTED", inline=True)
    embed.add_field(name="Status", value="🟢 In Stock", inline=True)
    embed.set_image(url="attachment://apex.gif")
    await ctx.send(file=file, embed=embed, view=ApexTicketView())

@bot.command(name='cs2')
async def cs2_script(ctx):
    file = discord.File("cs2.gif", filename="cs2.gif")
    embed = discord.Embed(title="🎯 Counter-Strike 2 Script", description="Universal Compatibility : working with any mouse and any gun", color=0xff5500)
    embed.add_field(name="Notice", value="✅ UNDETECTED", inline=True)
    embed.add_field(name="Status", value="🟢 In Stock", inline=True)
    embed.set_image(url="attachment://cs2.gif")
    await ctx.send(file=file, embed=embed, view=Cs2TicketView())

@bot.command(name='pubg')
async def pubg_script(ctx):
    file = discord.File("pubg.gif", filename="pubg.gif")
    embed = discord.Embed(title="🪖 PUBG Script", description="Universal Compatibility : working with any mouse and any gun", color=0xff5500)
    embed.add_field(name="Notice", value="✅ UNDETECTED", inline=True)
    embed.add_field(name="Status", value="🟢 In Stock", inline=True)
    embed.set_image(url="attachment://pubg.gif")
    await ctx.send(file=file, embed=embed, view=PubgTicketView())

@bot.command(name='wardogs')
async def wardogs_script(ctx):
    file = discord.File("wardogs.gif", filename="wardogs.gif")
    embed = discord.Embed(title="🛡️ WARDOGS Script", description="Universal Compatibility : working with any mouse and any gun", color=0xff5500)
    embed.add_field(name="Notice", value="✅ UNDETECTED", inline=True)
    embed.add_field(name="Status", value="🟢 In Stock", inline=True)
    embed.set_image(url="attachment://wardogs.gif")
    await ctx.send(file=file, embed=embed, view=WardogsTicketView())

@bot.command(name='deltaforce')
async def deltaforce_script(ctx):
    file = discord.File("deltaforce.gif", filename="deltaforce.gif")
    embed = discord.Embed(title="🔫 Delta Force Script", description="Universal Compatibility : working with any mouse and any gun", color=0xff5500)
    embed.add_field(name="Notice", value="✅ UNDETECTED", inline=True)
    embed.add_field(name="Status", value="🟢 In Stock", inline=True)
    embed.set_image(url="attachment://deltaforce.gif")
    await ctx.send(file=file, embed=embed, view=DeltaTicketView())

# Master Ticket Panel Command (Posts just the 5 buttons together)
@bot.command(name='tickets', aliases=['ticketpanel'])
async def tickets_panel(ctx):
    await ctx.send("🎫 **Support Ticket Panel**\nSelect a game below to open a private ticket:", view=AllGamesShopView())

bot.run("MTU3MTc3NTI2MTE2NTQ5MDE3Ng.G8p5oT.tcJ_-pcUIazvnuk1D2sNvryQ20Xw19VnxWeb3I")