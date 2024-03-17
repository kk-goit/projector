from cli_bot import PDP11Bot
from animation import welcome_animation

if __name__ == "__main__":
    welcome_animation()
    PDP11Bot().cmdloop()
