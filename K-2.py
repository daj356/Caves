import pygame
import sys
import os
import random
import pyttsx3
from pygame.locals import *

# https://github.com/jrenner/graphical-binary-trees
# The author of the original repository was jrenner from the link above.
# We took and modified his repository so that we could present the idea of Binary Trees

# Initializes the text-to-speech function
engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Speed percent
voices = engine.getProperty('voices')

# Initializes pygame
pygame.init()

# Get the screen resolution
screen = pygame.display.set_mode((1280, 800), FULLSCREEN)

# Sets the current window caption
pygame.display.set_caption("Spelunker 3000")

# Control how held keys are repeated: set_repeat(delay [ms], interval [ms])
pygame.key.set_repeat(200, 20)

# infoObject contains information about the users display settings e.g. resolution
infoObject = pygame.display.Info()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Gets the width and height of the screen
area = screen.get_rect()

# WIDTH and HEIGHT
WIDTH, HEIGHT = area[2], area[3]

# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Game Fonts
TITLE_FONT = "INVASION2000.TTF"
OPTIONS_FONT = "dpcomic.ttf"

droidsans = pygame.font.match_font("verdana")
FONT = pygame.font.Font(droidsans, 16)
FONT2 = pygame.font.Font(droidsans, 24)

ROOT_X = WIDTH / 2
# BOX_SIZE is used to determine the size of the box obviously, but it's also used to change the X and Y Step,
# which is how far the box is from the starting point.
BOX_SIZE = (25, 25)
X_STEP = BOX_SIZE[0] + 10

Y_START = 200
# Y_STEP's multiplier determines how deep the line from node to node is
Y_STEP = BOX_SIZE[1] * 2

# The number of nodes in the tree, and the maximum value for the random number that generates the node cargo value
NUM_OF_NODES = 10
KEYBOARD_PAN_STEP = 50


# A bit more confusing, Master is the whole display, tree and all. Nodelist and Count are pretty self-explanatory,
# they hold information about the tree. X_shift and Y_shift control how the WASD controls move the camera. Idk what
# the clock is for tbh. Selection handles which key the user is pressing. All usages of "m" is the initialized Master.
def talk(say):
    engine.say(say)
    engine.runAndWait()


