"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import default_cmds
from commands.command import MuxCommand


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """

    pass


class CmdDiagnose(BaseCommand):
    """
    see your stats (Hit Points, Mana, and Move Points).

    Usage:
        diagnose [target]

    This will give an estimate of the targets health. It will also update
    the targets prompt.
    """
    key = "diagnose"

    def func(self):
        if not self.args:
            target = self.caller
        else:
            target = self.search(self.args)
            if not target:
                return
        # try to get hp, mana and move
        hp = target.db.hit_points
        mn = target.db.mana_points
        mv = target.db.move_points

        if None in (hp, mn, mv):
            # Attributes not defined
            self.caller.msg("That is not a valid target!")
            return
        text = "You diagnose %s as having " \
               "%i HIT POINTS, %i MANA and %i MOVE POINTS." \
               % (hp, mn, mv)
        prompt = "HP: %i, MN: %i, MV: %i" % (hp, mn, mv)
        self.caller.msg(text, prompt=prompt)


class CmdAbilities(BaseCommand):
    """
    List abilities

    Usage:
        abilities

    Displays a list of youor current ability values.
    """
    key = "abilities"
    aliases = ["abi"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        """implements the actual functionality"""

        str, agi, mag = self.caller.get_abilities()
        string = "STR: %s, AGI: %s, MAG: %s" % (str, agi, mag)
        self.caller.msg(string)


# In game command for setting gender

class SetGender(Command):
    """
    Sets gender on yourself

    Usage:
      @gender male||female||neutral||ambiguous

    """

    key = "@gender"
    aliases = "@sex"
    locks = "call:developer()"

    def func(self):
        """
        Implements the command.
        """
        caller = self.caller
        arg = self.args.strip().lower()
        if arg not in ("male", "female", "neutral", "ambiguous"):
            caller.msg("Usage: @gender male||female||neutral||ambiguous")
            return
        caller.db.gender = arg
        caller.msg("Your gender was set to %s." % arg)

class CmdLook(default_cmds.CmdLook, MuxCommand):
    pass

class CmdScore(Command):
    """
    The Score Command will show the player the attributes of their current character. This will include
    all of the characters stats as well as their age, level, etc.

    Usage:
        Score

    """
    pass