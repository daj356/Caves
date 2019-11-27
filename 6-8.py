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
# # Sets a male voice
# engine.setProperty('voice', voices[0].id)
#
# # Sets a female voice
# engine.setProperty('voice', voices[1].id)

print(voices)

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
NUM_OF_NODES = 30
MAX_NUM = 100
KEYBOARD_PAN_STEP = 50


# A bit more confusing, Master is the whole display, tree and all. Nodelist and Count are pretty self-explanatory,
# they hold information about the tree. X_shift and Y_shift control how the WASD controls move the camera. Idk what
# the clock is for tbh. Selection handles which key the user is pressing. All usages of "m" is the initialized Master.
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

            # Main Menu UI
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
            pygame.display.set_caption("Main Menu")


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


def talk(say):
    engine.say(say)
    engine.runAndWait()


# Quits the game
def quit():
    print("QUIT")
    pygame.quit()
    sys.exit()


# Controls user input. Interface() works similarly, but pause allows to user only to move the screen display and hit
# enter to continue the program.
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


# Same function as pause(), but allows extra functionality of using arrow keys to move through the tree and add nodes
# and R to reset the tree.
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


# Draws nodes and add instructions for the 'pause' screen.
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


# Builds a hard-coded full binary tree. Guaranteed to be a full binary tree
def build_full_tree():
    root = create_root_node()
    m.selection = root
    insert_both(root, root.depth)
    root = root.left
    insert_both(root, root.depth)
    root = root.parent
    root = root.right
    insert_both(root, root.depth)
    root = root.left
    insert_both(root, root.depth)
    root = m.selection
    root = root.left
    root = root.left
    insert_both(root, root.depth)
    root = root.right
    insert_both(root, root.depth)
    root = root.parent
    root = root.left
    insert_both(root, root.depth)

    set_all_rects()
    return root


# Builds a complete binary tree, every parent has 2 children nodes
def build_comp_tree():
    root = create_root_node()
    m.selection = root
    insert_both(root, root.depth)
    root = root.left
    insert_both(root, root.depth)
    root = m.selection
    root = root.right
    insert_both(root, root.depth)
    root = m.selection
    root = root.left
    root = root.left
    insert_both(root, root.depth)
    root = root.parent
    root = root.right
    insert_both(root, root.depth)
    root = m.selection

    set_all_rects()
    return root


# Builds a perfect binary tree, all interior nodes have two children and
# for every parent node, the two children nodes are at the same depth
def build_perfect_tree():
    root = create_root_node()
    m.selection = root
    insert_both(root, root.depth)
    root = root.left
    insert_both(root, root.depth)
    root = m.selection
    root = root.right
    insert_both(root, root.depth)
    root = m.selection
    root = root.left
    root = root.left
    insert_both(root, root.depth)
    root = root.parent
    root = root.right
    insert_both(root, root.depth)
    root = m.selection
    root = root.right
    root = root.left
    insert_both(root, root.depth)
    root = root.parent
    root = root.right
    insert_both(root, root.depth)

    set_all_rects()
    return root


# Inserts both a left and a right node for a root (parent) node
def insert_both(root, depth):
    insert_node_left(root, depth)
    insert_node_right(root, depth)


# Builds a degenerate tree, where each parent only has one child
def build_degen_tree():
    root = create_root_node()
    m.selection = root
    # Randomly chooses if degen tree should be left or right
    rand = random.randint(0, 1)
    if rand == 0:
        while root.count_children() < NUM_OF_NODES:
            # If/else statement creates node.
            if m.selection.left:
                m.selection = m.selection.left
            else:
                insert_node_left(m.selection, m.selection.depth)
                set_all_rects()
    if rand == 1:
        while root.count_children() < 6:
            if m.selection.right:
                m.selection = m.selection.right
            else:
                insert_node_right(m.selection, m.selection.depth)
                set_all_rects()
    return root


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
        m.selection.visit = 1
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
        if root.right:
            step = step + 1
            stepCount = depth_first_search(root.right, tar, step, stepCount)
    while m.selection.parent:
        m.selection = m.selection.parent
    return stepCount


# Block of code that will be used to breadth first search for the cave will a value of "tar"
def breadth_first_search(tar):
    stepCount = 0
    tempArray = [m.selection]
    while len(tempArray) > 0:
        curNode = tempArray.pop(0)
        m.selection = curNode
        if curNode.value == tar:
            return stepCount
        if curNode.left:
            tempArray.append(curNode.left)
        if curNode.right:
            tempArray.append(curNode.right)


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


