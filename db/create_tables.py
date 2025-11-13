import asyncio
from db import engine, Base
import models
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

# if the only file will not run singlly than run it from modeule point of view ``python -m db.create_tables``