class Master(object):
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
        # nodelist - a 2d array of nodes sorted by depth level,
        # it is initialized as empty, layers added as needed
        self.nodelist = []
        self.nodecount = 1
        self.x_shift = 0
        self.y_shift = 0
        self.clock = pygame.time.Clock()
        self.selection = None
        self.sound = 0
        # True = male, False = Female
        self.voice = True

    # Formats the text
    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText

    # Resets the tree to an empty tree with a single node
    def reset(self):
        self.nodelist = []
        self.nodecount = 1
        self.x_shift = 0
        self.y_shift = 0
        self.clock = pygame.time.Clock()
        self.selection = None

    # Main Menu
    def intro_screen(self):
        index = 0
        # add "info" back to the list below
        menu_selection_list = ["start", "quit"]
        intro_screen = True
        selected = menu_selection_list[index]

        while intro_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            intro_screen = False
                            pygame.display.flip()
                        if selected == "quit":
                            pygame.quit()
                            quit()

            # Main Menu UI
            screen.fill(BLACK)
            title = m.text_format("SPELUNKSTER 3000", TITLE_FONT, 65, RED)
            if selected == "start":
                text_start = self.text_format("START", OPTIONS_FONT, 85, YELLOW)
            else:
                text_start = self.text_format("START", OPTIONS_FONT, 75, WHITE)

            if selected == "quit":
                text_quit = self.text_format("QUIT", OPTIONS_FONT, 85, YELLOW)
            else:
                text_quit = self.text_format("QUIT", OPTIONS_FONT, 75, WHITE)

            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            # Main Menu Text
            screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
            screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 250))
            screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 320))
            pygame.display.update()
            self.clock.tick(60)
            pygame.display.set_caption("Main Menu")

    # Select Voice
    def voice_selection(self):
        index = 0
        # add "info" back to the list below
        menu_selection_list = ["male", "female"]
        voice_select = True
        selected = menu_selection_list[index]

        while voice_select:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "male"
                    elif event.key == pygame.K_DOWN:
                        selected = "female"
                    if event.key == pygame.K_RETURN:
                        if selected == "male":
                            voice_select = False
                            m.voice = True
                            # Sets a male voice
                            engine.setProperty('voice', voices[0].id)

                            pygame.display.flip()
                        elif selected == "female":
                            voice_select = False
                            m.voice = False
                            # Sets a female voice
                            engine.setProperty('voice', voices[1].id)

                            pygame.display.flip()

            # Voice Selection UI
            screen.fill(BLACK)
            title = m.text_format("SPELUNKSTER 3000", TITLE_FONT, 65, RED)

            if selected == "male":
                text_male = self.text_format("MALE", OPTIONS_FONT, 85, YELLOW)
            else:
                text_male = self.text_format("MALE", OPTIONS_FONT, 75, WHITE)

            if selected == "female":
                text_female = self.text_format("FEMALE", OPTIONS_FONT, 85, YELLOW)
            else:
                text_female = self.text_format("FEMALE", OPTIONS_FONT, 75, WHITE)

            title_rect = title.get_rect()
            male_rect = text_male.get_rect()
            female_rect = text_female.get_rect()

            # Game title
            screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))

            # Male text
            screen.blit(text_male, (WIDTH / 2 - (male_rect[2] / 2), 250))
            # Male Character
            male = pygame.image.load(r'resources/Miner2.png')
            male = pygame.transform.scale(male, (74, 130))
            screen.blit(male, (WIDTH / 2 + male_rect[2] / 2 + 50, 250))

            # Female text
            screen.blit(text_female, (WIDTH / 2 - (female_rect[2] / 2), 420))
            # Female Character
            female = pygame.image.load(r'resources/Miner_Female2.png')
            female = pygame.transform.scale(female, (74, 130))
            screen.blit(female, (WIDTH / 2 + female_rect[2] / 2 + 25, 420))

            pygame.display.update()
            self.clock.tick(60)
            pygame.display.set_caption("Voice Selection")


# Every node is an object. It has information about its parent, cargo (the number it contains), the node to the left
# and right and the depth.
class Node(object):
    def __init__(self, parent=None, right=None, left=None, depth=None):
        self.type = None
        self.parent = parent
        self.right = right
        self.left = left
        self.depth = depth
        self.rect = None
        self.visit = 0
        m.nodecount += 1
        self.value = m.nodecount - 1

    # Provides on-screen depth information for the user at the bottom of the screen
    def __str__(self):
        return "NODE depth: %d" % self.depth

    # Sets the size and location of each node as they are created
    def set_rect(self, arrayOfCoords):
        tempArray = []
        if self.type == "root":
            mod = 0
            x = ROOT_X
        elif self.type == "left":
            mod = -X_STEP
            children = 0
            if self.right:
                children = 1
                children += self.right.count_children()
                mod = -(children * X_STEP)
        elif self.type == "right":
            mod = X_STEP
            children = 0
            if self.left:
                children = 1
                children += self.left.count_children()
                mod = children * X_STEP
        else:
            print("unhandled case in set_rect()")
            sys.exit(1)
        if self.type in ["left", "right"]:
            x = self.parent.rect.left
        y = Y_START + Y_STEP * self.depth
        tempArray.append(x + mod)
        tempArray.append(y)
        if tempArray in arrayOfCoords:
            if self.type == "right":
                tempArray[0] = tempArray[0] - BOX_SIZE[0]
                mod = mod - BOX_SIZE[0]
            if self.type == "left":
                tempArray[0] = tempArray[0] + BOX_SIZE[0]
                mod = mod + BOX_SIZE[0]
        arrayOfCoords.append(tempArray)
        self.rect = pygame.rect.Rect((x + mod, y), BOX_SIZE)

    # Prints the nodes onto the game window
    def draw(self):
        pic_select = pygame.image.load(r'resources/pic_selected.png')
        pic_select = pygame.transform.scale(pic_select, (BOX_SIZE[0] + 5, BOX_SIZE[1] + 5))
        pic = pygame.image.load(r'resources/pic.png')
        pic = pygame.transform.scale(pic, (BOX_SIZE[0] + 5, BOX_SIZE[1] + 5))
        rect = pygame.rect.Rect(self.rect.left + m.x_shift, self.rect.top + m.y_shift,
                                self.rect.width, self.rect.height)
        if BOX_SIZE[0] >= 10:  # skip text if box is too small
            text = FONT.render(str(self.value), 1, WHITE)
            tr = text.get_rect()
            tr.center = rect.center
            if self.value == m.selection.value:
                m.display.blit(pic_select, tr)
            else:
                m.display.blit(pic, tr)
            m.display.blit(text, tr)
        # pygame.draw.rect(m.display, BLUE, rect, 1)
        if self.parent:
            start = (rect.centerx, rect.top)
            end = (self.parent.rect.centerx + m.x_shift, self.parent.rect.bottom + m.y_shift)
            pygame.draw.aaline(m.display, BROWN, start, end)  # This is the line that actually draws the box.

    # Counts the number of children of the current tree being displayed, returns an integer "count"
    def count_children(self):
        count = 0
        if self.left:
            count += 1
            count += self.left.count_children()
        if self.right:
            count += 1
            count += self.right.count_children()
        return count


