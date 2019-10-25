import pygame
import sys
import os
import random
from pygame.locals import *
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 115) # Speed percent
voices = engine.getProperty('voices')
engine.say('You\'ve got mail.')
engine.runAndWait()


WIDTH = 800
HEIGHT = 600
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WIDTH/2, HEIGHT/2)

pygame.init()
# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("Spelunker")
pygame.key.set_repeat(200, 20)
# infoObject contains information about the users display settings e.g. resolution
infoObject = pygame.display.Info()
# Display should fit to users resolution
# IMPORTANT: WANT THIS TO BE FULLSCREEN, CURRENTLY GETS CUT OFF AT THE BOTTOM
screen = pygame.display.set_mode([WIDTH, HEIGHT])
# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
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
NUM_OF_NODES = 100
MAX_NUM = 100
KEYBOARD_PAN_STEP = 50


# A bit more confusing, Master is the whole display, tree and all. Nodelist and Count are pretty self-explanatory,
# they hold information about the tree. X_shift and Y_shift control how the WASD controls move the camera. Idk what
# the clock is for tbh. Selection handles which key the user is pressing. All usages of "m" is the initialized Master.
class Master(object):
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        # nodelist - a 2d array of nodes sorted by depth level,
        # it is initialized as empty, layers added as needed
        self.nodelist = []
        self.nodecount = 0
        self.x_shift = 0
        self.y_shift = 0
        self.clock = pygame.time.Clock()
        self.selection = None


# Every node is an object. It has information about its parent, cargo (the number it contains), the node to the left
# and right and the depth.
class Node(object):
    def __init__(self, parent=None, cargo=None, right=None, left=None, depth=None):
        self.type = None
        self.parent = parent
        self.cargo = cargo
        self.right = right
        self.left = left
        self.depth = depth
        self.rect = None
        m.nodecount += 1

    def __str__(self):  # Used to give information about the cargo and depth. Displayed at bottom of the screen.
        return "NODE - cargo: %d depth: %d" % (self.cargo, self.depth)

    def set_rect(self):
        if self.type == "root":
            mod = 0
            x = ROOT_X
        elif self.type == "left":
            mod = -(X_STEP)
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
            print
            "unhandled case in set_rect()"
            sys.exit(1)
        if self.type in ["left", "right"]:
            x = self.parent.rect.left
        y = Y_START + Y_STEP * self.depth
        self.rect = pygame.rect.Rect((x + mod, y), BOX_SIZE)

    def draw(self):
        rect = pygame.rect.Rect(self.rect.left + m.x_shift, self.rect.top + m.y_shift,
                                self.rect.width, self.rect.height)
        if BOX_SIZE[0] >= 10:  # skip text if box is too small
            text = FONT.render(str(self.cargo), 1, WHITE)
            tr = text.get_rect()
            tr.center = rect.center
            m.display.blit(text, tr)
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
    print
    "QUIT"
    pygame.quit()
    sys.exit()


def interface():
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_q, K_ESCAPE]:
                quit()
            elif event.key == K_r:
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
                else:
                    print
                    "no parent to be selected"
            elif event.key == K_LEFT:
                if m.selection.left:
                    m.selection = m.selection.left
                else:
                    print
                    "no left-child to be selected"
            elif event.key == K_RIGHT:
                if m.selection.right:
                    m.selection = m.selection.right
                else:
                    print
                    "no right-child to be selected"
            else:
                print
                "invalid keyboard input: '%s' (%d)" % (pygame.key.name(event.key), event.key)


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
        text = FONT2.render("Node cargo: %d, depth: %d" % (m.selection.cargo, m.selection.depth), 1, (200, 255, 255))
        trect = text.get_rect()
        trect.center = m.display.get_rect().center
        trect.bottom = m.display.get_rect().bottom - 10
        m.display.blit(text, trect)

        # Help
        help = FONT.render("WASD - pan, UP - go to parent, LEFT/RIGHT - travel down tree", 1, (255, 180, 180))
        help2 = FONT.render("R - create new random tree", 1, WHITE)
        hrect = help.get_rect()
        hrect.centerx = trect.centerx
        hrect.top = trect.top - trect.height
        m.display.blit(help, hrect)
        hrect.top -= hrect.height
        m.display.blit(help2, hrect)


def create_root_node(cargo):
    root = Node(cargo=cargo, depth=0)
    root.type = "root"
    add_new_node(root, 0)
    m.nodecount += 1
    return root


def build_tree():
    m.nodelist = []
    root = create_root_node(MAX_NUM / 2)
    numlist = [n for n in range(MAX_NUM)]
    for n in range(NUM_OF_NODES):
        r = random.choice(numlist)
        numlist.remove(r)
        insert_node(root, r)
    set_all_rects()

    print
    "-" * 60
    walk_tree(root)

    m.selection = root
    return root


def add_new_node(leaf, depth):
    try:
        m.nodelist[depth].append(leaf)
    except:
        m.nodelist.append([])
        m.nodelist[depth].append(leaf)


def insert_node(leaf, cargo, depth=0):
    if not leaf.cargo:
        leaf.cargo = cargo
        leaf.depth = depth
    elif cargo < leaf.cargo:
        if not leaf.left:
            leaf.left = Node(parent=leaf)
            leaf.left.type = "left"
            add_new_node(leaf.left, depth)
        insert_node(leaf.left, cargo, depth + 1)
    elif cargo > leaf.cargo:
        if not leaf.right:
            leaf.right = Node(parent=leaf)
            leaf.right.type = "right"
            add_new_node(leaf.right, depth)
        insert_node(leaf.right, cargo, depth + 1)
    elif cargo == leaf.cargo:
        print
        "duplicate cargo"


def walk_tree(leaf):
    if leaf.left:
        walk_tree(leaf.left)
    if leaf.right:
        walk_tree(leaf.right)


def set_all_rects():
    for layer in m.nodelist:
        for node in layer:
            node.set_rect()


# initialization
m = Master()

root = build_tree()

print
"count: %d" % m.nodecount
print
"layers: %d" % (len(m.nodelist) + 1)
print
"root kids"
print
root.count_children()

while True:
    m.clock.tick(60)
    interface()
    m.display.fill(BLACK)
    draw()
    pygame.display.flip()
