import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_server(self, server_id: int) -> int:
        """
        This function will add a server into the Database.

        :param server_id: The ID of the that is being joined.
        """
        await self.connection.execute(
            "INSERT INTO server_settings(id, dice, tracker, tracker_id) VALUES (?, 1, 0, NULL)",
            (
                    server_id,
            ),
        )

    async def set_setting(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id


    async def get_settings(self, server_id: int) -> list:
        """
        This function will get all the settings for a server.

        :param server_id: The ID of the server that should be checked.
        :return: A list of all the settings for the server.
        """
        rows = await self.connection.execute(
            "SELECT id, dice, tracker, tracker_id FROM server_settings WHERE id=?",
            (
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = result

            return result_list