# Quits the game
def quit():
    print("QUIT")
    pygame.quit()
    sys.exit()


def pause():
    pause = True
    while pause is True:
        pauseBuild()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w:
                    m.y_shift += KEYBOARD_PAN_STEP
                elif event.key == K_s:
                    m.y_shift -= KEYBOARD_PAN_STEP
                elif event.key == K_a:
                    m.x_shift += KEYBOARD_PAN_STEP
                elif event.key == K_d:
                    m.x_shift -= KEYBOARD_PAN_STEP
                elif event.key == K_RETURN:
                    pause = False
                else:
                    print("Invalid key.")


def interface():
    global LAST
    inter = True
    while inter is True and m.nodecount <= NUM_OF_NODES:
        build(True)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key in [K_q, K_ESCAPE]:
                    quit()
                elif event.key == K_r:
                    m.nodecount = 1
                    build_tree()
                elif event.key == K_w:
                    m.y_shift += KEYBOARD_PAN_STEP
                elif event.key == K_s:
                    m.y_shift -= KEYBOARD_PAN_STEP
                elif event.key == K_a:
                    m.x_shift += KEYBOARD_PAN_STEP
                elif event.key == K_d:
                    m.x_shift -= KEYBOARD_PAN_STEP
                elif event.key == K_UP:
                    if m.selection.parent:
                        m.selection = m.selection.parent
                        if LAST == "left":
                            m.x_shift = WIDTH / 2 - m.selection.rect[0]
                            m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                            set_all_rects()
                        elif LAST == "right":
                            m.x_shift = WIDTH / 2 - m.selection.rect[0]
                            m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                            set_all_rects()
                    else:
                        print("no parent to be selected")
                elif event.key == K_LEFT:
                    if m.selection.left:
                        m.selection = m.selection.left
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                        set_all_rects()
                        LAST = "left"
                    else:
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                        insert_node_left(m.selection, m.selection.depth)
                        set_all_rects()
                elif event.key == K_RIGHT:
                    if m.selection.right:
                        m.selection = m.selection.right
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                        set_all_rects()
                        LAST = "right"
                    else:
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                        insert_node_right(m.selection, m.selection.depth)
                        set_all_rects()
                elif event.key == K_RETURN:
                    inter = False
                else:
                    print("invalid keyboard input: '%s' (%d)" % (pygame.key.name(event.key), event.key))
    build(True)


