import discord
from random import randint


class MyClient(discord.Client):
    @staticmethod
    async def give_role(role_name, author, channel=None):
        guild = author.guild

        all_roles = guild.roles
        all_roles_names = [role.name.lower().strip() for role in all_roles]
        all_roles_id = {role.name.lower().strip(): role.id for role in all_roles}

        if role_name in all_roles_names:
            role_id = all_roles_id[role_name]
            role = guild.get_role(role_id)

            if str(role.color) == "#000000":
                if role in author.roles:
                    await channel.send("У вас уже есть эта роль")
                    return

                await author.add_roles(role)
                if channel:
                    await channel.send("Роль успешно выдана!")
                return
            
            await channel.send("Эту роль нельзя получить таким способом")
            return

        await channel.send("Такой роли нет")


    @staticmethod
    async def create_role(role_name, author, channel):
        guild = author.guild

        all_roles = guild.roles
        all_roles_names = [role.name.lower().strip() for role in all_roles]
        all_roles_id = {role.name.lower().strip(): role.id for role in all_roles}

        if all_roles_id["старший член консилиума"] not in [role.id for role in author.roles]:
            await channel.send("У вас недостаточно прав для использования этой команды!")
            return

        if role_name.lower() in all_roles_names:
            await channel.send("Такая роль уже существует")
            return

        role = await guild.create_role(name=role_name, colour=discord.Colour(0x000000))
        await channel.send("Роль успешно создана!")

        categories = guild.categories
        categories_by_name = {cat.name.lower(): cat for cat in categories}

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True),
            }

        await guild.create_voice_channel(role_name, overwrites=overwrites, category=categories_by_name["гамание"])
        await channel.edit(topic=channel.topic + "\n* " + role_name)


    @staticmethod
    async def create_poll(text, channel, ticks, crosses):
        total_votes = ticks + crosses
        text += "\nЗА\t\t\t\t| " + "#" * int(30 * ticks / total_votes) + "\n" + "ПРОТИВ\t | " + "#" * int(30 * crosses / total_votes)

        await channel.send(text)


    @staticmethod
    async def roll_dice(channel, sides=6):
        number = randint(1, sides)
        await channel.send(f"Выпало {number}")


    def __init__(self):
        super().__init__()
       # intents = discord.Intents.default()
       # intents.messages = True
       # discord.Intents = intents
       # intents.reactions = True
        print("Connecting...")


    @staticmethod
    async def on_connect():
        print("Successfully connected to server!\n")
        print("Preparing...")


    @staticmethod
    async def on_ready():
        print("Ready to execute commands!\n")


    async def on_message(self, message):
        if message.author == client.user:
            return

        author = message.author
        content = message.content
        channel = message.channel

        if str(message.channel) == "получение-роли":
            if content.lower().startswith("!роль ") or content.lower().startswith("! роль"):
                role_name = content.lower().removeprefix("! роль").removeprefix("!роль").strip()
                
                await self.give_role(role_name, author, channel)
                return


            if content.lower().startswith("!создать") or content.lower().startswith("! создать"):
                role_name = content.removeprefix("!создать").removeprefix("! создать").strip()

                await self.create_role(role_name, author, channel)
                return


        if content.strip().lower() in {"!кубик", "! кубик"}:
            await self.roll_dice(channel)
            return

'''
        if content.strip().lower().startswith("!голосование") or content.strip().lower().startswith("! голосование"):
            await message.delete()

            text = "\n".join(content.split("\n")[1:])
            await self.create_poll(text, channel, 1, 1)


    async def on_reaction_add(self, reaction, user):
        print(0)


    async def on_member_join(self, member):
        await self.give_role("кандидат", member)
'''


if __name__ == "__main__":
    client = MyClient()
    client.run('OTY1MjkyODE3NTMyNDczMzg0.YlxE_Q.oaMXtaEXsfvgQabAlU4ciWcosTE')
