# Enter The Gungeon MultiWorld Setup Guide

## Required Software

- Enter The Gungeon, from [Steam](https://store.steampowered.com/app/311690/Enter_the_Gungeon/) or the
  [Epic Games Store](https://store.epicgames.com/en-US/p/enter-the-gungeon)
- [r2modman](https://thunderstore.io/package/ebkr/r2modman/) or another Thunderstore mod manager
- The ArchipelaGun mod and its dependencies:
  - **ArchipelaGun** ([Thunderstore](https://thunderstore.io/c/enter-the-gungeon/p/MaoBoulve/ArchipelaGun_Multiworld_Randomizer/))
  - **Mod the Gungeon API** ([Thunderstore](https://thunderstore.io/c/enter-the-gungeon/p/MtG_API/Mod_the_Gungeon_API/))
  - **Alexandria** ([Thunderstore](https://thunderstore.io/c/enter-the-gungeon/p/Alexandria/Alexandria/))

The mod and this APWorld must be the same version. The mod tells you on its Connect tab if they don't match.

## Installation

1. Install Enter The Gungeon.
2. In r2modman, create a profile for Enter The Gungeon and install ArchipelaGun. Its dependencies install with it.
3. Put `enter_the_gungeon.apworld` in your Archipelago `custom_worlds` folder.
4. Start the game from r2modman with **Start modded**.

## Creating a config file

Use the [player options page](../player-options) to make your config file, or open the Archipelago Launcher and choose
**Generate Template Options** to get a template to edit.

## Joining a MultiWorld game

1. Start the game and press **F8** (you can change the key in the mod's BepInEx config file).
2. On the **Connect** tab, enter the server address and port (or paste `address:port` into the first box), your
   slot name and the password if the room has one, then press **Connect**. The mod remembers your last connection.
3. Start a run. Items you have received are handed out when the first floor loads.

You can connect from the title screen, the Breach or during a run.

## The ArchipelaGun menu

- **Connect**: connection details, DeathLink and enemy shuffle switches, and a button to retrieve items.
- **Tracker**: your unlocks and upgrades, checks done for each kind, your next milestones and what your goal still needs.
- **Items**: everything you have received. Hover an item to see what it does or what it rolled this run.
- **Hints**: hints about your items. Ask for a new hint by item name.
- **Console**: mod commands (type `help`) and the server chat.

On the death screen, press **F8** to see what you found and received during that run.

## Troubleshooting

- **Couldn't reach a server**: check the address and port. Rooms on archipelago.gg change port when they restart.
- **No player named ...**: slot names are case-sensitive and must match your config file.
- **The mod and APWorld versions don't match**: install the matching mod build, or regenerate with the matching APWorld.
- The mod writes a debug log to `BepInEx/config/ArchiGungeonDebug_*.txt` in your r2modman profile. Include it when
  reporting a problem.