# Draws the current screen, with the current tree and information on how to traverse the caves
def draw(control):
    for depth_level in m.nodelist:
        for node in depth_level:
            node.draw()
    if m.selection and control is True:
        s_rect = pygame.rect.Rect(m.selection.rect.topleft, m.selection.rect.size)
        s_rect.top += m.y_shift
        s_rect.left += m.x_shift

        # Node Info
        text = FONT2.render("Node depth: %d" % m.selection.depth, 1, (200, 255, 255))
        trect = text.get_rect()
        trect.center = m.display.get_rect().center
        trect.bottom = m.display.get_rect().bottom - 10
        m.display.blit(text, trect)

        # Help
        help = FONT.render("UP - go to parent, LEFT/RIGHT - travel down tree", 1, (255, 180, 180))
        help2 = FONT.render("W - Move screen up, A - Move screen left, S - Move screen down, D - Move screen right", 1,
                            WHITE)
        help3 = FONT.render("R - Reset Tree", 1, WHITE)
        hrect = help.get_rect()
        hrect.centerx = trect.centerx
        hrect.top = trect.top - trect.height
        m.display.blit(help, hrect)
        hrect.top -= hrect.height
        m.display.blit(help2, hrect)
        hrect.top -= hrect.height
        m.display.blit(help3, hrect)


def pauseHelp():
    for depth_level in m.nodelist:
        for node in depth_level:
            node.draw()
    if m.selection:
        s_rect = pygame.rect.Rect(m.selection.rect.topleft, m.selection.rect.size)
        s_rect.top += m.y_shift
        s_rect.left += m.x_shift
        text = FONT2.render("Node depth: %d" % m.selection.depth, 1, (200, 255, 255))
        trect = text.get_rect()
        trect.center = m.display.get_rect().center
        trect.bottom = m.display.get_rect().bottom - 10
        help = FONT.render("W - Move screen up, A - Move screen left, S - Move screen down, D - Move screen right", 1,
                           WHITE)
        help2 = FONT.render("ENTER - Continue Program", 1, WHITE)
        hrect = help.get_rect()
        hrect.centerx = trect.centerx
        hrect.top = trect.top - trect.height
        m.display.blit(help, hrect)
        hrect.top -= hrect.height
        m.display.blit(help2, hrect)


# Creates a single, starting parent node
def create_root_node():
    root = Node(depth=0)
    root.type = "root"
    add_new_node(root, 0)
    return root


# Builds a tree based on a single starting parent node
def build_tree():
    m.nodelist = []
    root = create_root_node()
    set_all_rects()
    m.selection = root
    return root


# Builds a randomized tree, with a nodecount of NUM_OF_NODES and a starting parent node with depth 0
def build_rand_tree():
    root = create_root_node()
    m.selection = root
    while root.count_children() < NUM_OF_NODES:
        rand = random.randint(0, 3)
        if rand == 1:
            if m.selection.left:
                m.selection = m.selection.left
            else:
                insert_node_left(m.selection, m.selection.depth)
                set_all_rects()
        if rand == 2:
            if m.selection.right:
                m.selection = m.selection.right
            else:
                insert_node_right(m.selection, m.selection.depth)
                set_all_rects()
        if rand == 3:
            if m.selection.parent:
                m.selection = m.selection.parent
    for x in range(NUM_OF_NODES):
        if m.selection.parent:
            m.selection = m.selection.parent
    return root

# tree1() and tree2() build hard coded trees that will be used to explain searches. We wanted to avoided having
# degenerate trees pop up which could happen with the low node count, so we opted to hard code the trees K-2 will
# look at which avoids this issue.
def tree1():
    root = create_root_node()
    m.selection = root
    insert_both(root, root.depth)
    insert_node_right(root.right, root.right.depth)
    insert_both(root.left, root.right.depth)
    m.selection = root.left
    m.selection = m.selection.right
    insert_node_left(m.selection, m.selection.depth)
    while m.selection.parent:
        m.selection = m.selection.parent
    set_all_rects()
    return root

