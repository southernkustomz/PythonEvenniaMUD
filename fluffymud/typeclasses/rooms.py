"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from collections import defaultdict
from evennia.utils.utils import list_to_string

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)

            elif con.has_account:
                users.append("|m%s|n" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            string += "%s\n" % desc

        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][
                        0
                    ]
                thing_strings.append(key)
            for thing in thing_strings:
                string += "\n|g{}".format(str(thing))
            for user in users:
                string += "\n|m{} is here.".format(str(user))

        if exits:
            # I want the exits to display as follows
            # Exits:
            # North: north exit
            # South: south exit
            string += "\n\n|[B|!WExits:\n"
            for ex in exits:
                string += "|[B|!W{}: \n|n".format(ex)

        return string

    @property
    def x(self):
        """Returns x coordinate or None."""
        x = self.tags.get(category="coordx")
        return int(x) if isinstance(x, str) else None

    @x.setter
    def x(self, x):
        """Change the X coordinate."""
        old = self.tags.get(category="coordx")
        if old is not None:
            self.tags.remove(old, category="coordx")
        if x is not None:
            self.tags.add(str(x), category="coordx")

    @property
    def y(self):
        """Returns Y coordinate or None."""
        y = self.tags.get(category="coordy")
        return int(y) if isinstance(y, str) else None

    @y.setter
    def y(self, y):
        """Change the Y coordinate."""
        old = self.tags.get(category="coordy")
        if old is not None:
            self.tags.remove(old, category="coordy")
        if y is not None:
            self.tags.add(str(y), category="coordy")

    @property
    def z(self):
        """Returns Z coordinate or None."""
        z = self.tags.get(category="coordz")
        return int(z) if isinstance(z, str) else None

    @z.setter
    def z(self, z):
        """Change the Z coordinate."""
        old = self.tags.get(category="coordz")
        if old is not None:
            self.tags.remove(old, category="coordz")
        if z is not None:
            self.tags.add(str(z), category="coordz")

    @classmethod
    def get_room_at(cls, x, y, z):
        """
        Return the room at the given location or None if not found

        Args:
            x(int): the X coord.
            y(int): the Y coord.
            z(int): the Z coord.

        Return:
            The room at this location(Room) or None if not found
        """
        rooms = cls.objects.filter(
                db_tags__db_key=str(x), db_tags__db_category="coordx").filter(
                db_tags__db_key=str(y), db_tags__db_category="coordy").filter(
                db_tags__db_key=str(z), db_tags__db_category="coordz")
        if rooms:
            return rooms[0]
        # This is a class method so we will call it from Room
        # Room.get_room_at(5, 2, -3)
        # You can still call it from an instance from within the game as follows
        # @py here.get_room_at(3, 8, 0)
        return None
