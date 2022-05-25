import math
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tracer import Tracer

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
STEP_DISTANCE = 0.2
STEP_THETA = 0.2

objects_not_to_be_drawn = []

tracer = None

display_dim = (WINDOW_WIDTH, WINDOW_HEIGHT)
display_center = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
display = None

camera_x, camera_y, camera_z = 0, 0, 0
theta_vertical = 0
theta_horizontal = 0

view_matrix = []

def init():
    global tracer
    global display
    global view_matrix

    tracer = Tracer()
    tracer.load_mesh_from_file("iphan_v5.obj")

    pygame.init()
    display = pygame.display.set_mode(display_dim, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Modelagem IPHAN')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (WINDOW_WIDTH/WINDOW_HEIGHT), 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(camera_x, 15, camera_z, 0, 0, 0, 0, 0, 1)
    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    pygame.mouse.set_pos(display_center)

def move_camera_with_keypress(keypress):
    global camera_x, camera_y, camera_z

    if keypress[pygame.K_w]:
        camera_z += STEP_DISTANCE
        glTranslatef(0, 0, STEP_DISTANCE)
    if keypress[pygame.K_s]:
        camera_z -= STEP_DISTANCE
        glTranslatef(0, 0,-STEP_DISTANCE)
    if keypress[pygame.K_d]:
        camera_x -= STEP_DISTANCE
        glTranslatef(-STEP_DISTANCE, 0, 0)
    if keypress[pygame.K_a]:
        camera_x += STEP_DISTANCE
        glTranslatef(STEP_DISTANCE, 0, 0)
    if keypress[pygame.K_q]:
        camera_y -= STEP_DISTANCE
        glTranslatef(0, -STEP_DISTANCE, 0)
    if keypress[pygame.K_e]:
        camera_y += STEP_DISTANCE
        glTranslatef(0, STEP_DISTANCE ,0)

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

def change_obj_visibility(obj_name):
    global objects_not_to_be_drawn

    if obj_name not in objects_not_to_be_drawn:
        objects_not_to_be_drawn.append(obj_name)
    else:
        objects_not_to_be_drawn.remove(obj_name)

def visibility_update(keypress):
    if keypress[pygame.K_c]:
        change_obj_visibility("Ceiling")
    if keypress[pygame.K_f]:
        change_obj_visibility("Ceiling_Frame.001")
        change_obj_visibility("Ceiling_Frame.002")
        change_obj_visibility("Ceiling_Frame.003")
        change_obj_visibility("Door_Frame.001")
        change_obj_visibility("Door_Frame.002")
        change_obj_visibility("Door_Frame.003")
    if keypress[pygame.K_b]:
        change_obj_visibility("Room")
    if keypress[pygame.K_u]:
        change_obj_visibility("Stairs_Base")
        change_obj_visibility("Stairs.001")
        change_obj_visibility("Stairs.002")

def main():
    global display

    up_down_angle = 0.0
    is_paused = False
    is_set_to_close = False
    mouse_pos = [0, 0]

    init()

    while not is_set_to_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_set_to_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    is_set_to_close = True
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    is_paused = not is_paused
                    pygame.mouse.set_pos(display_center)
            if not is_paused:
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = [event.pos[i] - display_center[i] for i in \
                        range(2)]
                pygame.mouse.set_pos(display_center)

        if not is_paused:
            keypress = pygame.key.get_pressed()

            visibility_update(keypress)

            view_update(mouse_pos, keypress)

            glLightfv(GL_LIGHT0, GL_POSITION, [-1, -1, -1, 0])

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            tracer.draw_objects(objects_not_to_be_drawn)
            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
