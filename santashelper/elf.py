from .classes.SantasHelper import *
from .classes.animation import welcome_animation

def main():
    welcome_animation()
    SantasHelper().cmdloop()

if __name__ == "__main__":
    main()

