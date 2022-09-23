import rust
import discordbot
import asyncio

class main():
    async def setup_connect(self):
        rust_class = rust.rust()
        discord_class = discordbot.discordbot()
        await asyncio.gather(
            discord_class.run_bot(rust_class),
            rust_class.connect_rust()
        )

asyncio.run(main().setup_connect())