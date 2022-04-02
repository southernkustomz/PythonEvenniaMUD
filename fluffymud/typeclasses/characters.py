"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""


from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, note anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.


    """
    def at_object_creation(self):
        """
            Setting Character attributes
        """
        self.db.gender = "ambiguous"
        self.db.age = 5

        self.db.level = 1
        self.db.hit_points = 0
        self.db.mana_points = 0
        self.db.move_points = 0
        self.db.max_hit_points = 100
        self.db.max_mana_points = 100
        self.db.max_move_points = 100

        self.db.attack_power = 1

        self.db.hit_regen_rate = 5
        self.db.mana_regen_rate = 5
        self.db.move_regen_rate = 5

        self.db.race = "human"

        self.db.classes = []
        self.db.stats = {"STR": 0, "INT": 0, "DEX": 0, "CON": 0, "CHA": 0, "WIS": 0}

        self.db.prompt = None
        self.db.prompt_enabled = True

        self.db.attackable = True
        self.db.can_attack = True



