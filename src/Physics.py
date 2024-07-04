import phylib;
import sqlite3;
import os;
import math;
import random;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;

DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;

MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;

FRAME_INTERVAL = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="svg" width="1375" height="700" viewBox="-100 -100 2900 1550"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect height="1350" width="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """<rect height="75" width="3100" x="-100" y="-100" fill="#ececec" />
<rect height="5800" width="100" x="-125" y="-100" fill="#ececec" />
<rect height="75" width="3100" x="-100" y="1375" fill="#ececec" />
<rect height="5800" width="100" x="2725" y="-100" fill="#ececec" />
</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;

################################################################################
class StillBall( phylib.phylib_object ):

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );

        self.__class__ = StillBall;

    def svg( self ):
        ball_class = ''
        if (self.obj.still_ball.number > 0 and self.obj.still_ball.number < 8):
            ball_class = 'low'
        elif (self.obj.still_ball.number > 8 and self.obj.still_ball.number < 16):
            ball_class = 'high'

        svgText = ('  <circle id="b%d" class="%s" cx="%d" cy="%d" r="%d" fill="%s" />\n' %
                   (self.obj.still_ball.number
                  , ball_class 
                  , self.obj.still_ball.pos.y
                  , self.obj.still_ball.pos.x 
                  , BALL_RADIUS
                  , BALL_COLOURS[self.obj.still_ball.number]));
        return svgText;

