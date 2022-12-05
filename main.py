import os
import re
import sys
import interactions
import json
import logger
from Event import *
from interactions.ext.tasks import IntervalTrigger, create_task

if os.path.isfile('config.json'):
    with open('config.json', 'r') as file:
        config = json.load(file)
else:
    file = open("config.json", 'w+')
    file.write('{\n  "token": ""\n}')
    print("Вставьте токен в сформированный config.json файл и перезапустите программу.")
    sys.exit()

bot = interactions.Client(
    token=config['token'],
)

users = dict()
events = []

# user = await bot.guilds[0].get_member(id)


@bot.command(
    name="create_meeting",
    description="Create new meeting",
    default_scope=False,
)
async def create_meeting(ctx: interactions.CommandContext):
    logger.default_log("Initiate meeting creating")
    modal = interactions.Modal(
        title="Создание мероприятия",
        custom_id="create_form",
        components=[interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Название",
            custom_id="meeting_name",
            min_length=2,
            max_length=20,
        ), interactions.TextInput(
            style=interactions.TextStyleType.PARAGRAPH,
            label="Описание",
            custom_id="meeting_description",
            required=False,
        ), interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Время",
            custom_id="meeting_time",
            required=True,
            placeholder="00:00",
            min_length=5,
            max_length=5,
        ), interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Дата",
            custom_id="meeting_date",
            required=True,
            placeholder="09.11.1986",
            min_length=10,
            max_length=10,
        ), interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Максимальное кол-во участников",
            custom_id="people_count",
            required=True,
            max_length=1,
        )# interactions.TextInput(
        #    style=interactions.TextStyleType.PARAGRAPH,
        #    label="Роли",
        #    custom_id="roles",
        #    required=True,
        #    placeholder=f"Введите роли через {config['separator']}",
        #    max_length=100,
        #)
        ]
    )
    await ctx.popup(modal)
    logger.default_log("Meeting creating complete")


@bot.modal("create_form")
async def create_response(ctx: interactions.CommandContext, meet_name: str, meet_description: str, meet_time: str, meet_date: str, people_count: str):
    logger.default_log("Initiate meeting modal creating")
    if re.fullmatch(r"\d\d:\d\d", meet_time) is None:
        logger.default_log("Input error: Bad time")
        await ctx.send(":no_entry:ОШИБКА: Неправильный ввод времени. Пример: 15:01", ephemeral=True)
        return
    if re.fullmatch(r"\d\d\.\d\d\.\d{4}", meet_date) is None:
        logger.default_log("Input error: Bad date")
        await ctx.send(":no_entry:ОШИБКА: Неправильный ввод даты. Пример: 01.01.1960", ephemeral=True)
        return
    if not people_count.isdigit():
        logger.default_log("Input error: Bad count users")
        await ctx.send(":no_entry:ОШИБКА: Неправильный ввод числа участников. Пример: 6", ephemeral=True)
        return
    if meet_description == "":
        meet_description = "Описание отсутствует"
    buttons = [interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Titan",
        custom_id="BtnTitan"
    ), interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Hunter",
        custom_id="BtnHunter"
    ), interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Warlock",
        custom_id="BtnWarlock",
    ), interactions.Button(
        style=interactions.ButtonStyle.SECONDARY,
        label="Late",
        custom_id="BtnLate",
    ), interactions.Button(
        style=interactions.ButtonStyle.SECONDARY,
        label="50/50",
        custom_id="Btn50/50",
    )]
    row = interactions.ActionRow(components=buttons)

    embed_fields = [interactions.EmbedField(
        name="Название",
        value=meet_name,
    ), interactions.EmbedField(
        name="Описание",
        value=meet_description,
    ), interactions.EmbedField(
        name="Дата",
        value=meet_date,
        inline=True
    ), interactions.EmbedField(
        name="Время",
        value=meet_time,
        inline=True,
    ), interactions.EmbedField(
        name="Люди",
        value="0/" + people_count,
        inline=True,
    ), interactions.EmbedField(
        name="Titan",
        value="-",
    ), interactions.EmbedField(
        name="Hunter",
        value="-",
    ), interactions.EmbedField(
        name="Warlock",
        value="-",
    )]

    embed = interactions.Embed(
        title="----------Мероприятие----------",
        author=interactions.EmbedAuthor(
            name="Лидер: " + ctx.member.name + " ID: " + str(ctx.user.id)
        ),
        color=15548997,
        fields=embed_fields,
        footer=interactions.EmbedFooter(
            text="Bench: -\n50/50: -",
        ),
    )
    logger.default_log("Modal created")
    await ctx.send(embeds=embed, components=row)
    logger.default_log("Modal sent")
    sep_datetime = meet_date.split('.')
    sep_datetime += meet_time.split(':')
    events.append(Event(ctx.message.id, datetime.datetime(day=int(sep_datetime[0]), month=int(sep_datetime[1]), year=int(sep_datetime[2]), hour=int(sep_datetime[3]), minute=int(sep_datetime[4])), meet_name))
    logger.default_log("Meeting created")


