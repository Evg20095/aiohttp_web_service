from aiohttp import web
import aiohttp_jinja2
import requests
import asyncio
import sqlalchemy as sa
from aiohttp_security import check_permission, is_anonymous, remember, forget, setup, check_authorized

import db
from db import log_pass_table, log_links_table


@aiohttp_jinja2.template('registration.html')
async def registration(request):
    data = await request.post()
    if request.method == "POST":
        async with request.app['db'].acquire() as conn:
            query = (sa.select([log_pass_table.c.Logins]).where(log_pass_table.c.Logins==data['login']))
            cursor = await conn.execute(query)
            records = await cursor.fetchall()
            if not records:
                await conn.execute( log_pass_table.insert(), {"Logins":data['login'], "Passwords":data['password']} )

                return {"login": "not_exist"}
            else:
                return {"login": "exist"}
                
                
@aiohttp_jinja2.template('authorization.html')
async def authorization(request):
    data = await request.post()
    if request.method == "POST":
        async with request.app['db'].acquire() as conn:
            query = (sa.select([log_pass_table.c.Passwords], use_labels=True)
                     .where(log_pass_table.c.Logins==data['login']))
            cursor = await conn.execute(query)
            records = await cursor.fetchall()
            if records and records[0][0] == data['password']:
                # логин и пароль совпали
                redirect_response = web.HTTPFound('/user_page')
                await remember(request, redirect_response, data['login'])
                raise redirect_response
            else:
                # логин и пароль не совпали
                return {"logpass": "False"}           
            
           
@aiohttp_jinja2.template('user_page.html')
async def userpage(request):
    is_logged = not await is_anonymous(request)
    if is_logged == True:
        id = await check_authorized(request)
        async with request.app['db'].acquire() as conn:
            query = (sa.select([log_links_table.c.Links]).where(log_links_table.c.Logins==id))
            cursor = await conn.execute(query)
            records = await cursor.fetchall()
            record = [dict(q) for q in records]
        return {"login": id, "record": record }
    else:
        raise web.HTTPFound('/authorization')


@aiohttp_jinja2.template('add_link.html')
async def addlink(request):
    is_logged = not await is_anonymous(request)
    if is_logged == True:
        id = await check_authorized(request)
        data = await request.post()
        if request.method == "POST":
            async with request.app['db'].acquire() as conn:
                await conn.execute( log_links_table.insert(), {"Logins":str(id), "Links":data['link']} )
            raise web.HTTPFound('/user_page')     
        return {"login" : id }
    else:
        raise web.HTTPFound('/authorization')


async def deletelink(request):
    id = await check_authorized(request)
    redirect_response = web.HTTPFound('/user_page')
    data = await request.post()
    if request.method == "POST":
        async with request.app['db'].acquire() as conn:
            query = (sa.delete(log_links_table).where(log_links_table.c.Links == data['deleted_link']).where(log_links_table.c.Logins == id))
            await conn.execute(query)
    raise redirect_response


async def logout(request): 
    id = await check_authorized(request)
    redirect_response = web.HTTPFound('/user_page')
    await forget(request, redirect_response)
    raise redirect_response


@aiohttp_jinja2.template('reset_password.html')
async def resetpassword(request): 
    is_logged = not await is_anonymous(request)
    if is_logged == True:
        id = await check_authorized(request)
        data = await request.post()
        if request.method == "POST":
            async with request.app['db'].acquire() as conn:
                query = (sa.update(log_pass_table).values({'Passwords': data['reset']}).where(log_pass_table.c.Logins == id))
                await conn.execute(query)
            raise web.HTTPFound('/user_page')     
        return {"login" : id }
    else:
        raise web.HTTPFound('/authorization')


async def deleteaccount(request): 
    id = await check_authorized(request)
    redirect_response = web.HTTPFound('/registration')
    async with request.app['db'].acquire() as conn:
            query = (sa.delete(log_pass_table).where(log_pass_table.c.Logins == id))
            await conn.execute(query)
    await forget(request, redirect_response)
    raise redirect_response


async def download(request):
    id = await check_authorized(request)
    data = await request.post()
    part = data['download_link'].split('=')[-1]
    download_link = 'https://drive.google.com/uc?id={}&export=download'.format(part)
    return web.HTTPFound(download_link)