################################################################################
class RollingBall( phylib.phylib_object ):

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y),
        velocity (x,y), and acceleration (x,y) as arguments.
        """
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        self.__class__ = RollingBall;

    def svg( self ):
        ball_class = ''
        if (self.obj.still_ball.number > 0 and self.obj.still_ball.number < 8):
            ball_class = 'low'
        elif (self.obj.still_ball.number > 8 and self.obj.still_ball.number < 16):
            ball_class = 'high'

        svgText = ('  <circle id="b%d" class="%s" cx="%d" cy="%d" r="%d" fill="%s" />\n' %
                   (self.obj.rolling_ball.number
                  , ball_class
                  , self.obj.rolling_ball.pos.y
                  , self.obj.rolling_ball.pos.x
                  , BALL_RADIUS
                  , BALL_COLOURS[self.obj.rolling_ball.number]));
        return svgText;

    def calcAcc(self):
        speed = math.sqrt((self.obj.rolling_ball.vel.x*self.obj.rolling_ball.vel.x) + (self.obj.rolling_ball.vel.y*self.obj.rolling_ball.vel.y))
        self.obj.rolling_ball.acc.x = (((self.obj.rolling_ball.vel.x * (-1.0)) / speed) * DRAG)
        self.obj.rolling_ball.acc.y = (((self.obj.rolling_ball.vel.y * (-1.0)) / speed) * DRAG)

################################################################################
class Hole( phylib.phylib_object ):

    def __init__( self, pos ):
        """
        Constructor function. Requires a position (x, y) as an arguments.
        """
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );

        self.__class__ = Hole;

    def svg( self ):
        svgText = ('  <circle cx="%d" cy="%d" r="%d" fill="black" />\n' %
                   
                   (self.obj.hole.pos.y
                  , self.obj.hole.pos.x
                  , HOLE_RADIUS));
        return svgText;

################################################################################
class HCushion( phylib.phylib_object ):

    def __init__( self, y ):
        """
        Constructor function. Requires a y value as an argument.
        """
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
                                       
        self.__class__ = HCushion;

    def svg( self ):
        y = 0;
        if (self.obj.hcushion.y == 0):
            y = -25;
        else:
            y = self.obj.hcushion.y;

        svgText = ('  <rect height="1400" width="25" x="%d" y="-25" fill="darkgreen" />\n' % y);
        return svgText;

################################################################################
class VCushion( phylib.phylib_object ):

    def __init__( self, x ):
        """
        Constructor function. Requires a x value as an argument.
        """
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );

        self.__class__ = VCushion;

    def svg( self ):
        x = 0;
        if (self.obj.vcushion.x == 0):
            x = -25;
        else:
            x = self.obj.vcushion.x;
        
        svgText = ('  <rect height="25" width="2750" x="-25" y="%d" fill="darkgreen" />\n' % x);
        return svgText;

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg( self ):
        """
        Returns an svg image to represent the table
        """
        tableSVG = HEADER;
        for object in self:
            if (object != None):
                tableSVG += object.svg();

        tableSVG += FOOTER;
        return tableSVG;

    def roll( self, t ):
        #print(self)
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
            # return table
        return new
    
    def nudge(self):
        return random.uniform( -1.5, 1.5 )
    
    def init_table(self):

        pos = Coordinate( TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                                TABLE_LENGTH - TABLE_WIDTH/2.0 )
        sb  = StillBall( 0, pos )
        self += sb
        # 1 ball
        pos = Coordinate( 
                        TABLE_WIDTH / 2.0,
                        TABLE_WIDTH / 2.0,
                        );

        sb = StillBall( 1, pos )
        self += sb
        # 2 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 2, pos )
        self += sb
        # 9 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 9, pos )
        self += sb
        # 10 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 10, pos )
        self += sb
        # 8 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 8, pos )
        self += sb
        # 3 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 3, pos )
        self += sb
        # 4 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)*(1.5) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(1.5)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 4, pos )
        self += sb
        # 11 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)*(1.5) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(1.5)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 11, pos )
        self += sb
        # 5 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)*(2) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(2)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 5, pos )
        self += sb
        # 12 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)*(2) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(2)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 12, pos )
        self += sb
        # 7 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(1.5)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 7, pos )
        self += sb
        # 14 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(1.5)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 14, pos )
        self += sb
        # 13 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(2)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 13, pos )
        self += sb
        # 15 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(2)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 15, pos )
        self += sb
        # 6 ball
        pos = Coordinate(
                        TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0) + self.nudge(),
                        TABLE_WIDTH/2.0 - 
                        math.sqrt(3.0)*(2)*(BALL_DIAMETER+4.0) + self.nudge()
                        )
        sb = StillBall( 6, pos )
        self += sb

    '''
    returns the ball with the given number or None if a ball with that number DNE
    '''
    def getBall(self, ballNo):
        for objct in self:
            if isinstance(objct, StillBall) and objct.obj.still_ball.number == ballNo:
                return objct
            elif isinstance(objct, RollingBall) and objct.obj.rolling_ball.number == ballNo:
                return objct
        return None
    
    def newCueBall(self):
        pos = Coordinate( TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                                TABLE_LENGTH - TABLE_WIDTH/2.0 )
        sb  = StillBall( 0, pos )
        self += sb

class Database:
    '''
    Initializes the phylib.db database connection
    '''
    def __init__(self, reset=False):
        if reset:
            if os.path.isfile('./phylib.db'):
                os.remove('./phylib.db')
        self.conn = sqlite3.connect('./phylib.db')

    '''
    Creates each of the tables required by the database
    '''
    def createDB(self):
        db_cursor = self.conn.cursor()
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Ball(
                                BALLID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                BALLNO INTEGER NOT NULL,
                                XPOS FLOAT NOT NULL,
                                YPOS FLOAT NOT NULL,
                                XVEL FLOAT,
                                YVEL FLOAT);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS TTable(
                                    TABLEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    TIME FLOAT NOT NULL);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS BallTable(
                                        BALLID INTEGER NOT NULL,
                                        TABLEID INTEGER NOT NULL,
                                        FOREIGN KEY (BALLID) REFERENCES Ball,
                                        FOREIGN KEY (TABLEID) REFERENCES TTable);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Game(
                                    GAMEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    GAMENAME VARCHAR(64) NOT NULL);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Player(
                                    PLAYERID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                                    GAMEID INTEGER NOT NULL,
                                    PLAYERNAME VARCHAR(64) NOT NULL,
                                    FOREIGN KEY (GAMEID) REFERENCES Game);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Shot(
                                SHOTID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                PLAYERID NOT NULL,
                                GAMEID NOT NULL,
                                FOREIGN KEY (PLAYERID) REFERENCES Player,
                                FOREIGN KEY (GAMEID) REFERENCES Game);
            ''')
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS TableShot(
                                        TABLEID INTEGER NOT NULL,
                                        SHOTID INTEGER NOT NULL,
                                        FOREIGN KEY (TABLEID) REFERENCES TTable,
                                        FOREIGN KEY (SHOTID) REFERENCES Shot);
            ''')
        db_cursor.close()
        self.conn.commit()

    '''
    Retrieves a table from the database and returns a corresponding table object
    '''
    def readTable(self, tableID):
        db_cursor = self.conn.cursor()

        # search data base for table with tableID (tableID+1)
        tableRow = db_cursor.execute(
            f'''SELECT * FROM TTABLE
                WHERE TABLEID={tableID+1};''').fetchall()
        # checks if table exists
        if tableRow == []:
            db_cursor.close()
            self.conn.commit()
            return None        
        table = Table()
        table.time = tableRow[0][1]
        # gets all the balls that belong to the table
        balls = db_cursor.execute(
            f'''SELECT * FROM (Ball INNER JOIN BallTable ON Ball.BALLID=BallTable.BALLID)
                WHERE BallTable.TABLEID={tableID+1};''').fetchall()
        # adds each ball to the table object
        for ball in balls:
            number = int(ball[1])
            posx = float(ball[2])
            posy = float(ball[3])
            velx = ball[4]
            vely = ball[5]
            if velx == None and vely == None:
                new_ball = StillBall(number, Coordinate(posx, posy))
            else:
                new_ball = RollingBall(number, Coordinate(posx, posy), Coordinate(float(velx), float(vely)), Coordinate(0,0))
                new_ball.calcAcc()
            table += new_ball
        # clean up cursor and commit
        db_cursor.close()
        self.conn.commit()
        return table
    
    '''
    Retrieves a table from the database and returns a corresponding table object
    '''
    def readTable_time(self, shotID, time):
        db_cursor = self.conn.cursor()

        tableRow = db_cursor.execute(
            f'''SELECT * FROM (TableShot INNER JOIN TTable ON TableShot.TABLEID=TTable.TABLEID)
                WHERE TableShot.SHOTID={shotID+1} AND TTable.TIME={time};''').fetchall()
        # checks if table exists
        if tableRow == []:
            db_cursor.close()
            self.conn.commit()
            return None        
        table = Table()
        tableID = tableRow[0][0]
        table.time = tableRow[0][3]

        # gets all the balls that belong to the table
        balls = db_cursor.execute(
            f'''SELECT * FROM (Ball INNER JOIN BallTable ON Ball.BALLID=BallTable.BALLID)
                WHERE BallTable.TABLEID={tableID};''').fetchall()
        # adds each ball to the table object
        for ball in balls:
            number = int(ball[1])
            posx = float(ball[2])
            posy = float(ball[3])
            velx = ball[4]
            vely = ball[5]
            if velx == None and vely == None:
                new_ball = StillBall(number, Coordinate(posx, posy))
            else:
                new_ball = RollingBall(number, Coordinate(posx, posy), Coordinate(float(velx), float(vely)), Coordinate(0,0))
                new_ball.calcAcc()
            table += new_ball
        # clean up cursor and commit
        db_cursor.close()
        self.conn.commit()
        return table, (tableID - 1)
    
    '''
    Retrieves a table from the database and returns a corresponding table object
    '''
    def get_shot_time(self, shotID):
        db_cursor = self.conn.cursor()

        tableRow = db_cursor.execute(
            f'''SELECT MAX(TTable.TIME) FROM (TableShot INNER JOIN TTable ON TableShot.TABLEID=TTable.TABLEID)
                WHERE TableShot.SHOTID={shotID+1};''').fetchall()
        # checks if table exists
        if tableRow == []:
            db_cursor.close()
            self.conn.commit()
            return None        

        # clean up cursor and commit
        db_cursor.close()
        self.conn.commit()
        return float(tableRow[0][0])

    '''
    Adds a new table to the database and returns its ID
    '''
    def writeTable(self, table):
        db_cursor = self.conn.cursor()

        db_cursor.execute(
            f'''INSERT INTO TTable(TIME)
                VALUES({round(table.time, 2)});''')
        tableID = db_cursor.lastrowid

        for ball in table:
            if isinstance(ball, RollingBall):
                db_cursor.execute(
                    f'''INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                        VALUES({ball.obj.rolling_ball.number},
                                {ball.obj.rolling_ball.pos.x},
                                {ball.obj.rolling_ball.pos.y},
                                {ball.obj.rolling_ball.vel.x},
                                {ball.obj.rolling_ball.vel.y});
                    '''
                )
                ballID = db_cursor.lastrowid
            elif isinstance(ball, StillBall):
                db_cursor.execute(
                    f'''INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                        VALUES({ball.obj.still_ball.number},
                                {ball.obj.still_ball.pos.x},
                                {ball.obj.still_ball.pos.y},
                                NULL,
                                NULL);
                    '''
                )
                ballID = db_cursor.lastrowid
            else:
                continue
            db_cursor.execute(
                f'''INSERT INTO BallTable(BALLID, TABLEID)
                    VALUES({ballID}, {tableID});''')

        db_cursor.close()
        self.conn.commit()
        return tableID - 1

    '''
    Reads and returns an existing game from the database
    '''
    def readGame(self, gameID):
        db_cursor = self.conn.cursor()
        # retrieves a game from the tables
        game = db_cursor.execute(
            f'''SELECT * FROM (Game INNER JOIN Player ON Game.GAMEID=Player.GAMEID)
                WHERE Game.GAMEID={gameID+1}
                ORDER BY Player.PLAYERID;''').fetchall()
        # (GAMEID, GAMENAME, PLAYERID, GAMEID, PLAYERNAME)
        if len(game) < 2:
            db_cursor.close()
            self.conn.commit()
            return None, None, None
        gameName = game[0][1]
        player1Name = game[0][4]
        player2Name = game[1][4]
        db_cursor.close()
        self.conn.commit()
        return gameName, player1Name, player2Name

    '''
    Adds a new game to the database
    '''
    def writeGame(self, game):
        db_cursor = self.conn.cursor()
        db_cursor.execute(
            f'''INSERT INTO Game(GAMENAME)
                VALUES("{game.gameName}");''')
        gameID = db_cursor.lastrowid

        db_cursor.execute(
            f'''INSERT INTO Player(GAMEID, PLAYERNAME)
                VALUES({gameID}, "{game.player1Name}");''')
        db_cursor.execute(
            f'''INSERT INTO Player(GAMEID, PLAYERNAME)
                VALUES({gameID}, "{game.player2Name}");''')     

        db_cursor.close()
        self.conn.commit()
        return gameID - 1 

    def writeShot(self, playerName, gameName):
        db_cursor = self.conn.cursor()

        game = db_cursor.execute(
            f'''SELECT GAMEID FROM Game
                WHERE Game.GAMENAME="{gameName}";''').fetchall()
        if game == []:
            db_cursor.close()
            return None
        gameID = game[0][0]

        player = db_cursor.execute(
            f'''SELECT PLAYERID FROM Player
                WHERE Player.GAMEID={gameID} AND Player.PLAYERNAME="{playerName}";''').fetchall()
        if player == []:
            db_cursor.close()
            return None
        playerID = player[0][0]

        db_cursor.execute(
            f'''INSERT INTO Shot(PLAYERID, GAMEID)
                VALUES({playerID}, {gameID});''')
        shotID = db_cursor.lastrowid
        db_cursor.close()
        self.conn.commit()
        return shotID - 1

    def writeTableShot(self, tableID, shotID):
        db_cursor = self.conn.cursor()
        db_cursor.execute(
        f'''INSERT INTO TableShot(TABLEID, SHOTID)
            VALUES({tableID+1}, {shotID+1});''')
        db_cursor.close()
        self.conn.commit()

    '''
    Commits all uncommited changes to the database and closes the connection
    '''
    def close(self):
        self.conn.commit()
        self.conn.close()

class Game:
    '''
    Initializes a new game object and adds it to the database or reopens an existing game
    '''
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        if gameID != None:
            if gameName != None or player1Name != None or player2Name != None:
                raise TypeError("Invalid constructor call")
            self.gameID = gameID
            db = Database()
            db.createDB()
            self.gameName, self.player1Name, self.player2Name = db.readGame(self.gameID)
            db.close()
            return
        
        if gameName == None or player1Name == None or player2Name == None:
            raise TypeError("Invalid constructor call")
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name
        db = Database()
        db.createDB()
        self.gameID = db.writeGame(self)
        db.close()
        
    '''

    '''
    def shoot(self, gameName, playerName, table, xvel, yvel):
        db = Database()
        shotID = db.writeShot(playerName, gameName)
        if shotID == None:
            db.close()
            return shotID

        cueBall = table.getBall(0)
        xpos = cueBall.obj.still_ball.pos.x
        ypos = cueBall.obj.still_ball.pos.y
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos.x = xpos
        cueBall.obj.rolling_ball.pos.y = ypos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel
        speed = math.sqrt((xvel*xvel) + (yvel*yvel))
        cueBall.obj.rolling_ball.acc.x = (((xvel * (-1.0)) / speed) * DRAG)
        cueBall.obj.rolling_ball.acc.y = (((yvel * (-1.0)) / speed) * DRAG)

        while table != None:
            oldTable = table
            startTime = table.time
            table = table.segment()
            if table == None:
                break
            endTime = table.time
            segTime = endTime - startTime
            numFrames = math.floor(segTime / FRAME_INTERVAL)
            for i in range(numFrames):
                t = i * FRAME_INTERVAL
                newTable = oldTable.roll(t)
                newTable.time = startTime + t
                if (i > 0):
                    tableID = db.writeTable(newTable)
                    db.writeTableShot(tableID, shotID)
            tableID = db.writeTable(table)
            db.writeTableShot(tableID, shotID)
               
        db.close()
        return shotID