async def events_handler():
    logger.default_log("Meetings time check started")
    now = datetime.datetime.now()
    for event in events:
        if event.datetime.year == now.year and event.datetime.month == now.month and event.datetime.day == now.day:
            if event.datetime.hour == (now + datetime.timedelta(minutes=30)).hour and event.datetime.minute == (now + datetime.timedelta(minutes=30)).minute:
                for user in event.members:
                    await user.send(f"Вы записаны на мероприятие {event.name} которое пройдет {event.datetime}. Оно начинается через 30 минут!")
            elif event.datetime.hour == (now + datetime.timedelta(minutes=15)).hour and event.datetime.minute == (now + datetime.timedelta(minutes=15)).minute:
                for user in event.members:
                    await user.send(f"Вы записаны на мероприятие {event.name} которое пройдет {event.datetime}. Оно начинается через 15 минут!")
            elif event.datetime.hour == (now + datetime.timedelta(minutes=5)).hour and event.datetime.minute == (now + datetime.timedelta(minutes=5)).minute:
                for user in event.members:
                    await user.send(f"Вы записаны на мероприятие {event.name} которое пройдет {event.datetime}. Оно начинается через 5 минут!")
        elif now > event.datetime:
            events.remove(event)
            logger.default_log(f"Event {event.name}:{event.id} deleted")
    logger.default_log("Meetings time check ended")


def member_activity(ctx: interactions.CommandContext, field_number: int):
    embed = ctx.message.embeds[0]
    nick_user = users.get(ctx.user.id)
    fields = [5, 6, 7]
    fields.remove(field_number)
    if nick_user is None:
        logger.default_log(f"User {ctx.user.id} not found")
        if int(embed.fields[4].value[0]) == int(embed.fields[4].value[2]):
            footer_text = embed.footer.text.split('\n')
            footer_text[0] += ctx.member.name + ", "
            embed.footer.text = footer_text[0] + "\n" + footer_text[1]
        else:
            embed.fields[field_number].value += ctx.member.name + ", "
            embed.fields[4].value = str(int(embed.fields[4].value[0]) + 1) + embed.fields[4].value[1:]
        users[ctx.user.id] = ctx.member.name
        logger.default_log(f"User {ctx.user.id}: {ctx.member.name} created and subscribed")
        for event in events:
            if event.id == ctx.message.id:
                print("Member added to event")
                event.members.append(ctx.user)
    elif nick_user in embed.fields[field_number].value.split(",") or nick_user == embed.fields[field_number].value[1:-1]:
        embed.fields[field_number].value = embed.fields[field_number].value.replace(nick_user + ",", '')
        embed.fields[4].value = str(int(embed.fields[4].value[0]) - 1) + embed.fields[4].value[1:]
        for event in events:
            if event.id == ctx.message.id:
                print("Member removed from event")
                event.members.remove(ctx.user)
        logger.default_log(f"User {ctx.member.name}:{ctx.user.id} unsubscribed")
    else:
        if int(embed.fields[4].value[0]) == int(embed.fields[4].value[2]) and nick_user not in embed.fields[fields[0]].value and nick_user not in embed.fields[fields[1]].value:
            footer_text = embed.footer.text.split('\n')
            footer_text[0] += ctx.member.name + ", "
            embed.footer.text = footer_text[0] + "\n" + footer_text[1]
        else:
            if nick_user not in embed.fields[fields[0]].value and nick_user not in embed.fields[fields[1]].value:
                embed.fields[4].value = str(int(embed.fields[4].value[0]) + 1) + embed.fields[4].value[1:]
            embed.fields[field_number].value += ctx.member.name + ","
            embed.fields[fields[0]].value = embed.fields[fields[0]].value.replace(nick_user + ",", '')
            embed.fields[fields[1]].value = embed.fields[fields[1]].value.replace(nick_user + ",", '')
            footer_text = embed.footer.text.split('\n')
            footer_text[0] = footer_text[0].replace(nick_user + ",", '')
            footer_text[1] = footer_text[1].replace(nick_user + ",", '')
            embed.footer.text = footer_text[0] + "\n" + footer_text[1]
        users[ctx.user.id] = ctx.member.name
        for event in events:
            if event.id == ctx.message.id:
                if ctx.user not in event.members:
                    print("Member added to event")
                    event.members.append(ctx.user)
        logger.default_log(f"User {ctx.member.name}:{ctx.user.id} subscribed")
    return embed


