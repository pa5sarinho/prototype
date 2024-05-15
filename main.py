import curses
import random

class Map:

    def __init__(self, height: int, width: int) -> None:
        self.width  = width
        self.height = height
        self.array  = list()

    def generateMap(self) -> None:
        a = []
        for h in range(self.height):
            a = ['.' for i in range(self.width)] 
            self.array.append(a)
        
    def generateTrees(self, n: int = 1) -> None:
        for h in range(self.height):
            for w in range(self.width):
                num = random.randint(0, 10*(1/n))
                if num == 1:
                    self.array[h][w] = 'Y'
    
    def getSubArea(self, xi: int, yi: int, xf: int, yf: int) -> list:
        cutArray = self.array[yi:yf]
        return [row[xi:xf] for row in cutArray]

class Animal:
    def __init__(self, name: str) -> None:
        self._name    = name
        self._species = ''
        self._hunger  = 100
        self._dead    = False
        self._coord   = None

        self.body_status = {
            '''
            attached: 1 has the limb; 0 for amputated/does not apply
            injure: 0 for not injured; 1 to 4 for severity
            injuries: type(s) of injury (list)
            health: overall health indicator of limb (from 1 to 100)
            temperature: 9 too hot; 1 too cold, 5 just right
            bleeding: 0 to 100, affects rest of the body
            '''
            "head": {
                "attached"    : 1,
                "injured"     : 0,
                "injuries"    : [],
                "health"      : 100,
                "temperature" : 5,
                "bleeding"    : 0
            },
            "torso": {
                "attached"    : 1,
                "injured"     : 0,
                "injuries"    : [],
                "health"      : 100,
                "temperature" : 5,
                "bleeding"    : 0
            }
        }
    
    def place(self, x, y):
        self._coord = (x, y)

    def despawn(self):
        self._coord = None


MAP_LIMIT = (23, 49)
mainMap = Map(90, 120)
mainMap.generateMap()
mainMap.generateTrees()

you = (11, 24)
barriers = ['#', 'Y', '&']

mainMap.array[you[0]][you[1]] = '@'

visibleMapCoord = ()


def move(direction: str):
    global you
    modifier = 0

    if direction == 'right' or direction == 'down':
        modifier = 1
    else:
        modifier = -1

    if (direction == 'right' and you[1] < MAP_LIMIT[1]-1) or (direction =='left' and you[1] > 0):
        if mainMap.array[you[0]][you[1]+modifier] not in barriers:
            mainMap.array[you[0]][you[1]] = '.'
            you = (you[0],you[1]+modifier)
            mainMap.array[you[0]][you[1]] = '@'
        
    elif (direction == 'up' and you[0] > 0) or (direction == 'down' and you[0] < MAP_LIMIT[0]-1):
        if mainMap.array[you[0]+modifier][you[1]] not in barriers:
            mainMap.array[you[0]][you[1]] = '.'
            you = (you[0]+modifier,you[1])
            mainMap.array[you[0]][you[1]] = '@'

def addLog(logWindow, log, string):
    logWindow.clear()
    log[0] = log[1]
    log[1] = log[2]
    log.pop()
    log.append(string)


def main():
    screen = curses.initscr()
    screen.nodelay(1)
    curses.start_color()
    curses.noecho()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    mapWin = curses.newwin(MAP_LIMIT[0]+2, MAP_LIMIT[1]+2, 4, 2) # 50x50 starting at 2,2
    #mapWin.bkgd(' ', curses.color_pair(1))
    mapWin.box()
    mapWin.keypad(True)
    curses.mousemask(1)

    logWin = curses.newwin(4, 50, 0, 2)
    logWin.box()

    logStack = ['', '', '']


    while True:
        visibleMap = mainMap.getSubArea(1, 1, MAP_LIMIT[0]-2,MAP_LIMIT[1]-2)
        for i in range(len(visibleMap)):
            for j in range(len(visibleMap)):
                mapWin.addstr(i+1, j+1, visibleMap[i][j])

        mapWin.refresh()
        logWin.refresh()
        # Handling user input
        key       = screen.getch()

        if key == curses.KEY_MOUSE:
            _, mousex, mousey, _, _ = curses.getmouse()
            addLog(logWin, logStack, f"clicked{mousex}{mousey}")
        elif key == ord('q'):
            break
        elif key == ord('s') or key == curses.KEY_DOWN:
            move('down')
        elif key == ord('w') or key == curses.KEY_UP:
            move('up')
        elif key == ord('a') or key == curses.KEY_LEFT:
            move('left')
        elif key == ord('d') or key == curses.KEY_RIGHT:
            addLog(logWin, logStack, "moved right")
            move('right')

        # Game events
        logWin.addstr(1, 1, logStack[0])
        logWin.addstr(2, 1, logStack[1])
        logWin.addstr(3, 1, logStack[2], curses.color_pair(1))

        
    curses.endwin()
    print(visibleMap)

if __name__ == "__main__":
    main()
