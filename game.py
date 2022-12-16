import pygame
import random
pygame.font.init()

#Setting up width and height of the game -window
WIDTH, HEIGHT = 600, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#Import images for the game and scale them to the correct sizes..
START = pygame.image.load("attatchments/start.png")
BACKGROUND = pygame.image.load("attatchments/road.png")
PLAYERIMG = pygame.transform.scale(pygame.image.load("attatchments/playerImg.png"), (50,100))
WHITECAR = pygame.transform.scale(pygame.image.load("attatchments/whitecar.png"), (100,150))
BLACKCAR = pygame.transform.scale(pygame.image.load("attatchments/blackcar.png"), (100,150))
BLUECAR = pygame.transform.scale(pygame.image.load("attatchments/bluecar.png"), (100,150))
YELLOWCAR = pygame.transform.scale(pygame.image.load("attatchments/yellowcar.png"), (100,150))

pygame.display.set_caption("DRÜNKEN DRIVER")


#Player class
class Player:
    def __init__(self):
        self.x = WIDTH/2 - 25
        self.y = HEIGHT - 150
        self.__img = PLAYERIMG
        self.width = 50
        self.height = 100

    #Draw function takes a surface (window) as a parameter and "draws" the player image to it.
    def draw(self, window):
        window.blit(self.__img, (self.x, self.y))
        

#Class for Background elements
class Background:
    def __init__(self, y):
        self.__x = 0
        self.y = y
        self.__img = BACKGROUND

    def draw(self, window, speed):
        window.blit(self.__img, (self.__x, self.y))
        self.y += speed


#Class for Car (obstacle) -elements
class Car:
    #Class has a list of car images so it can randomly assign car -objects images when being called...
    cars = [WHITECAR, BLACKCAR, BLUECAR, YELLOWCAR]

    def __init__(self, x, y):
        self.lane = x
        self.y = y 
        self.collided = False
        self.speed = 5
        self.__img = random.choice(self.cars) #This randomly assigns an image to the class from the cars -list
        self.width = 100
        self.height = 150

    #This function takes care of drawing the cars on to the screen and moving them downwards.
    def draw(self, window):
        window.blit(self.__img, (self.lane, self.y))
        self.y += self.speed

    #Collision detection fuction that checks whether the current car -obejct collides with the player object passed to it as a parameter..
    def collision(self, player, list):

        #First the function checks whether the player -object is colliding with current Car -object on Y-axis
        if (player.y <= self.y + self.height and player.y + player.height >= self.y):
            #If player is colliding with Car on Y-axis, the function also checks collisions on the X-axis.
            if ((player.x >= self.lane and player.x <= self.lane + self.width) or 
            (player.x + player.width >= self.lane and player.x + player.width <= self.lane + self.width)):
                #If there's a collision on both Y- and X-axis, the current Car -object gets a value -collided = True, so we can see which cars have collided with the player..
                self.collided = True
                list.append(self)


#This list includes three possible X -postions that Car -objects can use..
lanes = [118, WIDTH/2 - 50, WIDTH -100 -118]

