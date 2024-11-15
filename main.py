from telethon import TelegramClient, events
import asyncio
import time

# Replace these with your own values
API_ID = '23957241'  # Your API ID
API_HASH = 'c806d41322a1d13b32e910b39c138fc8'  # Your API Hash
SESSION_STRING = '1BVtsOJgBu46oxM2FjD64dZxr3zQWbloyopB-jRND5tOhzr21Ov1ghZgEw1JVfdwEapswKVC0m7dfj9YcC2R2CUK6zaV-STGdmA_cdQ6aHVzZf530n94xhcD6lE5xCFmtxyrdNQoD-4i71rMHW1alJiLEJQMujlku4CBb-7Lhu0QFugT9h_9K1DAglQWjBjMKw1_BM6KizWkJMprmC8LPZxxFycPzM1p1xIrve_EUJVclIWEal-RRoEVQhTMpmnfzZGBS7_Dynv7qMNIQpC36ZiFIid0z_oce9pesuR3zlCaiaeKLZhQN6-REg_Dj6gqlE2JuRjQWcMJJhmQvx8YvkebV43ZoaXo='  # Your session string for the bot
TARGET_CHANNEL = '@privateherox'  # The channel to monitor
FORWARD_INTERVAL = 1200 # Time interval (in seconds) to forward messages

# Create the client
client = TelegramClient(SESSION_STRING, API_ID, API_HASH)

# Store messages to be forwarded
messages_to_forward = []

async def fetch_latest_messages():
    global messages_to_forward
    async for message in client.iter_messages(TARGET_CHANNEL, limit=5):
        if message.message and message.id not in [msg.id for msg in messages_to_forward]:
            messages_to_forward.append(message)
            print(f"Fetched new message: {message.message}")

async def forward_messages():
    global messages_to_forward
    while True:
        if messages_to_forward:
            for dialog in await client.get_dialogs():
                if dialog.is_group:
                    for message in messages_to_forward:
                        try:
                            await client.send_message(dialog.entity, message.message)
                            print(f'Sent message to {dialog.title}: {message.message}')
                        except Exception as e:
                            print(f'Failed to send message to {dialog.title}: {e}')
            messages_to_forward.clear()  # Clear messages after forwarding
        await asyncio.sleep(FORWARD_INTERVAL)

async def main():
    await client.start()
    print("Bot started!")

    while True:
        await fetch_latest_messages()  # Fetch latest messages from the channel
        await forward_messages()  # Forward messages to all groups

if __name__ == '__main__':
    asyncio.run(main()
