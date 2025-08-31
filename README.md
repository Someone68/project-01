# How to run the project

## USE PYTHON 3.12 OR NEWER!

### IMPORTANT: RUN IN A LOCAL MACHINE FOR THE BEST EXPERIENCE

The best way to run the project is to clone the repository and run it manually:

```bash
git clone https://github.com/Someone68/cool_repo.git
cd cool_repo
python main.py
```

Packages should automatically be installed, in a virtual environment. This is because it is safer to install packages in an venv, rather than globally on the system. Also because installing global Python packages are completely deprecated on Arch Linux and Arch-based distros. Poetry may or may not work. Online IDEs/compilers may or may not work.

## How it works

This game is mostly modular. Pretty much most of the content is actually in the `interactions` folder using .json files. This allows for easy modding and adding content. NPCs are defined in `npcs.py` in a global NPC registry. The player object is defined in `game.py`, as are 90% of the utilities/helper functions that are used.

To access hidden/unused interactions and change player stats, or do anything that you wouldn't normally be able to do, you can turn on DEV_MODE in `main.py`, which allows you "control" the game however you want. Have fun!
