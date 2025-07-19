# Pixel-game

## About the game
This game influenced by the typical mario-2D side scrolling platfrom game, the player navigates, defeat enemies and collect health packs to survive. 
The player can move with arrows on the keyboard and fight approaching enemeies with a sword which is activated by pressing 'w'. 
The enemy approaches the player when it is within a certain distance of the player and follows a pathfinding algoithm to find the shortest path
If they reduce the enemy health by a certain amount the enemy retreats allowing the player some time to escape.
In the game the player is kept in the center of the screen so the camera follows them through out the world. If they fall off the platform or a killed by an enemy they respawn at the beginning until thier health has fully depleted. 

---

## The code behind it
In the making of the game I have used pygame and created classes for the individual sprites of the game, e.g. the player, enemies, health packs and platforms. Classes and functions have also been used to create a start menu, help menu and game over menu adding to the game features
