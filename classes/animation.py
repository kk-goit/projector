from __future__ import division
from asciimatics.effects import Print, Cycle, Stars
from asciimatics.renderers import ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

import sys

# Set the GIF file path
IMG = "assets/santa.gif"


# Define the demo function
def animation(screen):
    # Create a list to store scenes
    scenes = []

    # Create the effect for displaying the GIF
    santa_effect = [
        Print(
            screen,
            ColourImageFile(
                screen, IMG,
                screen.height-2,
                uni=screen.unicode_aware,
                dither=screen.unicode_aware),
            0,
            speed=1
        )
    ]

    botname_effect = [
        Cycle(
            screen,
            FigletText("ELF", font='big'),
            int(screen.height / 2 - 8)),
        Cycle(
            screen,
            FigletText("BOT", font='big'),
            int(screen.height / 2 + 3)),
        Stars(screen, 200)
    ]

    # Append the scene with effects to the scenes list
    scenes.append(Scene(santa_effect, duration=60))
    scenes.append(Scene(botname_effect, duration=80))

    # Play the scenes
    screen.play(scenes, stop_on_resize=True, repeat=False)


# Main function
def welcome_animation():
    con = True
    while con:
        try:
            # Start the demo within a Screen wrapper
            Screen.wrapper(animation, catch_interrupt=True)
            con = False
        except ResizeScreenError:
            # Handle resize screen error
            sys.exit(0)


if __name__ == "__main__":
    welcome_animation()
