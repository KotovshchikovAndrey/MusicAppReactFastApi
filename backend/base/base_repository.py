from databases import Database
from db import database as db
from typing import Union


class BaseRepository:
    _database: Database = db

    def __init__(self, model) -> None:
        self.table = model.__table__
    
    async def get_all(self) -> list:
        query = self.table.select()
        return list(await self.database.fetch_all(query))
    
    async def get_by_id(self, id: int) -> Union[dict, None]:
        query = self.table.select().where(self.table.c.id == id)
        query_dict = await self.database.fetch_one(query)
        return dict(query_dict) if query_dict is not None else None
    
    async def create(self, create_data: dict) -> int:
        create_keys = ", ".join(list(create_data.keys()))
        create_values = ", ".join(map(lambda x: f"'{x}'", list(create_data.values())))
        query = f"""
                    INSERT INTO {self.table} 
                        ({create_keys}) VALUES ({create_values})
                        RETURNING id;
                """
                
        return int(await self.database.execute(query))
    
    async def update(self, id: int, update_data: dict) -> int:
        update_params = ", ".join("{}='{}'".format(key, value) for key, value in update_data.items())
        query = f"""UPDATE {self.table} SET {update_params} RETURNING id;"""

        return int(await self.database.execute(query))

    async def delete(self,id: int) -> None:
        query = self.table.delete().where(self.table.c.id == id)
        await self.database.execute(query)
    
    @property
    def database(self):
        return self._database
        
               