def tree2():
    root = create_root_node()
    m.selection = root
    insert_both(root, root.depth)
    insert_both(root.right, root.right.depth)
    insert_node_right(root.left, root.left.depth)
    m.selection = root.left
    insert_node_left(m.selection.right, m.selection.right.depth)
    m.selection = root.right
    insert_node_left(m.selection.left, m.selection.left.depth)
    m.selection = m.selection.parent
    set_all_rects()
    return root

# Builds a single parent node as a tree, for displaying an example of a parent node
def build_single_root():
    root = create_root_node()
    m.selection = root
    set_all_rects()
    return root


# Builds a single parent with 2 children nodes, for displaying an example of a parent with 2 children nodes
def parent_with_two_children():
    root = build_single_root()
    m.selection = root
    insert_both(root, root.depth)
    set_all_rects()
    return root


# Inserts both a left and a right node for a root (parent) node
def insert_both(root, depth):
    insert_node_left(root, depth)
    insert_node_right(root, depth)


# Adds a new node to the m.nodelist[depth] which allows us to know how many nodes a tree has
def add_new_node(leaf, depth):
    try:
        m.nodelist[depth].append(leaf)
    except:
        m.nodelist.append([])
        m.nodelist[depth].append(leaf)


# Inserts a node to the right for a current tree
def insert_node_right(node, depth):
    # print("insert_node_right \nnode.rect: ", node.rect)
    node.right = Node(parent=node)
    node.right.type = "right"
    node.right.depth = depth + 1
    add_new_node(node.right, depth + 1)


# Inserts a node to the left for a current tree
def insert_node_left(node, depth):
    # print("insert_node_left \nnode.rect: ", node.rect)
    node.left = Node(parent=node)
    node.left.type = "left"
    node.left.depth = depth + 1
    add_new_node(node.left, depth + 1)


# Sets the position of all nodes at all depths
def set_all_rects():
    arrayOfCoords = []
    for layer in m.nodelist:
        for node in layer:
            node.set_rect(arrayOfCoords)


def random_search(tar):
    stepCount = 0
    while True:
        build()
        pygame.time.wait(500)
        if m.selection.value == tar:
            while m.selection.parent:
                m.selection = m.selection.parent
            return stepCount
        rand = random.randint(0, 3)
        if rand == 1:
            if m.selection.left:
                m.selection = m.selection.left
                stepCount = stepCount + 1
        if rand == 2:
            if m.selection.right:
                m.selection = m.selection.right
                stepCount = stepCount + 1
        if rand == 3:
            if m.selection.parent:
                m.selection = m.selection.parent
                stepCount = stepCount + 1


# Block of code used to run a depth first search for cave with the value of "tar"
def depth_first_search(root, tar, step=0, stepCount=0):
    if root:
        if root.value == tar:
            stepCount = step
        if root.left:
            step = step + 1
            stepCount = depth_first_search(root.left, tar, step, stepCount)
        m.selection = root
        build()
        pygame.time.wait(2000)
        if root.right:
            step = step + 1
            stepCount = depth_first_search(root.right, tar, step, stepCount)
    while m.selection.parent:
        m.selection = m.selection.parent
    return stepCount


# Block of code that will be used to breadth first search for the cave will a value of "tar"
def breadth_first_search(tar):
    steps = 0
    stepCount = 0
    tempArray = [m.selection]
    while len(tempArray) > 0:
        curNode = tempArray.pop(0)
        m.selection = curNode
        build()
        pygame.time.wait(2000)
        stepCount = stepCount + 1
        if curNode.value == tar:
            steps = stepCount
        if curNode.left:
            tempArray.append(curNode.left)
        if curNode.right:
            tempArray.append(curNode.right)
    return steps


