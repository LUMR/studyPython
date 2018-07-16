import asyncio

import aiomysql
import lumr_web.config
from request import db_dev

db = db_dev.configs['db']
# db = lumr_web.config.toDict(db)

loop = asyncio.get_event_loop()


async def getConn(**db):
    async with aiomysql.create_pool(**db) as pool:
        async with pool.get() as conn:
            async with conn.cursor() as curor:
                await curor.execute("SELECT * FROM t_emp_employee")
                value = await curor.fetchmany(size=20)
                for k in value:
                    print(k)


async def execute(sql, **db):
    async with aiomysql.connect(**db) as conn:
        async with conn.cursor() as curor:
            await curor.execute(sql)
            value = await curor.fetchmany(size=20)
            for k in value:
                print(k)


if __name__ == '__main__':
    loop.run_until_complete(execute("select * from t_emp_employee;", **db))

