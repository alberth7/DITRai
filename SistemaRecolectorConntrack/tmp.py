from connectionPostgresql import ConnectionPostgresql
import psycopg2

class Room(object):
    number = int
    name = str
    ''' An area of the game's map.'''
    def __init__(self):
        print("Accessing the Room __init__ method.")
        self.number = 120
        self.name = "jennie"

    def __int__(self,number):
        self.number = number

    def __int__(self,number, name):
        self.number = number
        self.name = name

class FirstRoom(ConnectionPostgresql):
    ''' Just some room.'''
    def __init__(self):
        #super.__init__()
        #super(FirstRoom, self).__init__()
        #print("Accessing the FirstRoom __init__ method.", self.number, self.name)
        super(FirstRoom, self).__init__()
        print("hola", self._hostDB)

    def __int__(self, number):
        super.__init__(number)




class SecondRoom(Room):
    ''' Just some other room.'''
    def __init__(self):
        print("Accessing the SecondRoom __init__ method.")
        super(SecondRoom, self).__init__()
        #super.__init__()


class Game(object):
    ''' Creates a new game.'''
    _current_room = None # Class-level definition of this property.

    def __init__(self):
        print("Created a new Game object.")
        self._current_room = FirstRoom()
        self._current_room = SecondRoom()

    @property
    def current_room(self):
        ''' Returns the current position of the actor.'''
        print("Getting the _current_room attribute for the Game object.")
        return self._current_room

    @current_room.setter   
    def set_room(self, new_room):
        ''' Sets the current_room property of the Game object.'''
        print("Setting the _current_room attribute for the Game object.")
        self._current_room = new_room

g = Game()
