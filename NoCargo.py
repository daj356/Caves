import pygame
import sys
import os
import random
import pyttsx3
from pygame.locals import *

engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Speed percent

voices = engine.getProperty('voices')
# Sets a female voice
engine.setProperty('voice', voices[1].id)

# Initializes pygame
pygame.init()

# Get the screen resolution
screen = pygame.display.set_mode((1280, 800), FULLSCREEN)

# Sets the current window caption
pygame.display.set_caption("Spelunker")

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

# Fonts

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
MAX_NUM = 100
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

    # Text Renderer
    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText

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

                            '''
                        if selected == "info":
                            intro_screen = False
                            m.info_screen()
                            '''
            # index %= len(menu_selection_list)

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

    '''
    def info_screen(self):
        info_screen = True
        selected = start

        # if event.key == pygame.K_RETURN:
        # if selected == "start":
        #     info_screen = False

        # Main Menu UI
        screen.fill(BLACK)
        title = m.text_format("SPELUNKSTER 3000", TITLE_FONT, 65, RED)
        if selected == "start":
            text_start = self.text_format("START", OPTIONS_FONT, 85, YELLOW)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()

        # Main Menu Text
        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 250))
        # screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 320))
        # screen.blit(text_info, (WIDTH / 2 - (info_rect[2] / 2), 390))
        pygame.display.update()
        self.clock.tick(60)
        pygame.display.set_caption("Info")
        '''


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

    def __str__(self):  # Used to give information about the depth. Displayed at bottom of the screen.
        return "NODE depth: %d" % self.depth

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
                tempArray[0] = tempArray[0] - 30
                mod = mod - 30
            if self.type == "left":
                tempArray[0] = tempArray[0] + 30
                mod = mod + 30
        arrayOfCoords.append(tempArray)
        # ARRAY COORDS DOES WHAT
        # print(arrayOfCoords)
        self.rect = pygame.rect.Rect((x + mod, y), BOX_SIZE)

    def draw(self):

        # pic = pygame.image.load(r'resources/pic.png')
        # pic = pygame.transform.scale(pic, (30, 30))
        rect = pygame.rect.Rect(self.rect.left + m.x_shift, self.rect.top + m.y_shift,
                                self.rect.width, self.rect.height)
        if BOX_SIZE[0] >= 10:  # skip text if box is too small
            text = FONT.render(str(self.value), 1, WHITE)
            tr = text.get_rect()
            tr.center = rect.center
            m.display.blit(text, tr)
            # m.display.blit(pic, tr)
        pygame.draw.rect(m.display, BLUE, rect, 1)
        if self.parent:
            start = (rect.centerx, rect.top)
            end = (self.parent.rect.centerx + m.x_shift, self.parent.rect.bottom + m.y_shift)
            pygame.draw.aaline(m.display, GREEN, start, end)  # This is the line that actually draws the box.

    def count_children(self):  # Recursive function to count children.
        count = 0
        if self.left:
            count += 1
            count += self.left.count_children()
        if self.right:
            count += 1
            count += self.right.count_children()
        return count


def quit():
    print("QUIT")
    pygame.quit()
    sys.exit()


def interface():
    global LAST
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_q, K_ESCAPE]:
                quit()
            elif event.key == K_r:
                m.nodecount = 1
                build_tree()
                ''' Kept these just in case
            elif event.key == K_w:
                m.y_shift += KEYBOARD_PAN_STEP
            elif event.key == K_s:
                m.y_shift -= KEYBOARD_PAN_STEP
            elif event.key == K_a:
                m.x_shift += KEYBOARD_PAN_STEP
            elif event.key == K_d:
                m.x_shift -= KEYBOARD_PAN_STEP
                '''
            elif event.key == K_UP:
                if m.selection.parent:
                    m.selection = m.selection.parent
                    if LAST == "left":
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                    elif LAST == "right":
                        m.x_shift = WIDTH / 2 - m.selection.rect[0]
                        m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                else:
                    print("no parent to be selected")
            elif event.key == K_LEFT:
                if m.selection.left:
                    m.selection = m.selection.left
                    m.x_shift = WIDTH / 2 - m.selection.rect[0]
                    m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                    LAST = "left"
                else:
                    print("no left-child to be selected")
            elif event.key == K_RIGHT:
                if m.selection.right:
                    m.selection = m.selection.right
                    m.x_shift = WIDTH / 2 - m.selection.rect[0]
                    m.y_shift = HEIGHT / 2 - m.selection.rect[1]
                    LAST = "right"
                else:
                    print("no right-child to be selected")
            else:
                print("invalid keyboard input: '%s' (%d)" % (pygame.key.name(event.key), event.key))


