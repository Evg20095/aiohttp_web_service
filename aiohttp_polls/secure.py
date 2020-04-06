import aiohttp_security
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security.abc import AbstractAuthorizationPolicy



class Simple_AuthorizationPolicy(AbstractAuthorizationPolicy):
    async def authorized_userid(self, identity):
        if identity:
            return identity
    async def permits(self, identity, permission, context=None):
        return identity and permission
    
autz_policy =  Simple_AuthorizationPolicy()

identity_policy = SessionIdentityPolicy()

