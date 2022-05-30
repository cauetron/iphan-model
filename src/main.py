import math
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tracer import Tracer

from enum import Enum

DELAY = 1000//60

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
STEP_DISTANCE = 0.2
STEP_THETA = 0.2

moving_velocity = 1 # the velocity which you move within the model

objects_not_to_be_drawn = []

tracer = None

display_dim = (WINDOW_WIDTH, WINDOW_HEIGHT)
display_center = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
display = None

theta_vertical = 0 # the vertical angle which you are looking at the model
theta_horizontal = 0 # the vertical angle which you are looking at the model

camera = [0, 15, 0] # camera position

# variables to control each one of the four doors
doors_state = [False, False, False, False]
doors_theta = [0.0, 0.0, 0.0, 0.0]
doors_direction_of_movement = [-1, -1, -1, -1]

view_matrix = []    # the view matrix, we only keep track of it because we can't
                    # rotate the two axis at the same time without distortion

class Door(Enum):
    center = 0
    left = 1
    right = 2
    window = 3

class Pos(Enum):
    x = 0
    y = 1
    z = 2

class Visibility(Enum):
    hide = 0
    show = 1

def load_mesh(file_name):
    global tracer

    tracer = Tracer()
    tracer.load_mesh_from_file(file_name)

def init():
    global display
    global view_matrix

    pygame.init()
    display = pygame.display.set_mode(display_dim, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Modelagem IPHAN')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [1, 1, 0, 1])

    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(camera[Pos.x.value], camera[Pos.y.value], camera[Pos.z.value],
    0, 0, 0, 0, 0, 1)

    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    pygame.mouse.set_pos(display_center)

def move_camera_with_keypress(keypress):
    global camera
    global moving_velocity

    moving_distance = STEP_DISTANCE * moving_velocity

    if keypress[pygame.K_m]:
        moving_velocity += 1
    if keypress[pygame.K_n]:
        if moving_velocity > 1:
            moving_velocity -= 1

    if keypress[pygame.K_w]:
        camera[Pos.z.value] += moving_distance
        glTranslatef(0, 0, moving_distance)
    if keypress[pygame.K_s]:
        camera[Pos.z.value] -= moving_distance
        glTranslatef(0, 0,-moving_distance)
    if keypress[pygame.K_d]:
        camera[Pos.x.value] -= moving_distance
        glTranslatef(-moving_distance, 0, 0)
    if keypress[pygame.K_a]:
        camera[Pos.x.value] += moving_distance
        glTranslatef(moving_distance, 0, 0)
    if keypress[pygame.K_q]:
        camera[Pos.y.value] -= moving_distance
        glTranslatef(0, -moving_distance, 0)
    if keypress[pygame.K_e]:
        camera[Pos.y.value] += moving_distance
        glTranslatef(0, moving_distance, 0)

def view_update(mouse_pos, keypress):
    global view_matrix
    global theta_vertical, theta_horizontal

    glLoadIdentity()

    theta_vertical += mouse_pos[1] * STEP_THETA
    glRotatef(theta_vertical, 1, 0, 0)

    glPushMatrix()
    glLoadIdentity()

    move_camera_with_keypress(keypress)

    theta_horizontal += STEP_THETA
    glRotatef(mouse_pos[0] * STEP_THETA, 0, 1, 0)

    glMultMatrixf(view_matrix)
    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glPopMatrix()
    glMultMatrixf(view_matrix)

def change_obj_visibility(obj_name, force_visibility=None):
    global objects_not_to_be_drawn

    if force_visibility is None:
        if obj_name not in objects_not_to_be_drawn:
            objects_not_to_be_drawn.append(obj_name)
        else:
            objects_not_to_be_drawn.remove(obj_name)

    elif force_visibility == Visibility.hide and \
    obj_name not in objects_not_to_be_drawn:
        objects_not_to_be_drawn.append(obj_name)

    elif force_visibility == Visibility.show and \
    obj_name in objects_not_to_be_drawn:
        objects_not_to_be_drawn.remove(obj_name)

def visibility_update(keypress):
    global force_visibility

    if keypress[pygame.K_g]:
        change_obj_visibility("Ground_Floor")

    if keypress[pygame.K_c]:
        change_obj_visibility("Ceiling")

    if keypress[pygame.K_f]:
        change_obj_visibility("Ceiling_Frame.001")
        change_obj_visibility("Ceiling_Frame.002")
        change_obj_visibility("Ceiling_Frame.003")
        change_obj_visibility("Door_Frame.001")
        change_obj_visibility("Door_Frame.002")
        change_obj_visibility("Door_Frame.003")
        change_obj_visibility("Building_Frame")

    if keypress[pygame.K_b]:
        change_obj_visibility("Room")
        change_obj_visibility("Room_Upstairs")
        change_obj_visibility("Iphan_Frame.001")
        change_obj_visibility("Iphan_Frame.002")
        change_obj_visibility("Iphan_Frame.003")

    if keypress[pygame.K_u]:
        change_obj_visibility("Stairs_Base")
        change_obj_visibility("Stairs.001")
        change_obj_visibility("Stairs.002")

    if keypress[pygame.K_h]:
        change_obj_visibility("Ceiling", Visibility.hide)
        change_obj_visibility("Ceiling_Frame.001", Visibility.hide)
        change_obj_visibility("Ceiling_Frame.002", Visibility.hide)
        change_obj_visibility("Ceiling_Frame.003", Visibility.hide)
        change_obj_visibility("Door_Frame.001", Visibility.hide)
        change_obj_visibility("Door_Frame.002", Visibility.hide)
        change_obj_visibility("Door_Frame.003", Visibility.hide)
        change_obj_visibility("Building_Frame", Visibility.hide)
        change_obj_visibility("Room", Visibility.hide)
        change_obj_visibility("Room_Upstairs", Visibility.hide)
        change_obj_visibility("Stairs_Base", Visibility.hide)
        change_obj_visibility("Stairs.001", Visibility.hide)
        change_obj_visibility("Stairs.002", Visibility.hide)
        change_obj_visibility("Iphan_Frame.001", Visibility.hide)
        change_obj_visibility("Iphan_Frame.002", Visibility.hide)
        change_obj_visibility("Iphan_Frame.003", Visibility.hide)

    if keypress[pygame.K_j]:
        change_obj_visibility("Ceiling", Visibility.show)
        change_obj_visibility("Ceiling_Frame.001",  Visibility.show)
        change_obj_visibility("Ceiling_Frame.002",  Visibility.show)
        change_obj_visibility("Ceiling_Frame.003",  Visibility.show)
        change_obj_visibility("Door_Frame.001",  Visibility.show)
        change_obj_visibility("Door_Frame.002",  Visibility.show)
        change_obj_visibility("Door_Frame.003",  Visibility.show)
        change_obj_visibility("Building_Frame",  Visibility.show)
        change_obj_visibility("Room", Visibility.show)
        change_obj_visibility("Room_Upstairs",  Visibility.show)
        change_obj_visibility("Stairs_Base",  Visibility.show)
        change_obj_visibility("Stairs.001",  Visibility.show)
        change_obj_visibility("Stairs.002",  Visibility.show)
        change_obj_visibility("Iphan_Frame.001",  Visibility.show)
        change_obj_visibility("Iphan_Frame.002",  Visibility.show)
        change_obj_visibility("Iphan_Frame.003",  Visibility.show)

def change_state_door(door:int):
    global doors_state

    doors_state[door] = not doors_state[door]

def open_door(door:int):
    global doors_state
    global doors_theta
    global doors_direction_of_movement

    if 0 < doors_theta[door] < 90:
        doors_theta[door] += doors_direction_of_movement[door] * moving_velocity
        if doors_theta[door] > 90:
            doors_theta[door] = 90
            change_state_door(door)
        elif doors_theta[door] < 0:
            doors_theta[door] = 0
            change_state_door(door)

    elif doors_theta[door] == 0 or doors_theta[door] == 90:
        doors_direction_of_movement[door] *= -1
        doors_theta[door] += doors_direction_of_movement[door] * 0.00001

def main():
    global display

    is_paused = False
    is_set_to_close = False
    mouse_pos = [0, 0]

    load_mesh("iphan_v8.obj")

    init()

    while not is_set_to_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_set_to_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_set_to_close = True
                elif event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    is_paused = not is_paused
                    pygame.mouse.set_pos(display_center)
                elif event.key == pygame.K_1:
                    change_state_door(Door.center.value)
                elif event.key == pygame.K_2:
                    change_state_door(Door.left.value)
                elif event.key == pygame.K_3:
                    change_state_door(Door.right.value)
                elif event.key == pygame.K_4:
                    change_state_door(Door.window.value)
                else:
                    visibility_update(pygame.key.get_pressed())

            if not is_paused:
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = [event.pos[i] - display_center[i] for i in \
                        range(2)]
                pygame.mouse.set_pos(display_center)

        if not is_paused:
            keypress = pygame.key.get_pressed()

            view_update(mouse_pos, keypress)

            for door in Door:
                if doors_state[door.value]:
                    open_door(door.value)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            tracer.draw_objects(objects_not_to_be_drawn, doors_theta)
            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(DELAY)

    pygame.quit()

if __name__ == "__main__":
    main()