# Builds the current version of the tree we are wanting. The parameter control will determine whether or not to write
# instructions at the bottom of the screen. It will be true whenever the user has the ability to build their own tree
def build(control=None):
    pic_select = pygame.image.load(r'resources/background.jpg')
    pic_select = pygame.transform.scale(pic_select, (WIDTH, HEIGHT))
    screen.blit(pic_select, [0, 0])

    # These images came from this URL: https://scribblenauts.fandom.com/wiki/Miner
    # We do not take credit for the male and female miner .png's used in this game
    # We are not profiting off of this and can change the pictures if need be
    if m.voice:
        miner_select = pygame.image.load(r'resources/Miner2.png')
        miner_select = pygame.transform.scale(miner_select, (74, 130))
    elif not m.voice:
        miner_select = pygame.image.load(r'resources/Miner_Female2.png')
        miner_select = pygame.transform.scale(miner_select, (74, 130))
    # The numbers change the space between this character and the edge of the window
    screen.blit(miner_select, [10, 10])

    draw(control)
    pygame.display.flip()


# Similar to build(), but places a different set of instructions at the bottom of the screen.
def pauseBuild():
    pic_select = pygame.image.load(r'resources/background.jpg')
    pic_select = pygame.transform.scale(pic_select, (WIDTH, HEIGHT))
    screen.blit(pic_select, [0, 0])

    # These images came from this URL: https://scribblenauts.fandom.com/wiki/Miner
    # We do not take credit for the male and female miner .png's used in this game
    # We are not profiting off of this and can change the pictures if need be
    if m.voice:
        miner_select = pygame.image.load(r'resources/Miner2.png')
        miner_select = pygame.transform.scale(miner_select, (74, 130))
    elif not m.voice:
        miner_select = pygame.image.load(r'resources/Miner_Female2.png')
        miner_select = pygame.transform.scale(miner_select, (74, 130))
    # The numbers change the space between this character and the edge of the window
    screen.blit(miner_select, [10, 10])

    pauseHelp()
    pygame.display.flip()


# initialization
m = Master()
m.intro_screen()
m.voice_selection()
talk("Hello and welcome to Spelunkster 3000.")
root = build_single_root()
build()
talk('Describe purpose of program. Single root is shown. Narrator voice.')
m.reset()
root = parent_with_two_children()
talk('Describe how caves are added to root node. Parent with two children shown. Narrator voice.')
m.reset()
root = tree1()
build()
talk('This is the cave they will look at the most. Currently random, will include standard cave later. Begin to '
     'explain searches in terms of characters moving through caves. Depth-first is Left-Root-Right and Breadth first '
     'is level by level. We have been getting them mixed up this whole time. I fixed the old code to reflect this. '
     'Narrator voice.')
talk('Have each character introduce themselves probably. Try and explain why they do what they do. Use appropriate '
     'voice.')
target = 4
talk("First, lets see how -name- digs a cave. This can either be really quick or really slow.")
randCount = random_search(target)
talk("A random search of the tree took " + str(randCount) + "searches to find the target.")
talk("Now we will see how -name- searches a cave system.")
breadthCount = breadth_first_search(target)
build()
talk("A breadth first search of the tree took " + str(breadthCount) + "searches to find the target.")
talk("Finally, lets see how -name- searches a cave system.")
depthCount = depth_first_search(root, target)
build()
talk("Finally, a depth first search of the tree took " + str(depthCount) + "searches to find the target.")

talk('After this maybe run the searches again on a different tree, prompting them to guess which one is faster. Tell '
     'them how the pause menu works (WASD moves screen, enter to continue).')
m.reset()
root = tree2()
build()
pause()
talk("First, lets see how -name- digs a cave. This can either be really quick or really slow.")
randCount = random_search(target)
talk("A random search of the tree took " + str(randCount) + "searches to find the target.")
talk("Now we will see how -name- searches a cave system.")
breadthCount = breadth_first_search(target)
build()
talk("A breadth first search of the tree took " + str(breadthCount) + "searches to find the target.")
talk("Finally, lets see how -name- searches a cave system.")
depthCount = depth_first_search(root, target)
build()
talk("Finally, a depth first search of the tree took " + str(depthCount) + "searches to find the target.")
talk('Outro.')
quit()