# Checks to see if the tree is a full tree. Returns false if any node has only 1 child. Returns true if all nodes
# have zero or two children.
def checkFull():
    for depth_level in m.nodelist:
        for node in depth_level:
            if (node.left and node.right is None) or (node.right and node.left is None):
                return False
    return True


def endInstruct():
    pic_select = pygame.image.load(r'resources/background.jpg')
    pic_select = pygame.transform.scale(pic_select, (WIDTH, HEIGHT))
    screen.blit(pic_select, [0, 0])
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
        help = FONT.render("1 - Redo Tree Building", 1,
                           WHITE)
        help2 = FONT.render("ENTER - Continue Program", 1, WHITE)
        hrect = help.get_rect()
        hrect.centerx = trect.centerx
        hrect.top = trect.top - trect.height
        m.display.blit(help, hrect)
        hrect.top -= hrect.height
        m.display.blit(help2, hrect)
    pygame.display.flip()


# initialization
m = Master()
m.intro_screen()
m.voice_selection()
talk("Hello and welcome to Spelunkster 3000.")

root = build_single_root()
build()
talk("Today, we're going to explore binary trees, and hopefully learn a thing or two along the way. Let's go! ")
talk("Binary trees are most commonly used in computer science, which is the science behind your phone, your "
     "computer, your video games, and a lot of other electronic devices we use today. In computer science, you "
     "can think of a binary tree as a system of circles, or nodes, or as we think of it here, as a system of "
     "caves. Each cave is connected by a tunnel, a tunnel dug out of one cave and into another. These tunnels "
     "create a system that links everything together. At the very top of a binary tree is one root node, or "
     "cave, like this ")

m.reset()
root = parent_with_two_children()
build()
talk("This cave, at the top, is called a parent node, and like a lot of parents, it can have children. "
     "Every parent node in a binary tree can have either one, two, or no children at all. Here's what a parent "
     "node with two children looks like ")

m.reset()
root = build_comp_tree()
build()
talk("Ok, now that we know what a binary tree is, we can take a look at all the different types of binary trees "
     "there are. What you see now is one example. This binary tree is called a complete binary tree. What makes "
     "a binary tree complete? Well, a binary tree is complete if you can look at it top to bottom, and left to "
     "right, and find no empty spaces between all the way through. See if you can tell whether this binary tree is "
     "complete or not.")
talk("Since all of the circles, or nodes are filled between the first cave and the last cave, this tree can be "
     "rightly called 'complete'.")

m.reset()
root = build_full_tree()
build()
talk("Moving along to our next example. What you see now is a type of a binary tree called a full binary tree. "
     "A full binary tree is a tree where every parent node has either two children, or no children at all. "
     "The parent nodes that don't have any children, those nodes are called 'leaves', and, just like real tree "
     "leaves don't have branches growing out of them, binary leaf nodes have no links, or tunnels.")

m.reset()
root = build_rand_tree()
build()
talk("Let's see what we've learned. Look at the binary tree here, represented as a system of caves, with tunnels "
     "dug from one cave to another. Does the system of caves shown here represent a full binary tree? If you'd like "
     "to move the screen, to get a better look, press W to go up, S to move down, A to move left and D to move right. "
     "If you think you know the tree is or is not a full binary tree hit enter to continue. Remember, a full binary "
     "tree is a binary tree where every parent node has either two children, or no children at all ")
pause()
answer = checkFull()
if not answer:
    talk("Drum roll please, bahdahbahdahbahdah clash. The answer is. no. This tree is not a full binary tree. It isn't "
         "a full binary tree because not all of the parent nodes have two child nodes.")
else:
    talk("Drum roll please, bahdahbahdahbahdah clash. The answer is yes, because all nodes have 2 or zero children.")

m.reset()
root = build_degen_tree()
build()
talk("Here we have what you call a degenerate tree. A binary tree is called degenerate when each parent node has "
     "only one child. When you try and search a tree, which is something we'll get into soon, this tree, the "
     "degenerate tree, is the worst to sort. Can you think of any reasons why it's so tough to sort this tree?")

m.reset()
root = build_perfect_tree()
build()
talk("Our next tree is known as a perfect binary tree. Why is it perfect? Well, as you can see, all the parent nodes "
     "have two children, except the ones at the very bottom. Remember what these nodes at the bottom are called? The "
     "nodes that don't have any branches, or caves that don't have any tunnels, coming out of them?")
talk("If you said 'leaves', you're right! And if you didn't, now you know. ")

