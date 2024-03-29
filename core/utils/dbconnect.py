import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data_telegram(self, userid, username):
        query = f"INSERT INTO users (user_id, username) VALUES ({userid}, '{username}')" \
                f" ON CONFLICT (user_id) DO UPDATE SET username='{username}'"
        await self.connector.execute(query)
    #
    # async def add_vote(self, user_id="NULL", voted="FALSE", voted_for="NULL", username="NULL", name="NULL"):
    #
    #     query = f"INSERT INTO voting (user_id, username, name, voted, voted_for) " \
    #             f"VALUES ({user_id}, \'{username}\', \'{name}\', {voted}, \'{voted_for}\')"
    #     await self.connector.execute(query)
    #
    # async def get_vote(self, user_id):
    #     query = f"SELECT * FROM voting WHERE user_id='{user_id}'"
    #     return await self.connector.fetchrow(query)

    async def add_valentine(self, user_id, username, name, to_user, is_anon):
        query = f"INSERT INTO valentines (from_user_id, from_username, from_name, to_user, is_anon) VALUES " \
                f"({user_id}, '{username}', '{name}', '{to_user}', '{is_anon}')"
        await self.connector.execute(query)

    async def get_valentine(self, from_username, to_user):
        query = f"SELECT from_user_id FROM valentines WHERE from_username='{from_username}' AND to_user='{to_user}' AND is_anon = True"
        return await self.connector.fetch(query)