def draw():
    for depth_level in m.nodelist:
        for node in depth_level:
            node.draw()
    if m.selection:
        s_rect = pygame.rect.Rect(m.selection.rect.topleft, m.selection.rect.size)
        s_rect.top += m.y_shift
        s_rect.left += m.x_shift
        pygame.draw.rect(m.display, RED, s_rect, 4)

        # Node Info
        text = FONT2.render("Node depth: %d" % m.selection.depth, 1, (200, 255, 255))
        trect = text.get_rect()
        trect.center = m.display.get_rect().center
        trect.bottom = m.display.get_rect().bottom - 10
        m.display.blit(text, trect)

        # Help
        help = FONT.render("UP - go to parent, LEFT/RIGHT - travel down tree", 1, (255, 180, 180))
        help2 = FONT.render("R - create new random tree", 1, WHITE)
        hrect = help.get_rect()
        hrect.centerx = trect.centerx
        hrect.top = trect.top - trect.height
        m.display.blit(help, hrect)
        hrect.top -= hrect.height
        m.display.blit(help2, hrect)


def create_root_node():
    root = Node(depth=0)
    root.type = "root"
    add_new_node(root, 0)
    return root


def build_tree():
    m.nodelist = []
    root = create_root_node()
    set_all_rects()

    walk_tree(root)

    m.selection = root
    return root


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


def build_single_root():
    root = create_root_node()
    m.selection = root
    set_all_rects()
    return root


def parent_with_two_children():
    root = build_single_root()
    m.selection = root
    insert_both(root, root.depth)
    set_all_rects()
    return root


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


def insert_both(root, depth):
    insert_node_left(root, depth)
    insert_node_right(root, depth)


# Degenerate tree
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


def add_new_node(leaf, depth):
    try:
        m.nodelist[depth].append(leaf)
    except:
        m.nodelist.append([])
        m.nodelist[depth].append(leaf)


def insert_node_right(node, depth):
    # print("insert_node_right \nnode.rect: ", node.rect)
    node.right = Node(parent=node)
    node.right.type = "right"
    node.right.depth = depth + 1
    add_new_node(node.right, depth + 1)


def insert_node_left(node, depth):
    # print("insert_node_left \nnode.rect: ", node.rect)
    node.left = Node(parent=node)
    node.left.type = "left"
    node.left.depth = depth + 1
    add_new_node(node.left, depth + 1)


def walk_tree(leaf):
    if leaf.left:
        walk_tree(leaf.left)
    if leaf.right:
        walk_tree(leaf.right)


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


# Block of code used to run a breadth first search for cave with the value of "tar"
def breadth_first_search(tar):
    stepCount = 0
    tempArray = [m.selection]
    while len(tempArray) > 0:
        curNode = tempArray[0]
        if curNode.value == tar:
            while m.selection.parent:
                m.selection = m.selection.parent
            return stepCount
        if curNode.left:
            tempArray.append(curNode.left)
        if curNode.right:
            tempArray.append(curNode.right)
        tempArray.pop(0)
        stepCount = stepCount + 1


# Block of code that will be used to depth first search for the cave will a value of "tar"
def depth_first_search(tar):
    stepCount = 0
    tempArray = [m.selection]
    while len(tempArray) > 0:
        curNode = tempArray.pop()
        if curNode.value == tar:
            return stepCount
        stepCount = stepCount + 1
        if curNode.right:
            tempArray.append(curNode.right)
        if curNode.left:
            tempArray.append(curNode.left)


def build():
    m.display.fill(BLACK)
    draw()
    pygame.display.flip()


# initialization
m = Master()
m.intro_screen()
talk("Hello and welcome to Spelunkster 3000")


root = build_single_root()
build()
talk("In this program, we will explain a little bit about binary trees, which is useful knowledge for computer "
     "science. A binary tree can be visualized like a system of caves, with parent and children caves. An example "
     "of a parent cave is shown on the screen.")

m.reset()
root = parent_with_two_children()
build()
talk("Every parent cave can have one, two, or no children caves (also known as leaves). "
     "A parent with two children is shown on the screen.")


m.reset()
root = build_comp_tree()
build()
talk("Here is an example of a complete binary tree. "
     "A binary tree is complete if looking top to bottom, and left to right, there are no empty spaces "
     "until the end of the cave system. Because there are no missing nodes in between the first cave and "
     "the last, this tree is considered 'complete'.")


m.reset()
root = build_full_tree()
build()
talk("This is also a complete binary tree.")


m.reset()
root = build_rand_tree()
build()
talk("Question: Does the cave system shown represent a complete binary tree?")
talk(" ")
talk("The answer is no, because not all of the parent nodes have 2 children nodes.")

m.reset()
root = build_degen_tree()
build()
talk("This tree is what we call a degenerate tree. A tree is called a degenerate tree "
     "where there is only 1 child node for each parent node. It is unbalanced and "
     "is considered the worst case when it comes to sorting through a tree. ")

m.reset()
root = build_perfect_tree()
build()
talk("This tree is called a perfect binary tree. All interior nodes have two children and "
     "all of the children caves (also known as leaves) have the same depth in the tree. "
     "The depth of a tree is a fancy way of representing which level a node is at. ")

target = 9

randCount = random_search(target)
breadthCount = breadth_first_search(target)
depthCount = depth_first_search(target)

print("Number of steps for rand: " + str(randCount))
print("Number of steps for breadth: " + str(breadthCount))
print("Number of steps for depth: " + str(depthCount))

while True:
    m.clock.tick(60)
    interface()
    m.display.fill(BLACK)
    draw()
    pygame.display.flip()
