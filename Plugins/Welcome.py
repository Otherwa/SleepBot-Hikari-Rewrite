from datetime import datetime
import hikari
import lightbulb
import random
import Utils
from lightbulb import checks
from lightbulb.command_handler import Bot
from typing import Optional

class Welcome(lightbulb.Plugin):
	def __init__(self, bot : Bot) -> None:
		self.bot = bot
		super().__init__()
	
	def WelcomeEmbed(self, target : hikari.User) -> hikari.Embed:
		welcomeEmbed = hikari.Embed(
			title = "Welcome to the Bluelearn Discord Server!",
			description = "Make sure that you have a **verified email connected to your account** so that you can interact in the server. \nHere are a few things that you can do:",
			color = random.randint(0, 0xffffff),
			url = 'https://www.bluelearn.in/'
		).add_field(
			name = "Read the rules",
			value = "Read the rules in the `Rules channel mention here` channel carefully"
		).add_field(
			name = "Check out the Server Guide Video",
			value = "If you are new to discord, you can watch a tutorial video which will help you to go about the server.\n**Tutorial:** [Click here](https://youtu.be/AUimFYOBXYU?t=291)"
		).add_field(
			name = "Getting to Know You",
			value = "Please fill up this form so that we know your interests and can make the community better! **[Click here](https://forms.gle/5Zhums746RWRcAhu7)**"
		).set_image(
			'https://res.cloudinary.com/zeusabhijeet/image/upload/v1624014516/Clinify%20Stuff/Bluelearn_welcome_banner_1.gif'
		).set_author(
			name = target.username,
			icon = target.avatar_url
		)
		return welcomeEmbed
	
	@lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
	@lightbulb.command(name = 'welcomedm', aliases = ['welcomeDM'])
	async def welcome_dm_command(self, ctx : lightbulb.Context, target : Optional[hikari.User] = None):
		"""Send the Welcomer DM to the mentioned user. If not mentioned then sends to the author."""
		if target is None:
			target = ctx.author
		
		await target.send(embed = self.WelcomeEmbed(target))
		await ctx.respond(f"Successfully sent DM to {target.mention}")
	
	@lightbulb.listener(hikari.MemberCreateEvent)
	async def on_member_join(self, event : hikari.MemberCreateEvent):
		await event.member.send(embed = self.WelcomeEmbed(event.user))
		await self.bot.rest.create_message(
			Utils.LOGCHANNELID,
			embed = hikari.Embed(
				title = "SleepBot Welcome DM Log",
				description = f"Sent DM Message Successfully to: Username : {event.member} ; ID : {event.user_id} at {datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}",
				colour = random.randint(0, 0xffffff) 
			)
		)

def load(bot : Bot):
	bot.add_plugin(Welcome(bot))
	print("Plugin Welcome has been loaded")

def unload(bot : Bot):
	bot.remove_plugin("Welcome")