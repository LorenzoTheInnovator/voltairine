import asyncio
import unittest

from unittest import mock

from voltairine import on_ready, on_message, help_msg
import voltairine
# class TestCows(unittest.TestCase):
#     def test_cowsay(self):
#         pass

async def do_nothing_msg(channel, msg):
    await asyncio.sleep(0)

async def do_nothing_wait(author=None):
    await asyncio.sleep(0)


@mock.patch("voltairine.reply")
@mock.patch('voltairine.learn')
class BulkTestResponses(unittest.TestCase):
    settings = {
        "pyborg": {"learning": True, "multiplex": True, 
                   "server": "localhost", "port": 2001},
        "token": "foo"
    }
    @mock.patch('discord.Client.user', create=True, return_value="221134985560588289")
    @mock.patch("toml.load")
    @mock.patch("discord.Client.send_message", wraps=do_nothing_msg)
    def test_responses(self, patched_learn, patched_reply, patched_send, patched_toml, patched_user):
        patched_toml.return_value = self.settings
        commands = help_msg.split("\n")
        # commands = ['!4chan', "!benned3"]
        for command in commands:
            # if command in ["!help", "!cowsay", "!cowthink"]:
            #     print("cowardly not testing these")
            if not command.startswith("!encounter"):
                msg = mock.MagicMock()
                type(msg).content = mock.PropertyMock(return_value=command)
                msg.channel.return_value = "maketotaldestroy"
                msg.message.author.return_value = "somefucko"
                print("calling {}".format(command))
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(on_message(msg))
                loop.close()
                last_call = patched_send.call_args
                print(last_call)
                if last_call:
                    self.assertIsInstance(last_call[0][1], str)

    @mock.patch('discord.Client.user', create=True, return_value="221134985560588289")
    @mock.patch("toml.load")
    @mock.patch("discord.Client.send_message", wraps=do_nothing_msg)
    def test_pyborg(self, patched_learn, patched_reply, patched_send, patched_toml, patched_user):
        msg = mock.MagicMock()
        type(msg).content = mock.PropertyMock(return_value="Welcome to my twisted mind! lol rawr")
        msg.channel.return_value = "maketotaldestroy"
        msg.message.author.return_value = "somefucko"