m.reset()
root = build_rand_tree()
build()
talk("Remember when we talked about 'searching' a binary tree, just a few moments ago? Well, now we're going to "
     "learn what searching a binary tree means. Let's go!")
talk("A binary tree is searching with a function. You can think of a function as something that takes in one thing, "
     "and puts out another. A lot of functions are used to search a binary tree. We'll look at two functions. One "
     "of these is called a depth-first-search. The other is known as a breadth-first-search. ")
talk("Let's talk about the breadth first search function first. This function will take in a tree, then search each "
     "node in that tree, level by level, starting at the top, and moving down, one level at a time. At each level, "
     "the search will move from left to right along the tree, then continue down another level, and so on, looking "
     "for whatever you want the tree to find.")
talk("The next function, the depth-first-search, has an order preference of 'left-root-right'. This can be "
     "confusing, so listen up. The first thing this search algorithm will do is it will move to a left node if it's "
     "possible. If it is no longer possible to move left, it will search the node it is at. The algorithm will then "
     "search the previous node that it just came from. Next, if it can move to a right node, it will do that. It will "
     "then restart its process of 'left-root-right', attempting to move left if possible. Like other search methods, "
     "it will not search the same node twice.")
temp = int(m.nodecount) - 1
temp2 = int(m.nodecount / 2)
target = random.randint(temp2, temp)
talk("Now that we know how to search a binary tree, let's interact with one. See if you can guess how long it will "
     "take for both search algorithms to find cave number " + str(target) + ". Again, use the keys W, A, S, and D to "
     "move the screen and press enter when you want to check your answer.")
pause()
randCount = random_search(target)
breadthCount = breadth_first_search(target)
depthCount = depth_first_search(root, target)

talk("A random search of the tree took " + str(randCount) + "searches to find the target.")
talk("A breadth first search of the tree took " + str(breadthCount) + "searches to find the target.")
talk("Finally, a depth first search of the tree took " + str(depthCount) + "searches to find the target.")

talk("Now let's have some fun creating binary trees of our own. Try making your own binary tree using our cave system. "
     "Can you make a full binary tree? A perfect tree? What about a degenerate tree? Only one way to find out. Press "
     "the left and right arrow keys to create a cave, or use the up and down arrow keys to dig through your caves. "
     "Press the enter key when you are done building the cave, or continue digging caves until you've dug "
     + str(NUM_OF_NODES) + " caves!")
loop = True
while loop is True:
    m.reset()
    root = build_single_root()
    build(True)
    interface()
    temp = int(m.nodecount) - 1
    temp2 = int(m.nodecount / 2)
    target = random.randint(temp2, temp)
    talk(
        "Now, with your binary tree cave system built, try and apply what you know about breadth first search and depth"
        " first search functions to guess which search will find cave number " + str(target) + " the fastest. But, "
        "before you do, keep in mind that a depth first search function likes to move left, then right, while a"
        " breadth first search function likes to move left to right, from one level to the next level.")
    talk("Look around the tree and write down an answer. Press ENTER when you are ready to check your answer.")
    randCount = random_search(target)
    breadthCount = breadth_first_search(target)
    depthCount = depth_first_search(root, target)
    pause()
    talk("Random search took " + str(randCount) + " steps, breadth first search took " + str(breadthCount) +
         " steps and depth first search took " + str(depthCount) + " steps.")
    if randCount <= breadthCount and randCount <= depthCount:
        talk("Would you look at that! Seems like searching the binary tree at random was faster than our best "
             "function. This can happen, but it's more likely that a set process will work faster.")
    talk("Was your answer correct? If you would like to build another tree, please press 1 to go again, or press enter "
         "to finish the program.")
    endInstruct()
    inputLoop = True
    while inputLoop is True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    loop = False
                    inputLoop = False
                elif event.key == K_1:
                    inputLoop = False
talk("Binary trees are pretty cool. What's cooler, you can find tree-like systems everywhere, not just in computer "
     "science. Ever heard of Charles Darwin? Darwin's theory of evolution started with a tree. A lot like a binary "
     "tree. Not just Darwin, though. The english language is explained using tree-like systems too. Grammar, for "
     "instance, is explained by displaying sentences and the rules of producing them using a tree. Music, too. The "
     "different lengths of a musical note are explained clearly by a binary search tree, a perfect binary search tree, "
     "to be exact. Even your family tree, with all your ancestors, is, in one way or another, a system of nodes and "
     "links. So binary trees are important structures that help explain a lot of different things about life and how "
     "to make sense of the world, and they can be used to dig pretty cool caves, too.")
quit()
