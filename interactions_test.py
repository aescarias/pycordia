from pycordia.interactions.components import *

btn = Button(custom_id="Hello World", style=ButtonStyles.primary, label="hello")

row = ActionRow(btn)


@btn.on_click
async def a():
    print("hello world!")