def secondary_activity(ctx: interactions.CommandContext, field_number: int):
    embed = ctx.message.embeds[0]
    nick_user = users.get(ctx.user.id)
    footer_text = embed.footer.text.split('\n')
    if nick_user is None:
        logger.default_log(f"User {ctx.user.id} not found")
        footer_text[field_number] += ctx.member.name + ","
        users[ctx.user.id] = ctx.member.name
        logger.default_log(f"User {ctx.member.name}:{ctx.user.id} created and subscribed")
        for event in events:
            if event.id == ctx.message.id:
                print("Member added to event")
                event.members.append(ctx.user)
    elif nick_user in footer_text[field_number]:
        footer_text[field_number] = footer_text[field_number].replace(nick_user + ",", '')
        for event in events:
            if event.id == ctx.message.id:
                print("Member removed from event")
                event.members.remove(ctx.user)
        logger.default_log(f"User {ctx.member.name}:{ctx.user.id} unsubscribed")
    else:
        footer_text[field_number] += ctx.member.name + ","
        if nick_user in (embed.fields[5].value[1:] + 'a').split(',') + (embed.fields[6].value[1:] + 'a').split(',') + (embed.fields[7].value[1:] + 'a').split(','):
            embed.fields[5].value = embed.fields[5].value.replace(nick_user + ",", '')
            embed.fields[6].value = embed.fields[6].value.replace(nick_user + ",", '')
            embed.fields[7].value = embed.fields[7].value.replace(nick_user + ",", '')
            embed.fields[4].value = str(int(embed.fields[4].value[0]) - 1) + embed.fields[4].value[1:]
        footer_text[1 - field_number] = footer_text[1 - field_number].replace(nick_user + ",", '')
        users[ctx.user.id] = ctx.member.name
        for event in events:
            if event.id == ctx.message.id:
                if ctx.user not in event.members:
                    print("Member added to event")
                    event.members.append(ctx.user)
        logger.default_log(f"User {ctx.member.name}:{ctx.user.id} subscribed")
    embed.footer.text = footer_text[0] + "\n" + footer_text[1]
    return embed


@bot.component("BtnTitan")
async def response(ctx: interactions.CommandContext):
    logger.default_log(f"Titan pressed by {ctx.user.username}:{ctx.user.id}")
    await ctx.message.edit(embeds=member_activity(ctx, 5), components=ctx.message.components)
    await ctx.send("Успешно", ephemeral=True)


@bot.component("BtnHunter")
async def response(ctx: interactions.CommandContext):
    logger.default_log(f"Hunter pressed by {ctx.user.username}:{ctx.user.id}")
    await ctx.message.edit(embeds=member_activity(ctx, 6), components=ctx.message.components)
    await ctx.send("Успешно", ephemeral=True)


@bot.component("BtnWarlock")
async def response(ctx: interactions.CommandContext):
    logger.default_log(f"Warlock pressed by {ctx.user.username}:{ctx.user.id}")
    await ctx.message.edit(embeds=member_activity(ctx, 7), components=ctx.message.components)
    await ctx.send("Успешно", ephemeral=True)


@bot.component("BtnLate")
async def response(ctx: interactions.CommandContext):
    logger.default_log(f"Late pressed by {ctx.user.username}:{ctx.user.id}")
    await ctx.message.edit(embeds=secondary_activity(ctx, 0), components=ctx.message.components)
    await ctx.send("Успешно", ephemeral=True)


@bot.component("Btn50/50")
async def response(ctx: interactions.CommandContext):
    logger.default_log(f"50/50 pressed by {ctx.user.username}:{ctx.user.id}")
    await ctx.message.edit(embeds=secondary_activity(ctx, 1), components=ctx.message.components)
    await ctx.send("Успешно", ephemeral=True)


@create_task(IntervalTrigger(60))
async def main_loop():
    await events_handler()


#for i in range(10):
#    @bot.component(f"event_button{i}")
#    async def prime_response(ctx: interactions.CommandContext):
#        print(f"Button {i} used!")
#        if ctx.user.username in ctx.message.embeds[0].fields[3 + i].value:
#            embed = ctx.message.embeds[0]
#            embed.fields[3 + i].value = embed.fields[3 + i].value.replace(ctx.user.username, '')
#        else:
#            embed = ctx.message.embeds[0]
#            embed.fields[3 + i].value += " " + ctx.user.username
#        await ctx.message.edit(embeds=embed, components=ctx.message.components)


@bot.event
async def on_ready():
    logger.default_log(f"Bot logged as {bot.me.name}")
    main_loop.start()

bot.start()