#Main function to that runs the game etc.
def gameLoop():
    game = True
    Lost = False

    playerSpeed = 6
    gameSpeed = 5
    global lostCounter
    lostCounter = 0

    leftBorder = 100
    rightBorder = 500 - 50

    mainFont = pygame.font.SysFont("comicsans", 20)
    lossFont = pygame.font.SysFont("comicsans", 42)
    global Level
    Level = 0
    carsDodged = 0
    global newLevel
    newLevel = 0

    FPS = 60
    clock = pygame.time.Clock()   

    player = Player()
    cars = []
    backgrounds = [Background(0), Background(-HEIGHT)]
    lostList = []

    #This function creates X amount of new Car -objects to the car list when called upon...
    def addCars(spaceBetween):
        #Bottom and Top -variables are the limits for where on Y-axis can new cars be placed...
        bottom = 150
        top = 250

        #This loop makes sure to create always increasing amount of cars to the cars -list based on the level 
        for i in range(0, newLevel):
            #Here the function adds a new Car -object to the cars -list
            cars.append(Car(
                random.choice(lanes), #this randomly assigns "lanes" (X-positions) for the new Car -object.
                - random.randint(bottom, top) #this creates a random Y-position for a new car, that is whithin the limits set on the top of this function
            ))
            #Here the function adds a big enough gap for the next Cars' Y-position that the Car -objects wont collide with each other.
            bottom += 250 + spaceBetween
            top += 250 + spaceBetween

        
        
    #This function takes care of moving the background so that the player appears to be moving on the screen, as well as removing backgrounds that have already passed the screen.
    #It also always ads a new Bakcground -object to the backgrounds -list whenever the last Background -object is about to appear on the screen.
    def moveBackground():
        for bg in backgrounds:
            bg.draw(WINDOW, gameSpeed)
        
        try:
            if (backgrounds[-1].y > -5 ):
                backgrounds.append(Background(-HEIGHT))
        except IndexError:
            pass

        try:
            if(backgrounds[0].y > HEIGHT + 100):
                backgrounds.remove(backgrounds[0])
        except IndexError:
            pass
    

    #This function takes care of updating the screen as well as rendering/drawing all the elements to the screen.
    def updateScreen():

        #moveBackground -function is executed whenever the screen is updated
        moveBackground()
    
        #This loop iterates through cars -list and draws all the cars to the screen, as well as checks them for collision.
        for car in cars:
            car.draw(WINDOW)
            car.collision(player, lostList)
        
        #Player, level text, and points text are only rendered when player has yet to lose.
        if(Lost != True):
            player.draw(WINDOW)    
            #Here the function renders level and point -texts to the screen
            WINDOW.blit(mainFont.render(f"Level {Level}", 1, (0,0,0)), (20,10))
            WINDOW.blit(mainFont.render(f"Points: {carsDodged}", 1, (0,0,0)), (20,30)) 

        pygame.display.update()


    #This funciton handles letting the player know that they have lost the game
    def lostScreen():
        WINDOW.blit(BACKGROUND, (0,0))
        lostList[0].draw(WINDOW)
        player.draw(WINDOW)
        lossText = lossFont.render(f"You crashed", 1, (255,0,0))
        endLevelPoints = mainFont.render(f"You got to level {Level} with {carsDodged} points", 1, (255,50,0))
        WINDOW.blit(lossText, ((WIDTH/2 - lossText.get_width()/2), (WIDTH/2 - lossText.get_height()/2)))
        WINDOW.blit(endLevelPoints, ((WIDTH/2 - endLevelPoints.get_width()/2),(HEIGHT/2 + lossText.get_height() -endLevelPoints.get_height()/2)))
        pygame.display.update()

    #This is the main game -loop
    while game:

        #clock.tick(FPS) takes care that the this loop only runs FPS -amounts / second (60 times / second)
        clock.tick(FPS)

        #This updates the screen 60time /second
        updateScreen()

        #This loop handles closing the game if the user tries to close it.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #This section handles moving the player by detecting user keyboard events.
        keys = pygame.key.get_pressed()
        if(Lost != True):
            if keys[pygame.K_a]:
                if(player.x > leftBorder):
                    player.x -= playerSpeed
            if keys[pygame.K_d]:
                if(player.x < rightBorder):
                    player.x += playerSpeed
            if keys[pygame.K_w]:
                if(player.y > HEIGHT/2):
                    player.y -= playerSpeed
            if keys[pygame.K_s]:
                if(player.y < HEIGHT - 100):
                    player.y += playerSpeed


        #This keeps our cars -list manageable and handles the collisions.
        for car in cars:
            if (car.collided):
                Lost = True
            if (car.y - 100 >= HEIGHT):
                cars.remove(car)
                carsDodged += 1
                newLevel -= 1

        #This controls the level system..
        #Everytime the current level has been beaten, this conditional creates a new level with increased difficulty
        if (newLevel <= 0):
            Level += 1
            playerSpeed += 0.5
            gameSpeed += 0.5
            newLevel = 15 + Level
            cars = []
            addCars(150)
            for car in cars:
                car.speed = playerSpeed
        
        #This conditional handles lose -situations, by stopping the game -loop and clearing both cars- and backgrounds -list
        if (Lost):
            cars = []
            backgrounds = []
            lostList[0].speed = 0
            #This conditional makes sure that the "You lost" -text is displayed for 5s after the game ends.
            if lostCounter >= (FPS) * 5:
                game = False
            else:
                lostScreen()
                lostCounter += 1

    
            
#This is a frame function that handles the start -screen, as well as starting the game when user presses any key on the keyboard.
def gameOn():
    WindowOpen = True
    startGame = False
    startScreen = True
    
    def makeStartScreen():
        WINDOW.blit(START, (0,0))
        pygame.display.update()
    
    while WindowOpen:

        if (startScreen):
            makeStartScreen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WindowOpen = False
                    exit()
                if event.type == pygame.KEYDOWN:
                    startGame = True
                    startScreen = False    

        if (startGame):
            gameLoop()
            startScreen = True
            startGame = False
    
gameOn()

pygame.quit()
