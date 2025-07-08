🚀 Overview:

“Meteor Dodge” is a classic survival arcade game made using Pygame, where players control an aircraft and maneuver it around the screen to avoid colliding with falling stars. The objective is to survive as long as possible, gain score by dodging stars, and collect power-ups to extend your survival.

🕹️ Gameplay Mechanics:

Player Control: Use arrow keys to move the aircraft in all directions. The movement is confined within the game window.

Falling Objects: Stars continuously fall from the top of the screen. Each dodged star increases your score.

Collision: If the player hits a star:

With shield → star is destroyed.

Without shield → player loses a life.

Lives System: You start with 3 lives. Lose all = Game Over.

Power-Ups:

💙 Shield (Blue Ellipse): Temporarily protects you from star collisions.

💚 Speed (Green Ellipse): Temporarily doubles your movement speed.

Pause Feature: Press P to pause/resume the game.

Restart Option: After losing, press R to restart or ESC to quit.

📊 Score & High Score:
The score increases with every dodged star.

A persistent high score system is implemented using a text file (highscore.txt) to store the highest score across game sessions.

🎨 Graphics & UI:
Background image (bg.jpeg) and aircraft sprite (aircraft.png) enhance the visual feel.

Stars use star.png image, scaled for proper appearance.

Fonts are used to display:

Time survived

Current score

High score

Number of lives

Power-up indicators

🧠 Power-Up Logic & Timing:

Power-ups appear randomly with a chance each time new stars spawn.

Shield lasts for 4 seconds, speed boost lasts for 3 seconds.

When active, special visual indicators are shown (a glowing circle for shield, a "SPEED!" label for boost).

🧪 Extra Features & Optimizations:

Game runs at a high FPS (120 ticks), making gameplay ultra-smooth.

Clean code structure with modular functions for drawing, input handling, and main loop.

The main menu gives instructions and waits for player input (SPACE to start, ESC to quit).# Meteor_Doge_game
