# NPC REGISTRY
# ADD NPCS BY ADDING ENTRIES TO THE LIST OF NPCS BELOW
# ARGS: NAME, DEF_NAME, COLOR

INTERNAL_NPC_NAMES = [
  "narrator"
]

def get_npcs():
  from game import Npc

  return [
      Npc("narrator", "", None),
      Npc("FJock", "Tuff-Looking Kid", "yellow"),
      Npc("Ms. Finessa", "Teacher", "magenta"),
      Npc("Ferd", "Nerdy-Looking Kid", "green"),
      Npc("Elina", "Popular Girl", "blue"),
      Npc("Classmate", "", "white"),
      Npc("Fern","Ferd's Crush","cyan"),
      Npc("Nass","Judge","red")
  ]

def register_npcs(registry):
    for npc in get_npcs():
        registry.add(npc)
