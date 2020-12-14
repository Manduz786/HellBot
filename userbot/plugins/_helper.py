import asyncio

import requests
from telethon import functions

from userbot import ALIVE_NAME, CMD_LIST, SUDO_LIST
from userbot.utils import admin_cmd, sudo_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Hell User"


@borg.on(admin_cmd(pattern=r"help ?(.*)", outgoing=True))
async def cmd_list(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "-", "_", "@"):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        input_str = event.pattern_match.group(1)
        if tgbotusername is None or input_str == "text":
            string = ""
            for i in CMD_LIST:
                string += "⚡️" + i + "\n"
                for iter_list in CMD_LIST[i]:
                    string += "    `" + str(iter_list) + "`"
                    string += "\n"
                string += "\n"
            if len(string) > 4095:
                with io.BytesIO(str.encode(string)) as out_file:
                    out_file.name = "cmd.txt"
                    await bot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="**COMMANDS** In __**Hêllẞø†**__",
                        reply_to=reply_to_id,
                    )
                    await event.delete()
            else:
                await event.edit(string)
        elif input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:\n".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "  " + i
                    string += "\n"
                await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            help_string = f"""Userbot Helper.. Provided by ✨{DEFAULTUSER}✨ \n
`Userbot Helper to reveal all the commands`\n__Do .help plugin_name for commands, in case popup doesn't appear.__"""
            results = await bot.inline_query(  # pylint:disable=E0602
                tgbotusername, help_string
            )
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()


@borg.on(admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())  # pylint:disable=E0602
    await event.edit(result.stringify())


@borg.on(admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)  # pylint:disable=E0602
    await event.edit("""Telethon UserBot Powered by @HellBot_Official""")


@borg.on(admin_cmd(pattern="syntax (.*)"))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)

    if plugin_name in CMD_LIST:
        help_string = CMD_LIST[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           @HellBot_Official"

        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:

        plugin_syntax = "Enter valid **Plugin** name.\nDo `.plinfo` or `.help` to get list of valid plugin names."

    await event.edit(plugin_syntax)


@bot.on(sudo_cmd(allow_sudo=True, pattern="help ?(.*)"))
async def info(event):
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = (
            "Total {count} commands found in {plugincount} sudo plugins of Hêllẞø†\n\n"
        )
        hellcount = 0
        plugincount = 0
        for i in sorted(SUDO_LIST):
            plugincount += 1
            string += f"{plugincount}) Commands found in Plugin " + i + " are \n"
            for iter_list in SUDO_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                hellcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=hellcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"All commands of the Hêllẞø† are [here]({url})"
            await event.reply(reply_text, link_preview=False)
            return
        await event.reply(
            string.format(count=hellcount, plugincount=plugincount), link_preview=False
        )
        return
    if input_str:
        if input_str in SUDO_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            hellcount = 0
            for i in SUDO_LIST[input_str]:
                string += f"  •  <code>{i}</code>"
                string += "\n"
                hellcount += 1
            await event.reply(
                string.format(count=hellcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            reply = await event.reply(input_str + " is not a valid plugin!")
            await asyncio.sleep(3)
            await event.delete()
            await reply.delete()
    else:
        string = "<b>Please specify which plugin do you want help for !!\
            \nNumber of plugins : </b><code>{count}</code>\
            \n<b>Usage:</b> <code>.help plugin name</code>\n\n"
        hellcount = 0
        for i in sorted(SUDO_LIST):
            string += "≈ " + f"<code>{str(i)}</code>"
            string += " "
            hellcount += 1
        await event.reply(string.format(count=hellcount), parse_mode="HTML")
