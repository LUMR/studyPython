from multiprocessing import Process

import requests
import asyncio
import aiohttp.client


def get(employeeId):
    print('task get:%s' % employeeId)
    response = requests.get('http://10.16.85.138/yh/ihr/api/employee/employees/fix/info',
                            {
                                'cookies': 'sid=01200f98ee-7b78-44b2-a91e-a49255d80659;Token=01200f98ee-7b78-44b2-a91e-a49255d80659',
                                'ihrAdminAuthorization': '01200f98ee-7b78-44b2-a91e-a49255d80659',
                                'sahara_tmp_processType': 'employeeDimissionProcess',
                                'empEmployeeId': employeeId})
    print('status: %s \ndata: %s' % (response.status_code, response.text))


async def asyncget(employeeId):
    print('task get:%s' % employeeId)
    async with aiohttp.request('get', 'http://10.16.85.138/yh/ihr/api/employee/employees/fix/info', params={
        'cookies': 'sid=01200f98ee-7b78-44b2-a91e-a49255d80659;Token=01200f98ee-7b78-44b2-a91e-a49255d80659',
        'ihrAdminAuthorization': '01200f98ee-7b78-44b2-a91e-a49255d80659',
        'sahara_tmp_processType': 'employeeDimissionProcess', 'empEmployeeId': employeeId}) as resp:
        # data = await resp.read()
        print(await resp.read())


async def he(id):
    print('strat %s' % id)
    r = await asyncio.sleep(5)
    print('end %s' % id)


if __name__ == '__main__':
    ids = ['8a90d50a63f42bb50163f45d6531167d', '8a90d50a63dafdf30163dd6879bc7dff',
           '8a90d50a63da0cdd0163da1f3e730070', '8a90d50a63af93b50163af9ce0ce0038',
           'a423a2b5483942b7b831bc6410281582', '8f27356d22ad4ba6a0e4701afbc48a6f']
    loop = asyncio.get_event_loop()
    tasks = [asyncget(id) for id in ids]
    loop.run_until_complete(asyncio.wait(tasks))
    print('task complate')
