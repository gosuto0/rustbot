from rustplus import RustSocket
import asyncio
from rustplus import EntityEvent

class rust():
    ip = ""
    port = ""
    steamid = 
    player_token = 
    entity_id = 
    raid = False
    rust_socket = RustSocket(ip, port, steamid, player_token)

    async def toggle_listener(self):
        @self.rust_socket.entity_event(entity_id)
        async def alarm(event : EntityEvent):
            if event.value:
                self.raid = True
                
    async def connect_rust(self):
        await self.rust_socket.connect()
        await self.toggle_listener()
        print("Connection Successfully!")

    async def raid_check(self):
        if self.raid:
            self.raid = False
            return True
        else:
            return False

    async def get_serverinfo(self):
        info = await self.rust_socket.get_info()
        return info
    
    async def get_servertime(self):
        time = await self.rust_socket.get_time()
        return time

    async def get_serverevent(self):
        event = await self.rust_socket.get_current_events()
        return event