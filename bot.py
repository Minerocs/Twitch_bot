import os
import time
import ctypes
from twitchio.ext import commands
from Inputs import *



class Bot_FG(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['ACCESS_TOKEN'], prefix='!', initial_channels=['minerocs'])
        self.start = 0
        self.delay = 0.55
        self.now = self.delay
        self.nombre = 'chat'
        self.same_name = False

    def spam_key(self, key, spam_times, mensaje):
        with open('comando_ejecutado.txt', 'w') as archivo:
            archivo.write(mensaje.author.display_name + ': ' + mensaje.content)
        for x in range(spam_times):
            PressKey(key)
            ReleaseKey(key)
        self.start = time.time()
        self.nombre = mensaje.author.display_name

    def hold_key(self, key, hold_time, mensaje):
        with open('comando_ejecutado.txt', 'w') as archivo:
            archivo.write(mensaje.author.display_name + ': ' + mensaje.content)
        PressKey(key)
        time.sleep(hold_time)
        ReleaseKey(key)
        self.start = time.time()
        self.nombre = mensaje.author.display_name

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await self.get_channel('minerocs').send('/me ¡Arranca el Juego!')

    async def event_message(self, message):
        if message.echo:
            return
        # print(message.content)
        # Messages with echo set to True are messages sent by the bot...
        # For now, we just want to ignore them...
        if (self.now - self.start) <= 1 and self.nombre == message.author.display_name:
            self.same_name = True
        self.now = time.time()
        if self.now - self.start >= self.delay and not self.same_name:
            mensaje = message.content.lower()
            # Analizar el mensaje
            if mensaje == 'izq':
                self.hold_key(A, 0.8, message)
            elif mensaje == 'der':
                self.hold_key(D, 0.8, message)
            elif mensaje == 'salta':
                self.hold_key(SPACE, 0.1, message)
            elif mensaje == 'dive':
                self.hold_key(CTRL, 0.8, message)
            elif mensaje == 'agarra':
                self.hold_key(SHIFT, 0.8, message)
            elif mensaje == 'ade':
                self.hold_key(W, 0.8, message)
            elif mensaje == 'atra':
                self.hold_key(S, 0.25, message)
        self.same_name = False

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def doug(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.
        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(
            f'Hola {ctx.author.name}! Toda la idea del bot de los comandos troll está inspirada en el streamer y '
            f'youtuber DOUGDOUGW, soy fanatico del pibe y me encanta lo que hace, así que programé mi propio bot con '
            f'la ayuda de Gio.\n Pasate a ver el contenido de doug en youtube que te va a encantar!')

    @commands.command()
    async def comandos(self, ctx: commands.Context):
        await ctx.send('''Comandos troll: __________ 
        IZQ: moverme a la izquierda (move right) ________ 
        DER: moverme a la derecha (move left) _________ 
        ADE: Moverme adelante (forward) ______________ 
        ATRA: Moverme atras (backward) ______________ 
        SALTA: Salto (jump) ____________________________ 
        DIVE: Salto hacia adelante (dive) _______________ 
        AGARRA: Agarro al que tengo en frente (grab)\n''')

    @commands.command()
    async def croquetas(self, ctx: commands.Context):
        await ctx.send('¡Hice croquetas para Montes!')


bot = Bot_FG()
bot.run()
