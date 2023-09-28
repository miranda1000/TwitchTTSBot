from aiohttp import web
import socketio
import ssl

def start(secret_token: str = 'admin', port: int = 7890):
    # creates a new Async Socket IO Server
    sio = socketio.AsyncServer()
    # Creates a new Aiohttp Web Application
    app = web.Application()
    # Binds our Socket.IO server to our Web App instance
    sio.attach(app)
    
    ## If we wanted to create a new websocket endpoint,
    ## use this decorator, passing in the name of the
    ## event we wish to listen out for
    @sio.on('message')
    async def print_message(sid, message):
        #print("Socket ID: " , sid)
        #print(message)

        if not isinstance(message, dict) or not 'token' in message or message['token'] != secret_token:
            return # invalid

        ## await a successful emit of our reversed message
        ## back to the client
        await sio.emit('message', message['msg'])
    
    ## we can define aiohttp endpoints just as we normally
    ## would with no change
    async def index(request):
        if not 'token' in request.rel_url.query or request.rel_url.query['token'] != secret_token:
            raise web.HTTPUnauthorized()
            
        with open('index.html') as f:
            return web.Response(text=f.read().replace('{{ip}}', 'mc.rogermiranda1000.com').replace('{{port}}', str(port)), content_type='text/html')

    # We bind our aiohttp endpoint to our app router
    app.router.add_get('/', index)

    # https TODO
    ssl_context = None
    #ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #ssl_context.load_cert_chain('server.pem', 'key.pem')

    # We kick off our server
    web.run_app(app, port=port, ssl_context=ssl_context)

if __name__ == '__main__':
    start()