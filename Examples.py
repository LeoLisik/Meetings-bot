import interactions

bot = interactions.Client(
    token=""
)


@bot.command(
    name="my_first_command",
    description="This is the first command I made!",
)
async def example_simple_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

##############################################


@bot.command(
    name="say_something",
    description="say something!",
    default_scope=False,
    options=[
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def example_option(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")

##############################################


@bot.command(
    name="base_command",
    description="This description isn't seen in UI (yet?)",
    default_scope=False,
    options=[
        interactions.Option(
            name="command_name",
            description="A descriptive description",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="option",
                    description="A descriptive description",
                    type=interactions.OptionType.INTEGER,
                    required=False,
                ),
            ],
        ),
        interactions.Option(
            name="second_command",
            description="A descriptive description",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="second_option",
                    description="A descriptive description",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ],
        ),
    ],
)
async def cmd(ctx: interactions.CommandContext, sub_command: str, second_option: str = "", option: int = None):
    if sub_command == "command_name":
        await ctx.send(f"You selected the command_name sub command and put in {option}")
    elif sub_command == "second_command":
        await ctx.send(f"You selected the second_command sub command and put in {second_option}")

##############################################


@bot.command(
    type=interactions.ApplicationCommandType.USER,
    name="User Command",
    default_scope=False,
)
async def test(ctx):
    await ctx.send(f"You have applied a command onto user {ctx.target.user.username}!")

##############################################

button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="hello world!",
    custom_id="hello"
)


@bot.command(
    name="button_test",
    description="This is the first command I made!",
    default_scope=False,
)
async def button_test(ctx):
    await ctx.send("testing", components=button)


@bot.component("hello")
async def button_response(ctx):
    await ctx.send("You clicked the Button :O", ephemeral=True)

#####################################


@bot.command(
    name="mathematica",
    description="desk",
    default_scope=False,
)
async def my_cool_modal_command(ctx):
    modal = interactions.Modal(
        title="Application Form",
        custom_id="mod_app_form",
        components=[interactions.TextInput(
            style=interactions.TextStyleType.SHORT,
            label="Let's get straight to it: what's 1 + 1?",
            custom_id="text_input_response",
            min_length=1,
            max_length=3,
        )]
    )

    await ctx.popup(modal)


@bot.modal("mod_app_form")
async def modal_response(ctx, response: str):
    await ctx.send(f"You wrote: {response}", ephemeral=True)
