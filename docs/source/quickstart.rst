Quickstart
==========    

.. note:: 
   Note that Pycordia works best on Python 3.8+, 
   although 3.7 is supported.

Pycordia can be installed in two possible ways.

Migrating from Discord.py (or its forks)
----------------------------------------

Pycordia is **not** a drop-in replacement for Discord.py, Pycordia has been built from scratch and shares a different codebase than the one from Discord.py. 
Please note this before using our library. It's up to **you** to decide whether learning a different codebase is worth it for your current bot. Pycordia is still excellent if developing new bots.

Virtual Environments
----------------------------------

We recommend using Pycordia inside a virtual environment to not conflict with other
installed packages.

The following shows steps on how to create and activate one by using `venv`:

.. tab-set::
   
   .. tab-item:: Linux or MacOS

      .. code-block:: sh
         
         $ python3 -m venv venv
         $ source venv/bin/activate
      
   .. tab-item:: Windows
      
      .. code-block:: sh
         
         $ py -3 -m venv venv
         $ venv/Scripts/activate



Installing from PyPi (recommended)
----------------------------------

The easiest way to install Pycordia is from PyPi through `pip`.

.. tab-set::
   
   .. tab-item:: Linux or MacOS

      .. code-block:: sh
         
         $ python3 -m pip install pycordia
      
   .. tab-item:: Windows
      
      .. code-block:: sh
         
         $ py -3 -m pip install pycordia


Installing from Git
-------------------

If you prefer to stay on the edge and install Pycordia directly from Git,
proceed with the following:

.. tab-set::
   
   .. tab-item:: Linux or MacOS

      .. code-block:: sh
         
         $ python3 -m pip install git+https://github.com/angelcarias/pycordia.git
      
   .. tab-item:: Windows

      .. code-block:: sh
         
      $ py -3 -m pip install git+https://github.com/angelcarias/pycordia.git


Verify Pycordia is properly installed by doing:

.. code-block:: python
   
   import pycordia


Examples
--------

All the examples below assume:

- you have setup a Discord application and have obtained a bot token
- you are loading the token through a .env file loader like `python-dotenv`


Basic event showcase
----------------------

A simple example showcasing events in Pycordia

.. code-block:: python

   import pycordia
   from pycordia import models, events
   import dotenv
   import os

   dotenv.load_dotenv()

   client = pycordia.Client(intents=pycordia.Intents.all())
   
   @client.event
   async def on_ready(event: events.ReadyEvent):
      print(f"{client.user} active")

   @client.event
   async def on_message(message: models.Message):
      print(f"A message with content '{message.content}' was sent by {message.author}.")

   client.run(os.getenv("DISCORD_TOKEN"))

HTTP-only client
----------------

Pycordia can also be used solely as an HTTP client for Discord's API.

.. code-block:: python

   import pycordia
   from pycordia import models, events

   import asyncio
   import dotenv
   import os

   dotenv.load_dotenv()

   client = pycordia.Client(intents=pycordia.Intents.all())

   async def main():
      await client.setup_http(os.getenv("DISCORD_TOKEN"))

      await pycordia.models.Message.send("<channel_id>", content="Hello!")

   asyncio.run(main())
