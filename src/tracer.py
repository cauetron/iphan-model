from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from mesh_loader import MeshLoader

import re

def starts_with(string, word):
    regexp = "\A" + word
    return re.search(regexp, string)

class Tracer():
    def __init__(self):
        self.mesh_loader = MeshLoader()

        self.colors = {
        "red": [1, 0, 0, 1],
        "blue": [0, 1, 0, 1],
        "green": [0, 0, 1, 1],
        "yellow": [0, 1, 1, 1],
        "brown": [75/255, 54/255, 33/255, 1],
        "pink": [1, 0, 0, 1],
        "white": [1, 1, 1, 1],
        "light_gray": [0.7, 0.7, 0.7, 1],
        "gray": [0.5, 0.5, 0.5, 1],
        "dark_gray": [0.2, 0.2, 0.2, 1],
        "black": [0, 0, 0, 1]
        }

    def load_mesh_from_file(self, file_name):
        self.mesh_loader.load_from_file(file_name)

    def draw_ground_flor(self, x:float, y:float, z:float, color:list):
        glColor4fv(color)
        glBegin(GL_QUADS)
        glVertex3f(-x, -y, z)
        glVertex3f(x, -y, z)
        glVertex3f(x, y/3, z)
        glVertex3f(-x, y/3, z)
        glEnd()

    def draw_objects(self, list_of_objects:list, doors_theta:list):
        if "Ground_Floor" not in list_of_objects:
            self.draw_ground_flor(15, 45, -0.01, self.colors["dark_gray"])

        for obj in self.mesh_loader.objects:
            if obj.name not in list_of_objects:
                if obj.name == "Floor":
                    glColor4fv(self.colors["gray"])
                    obj.draw()

                elif obj.name == "Room":
                    glColor4fv(self.colors["light_gray"])
                    obj.draw()

                elif obj.name == "Room_Upstairs":
                    glColor4fv(self.colors["light_gray"])
                    obj.draw()

                elif obj.name == "Room_Back_White":
                    glColor4fv(self.colors["light_gray"])
                    obj.draw()

                elif obj.name == "Room_Back_Red":
                    glColor4fv(self.colors["red"])
                    obj.draw()

                elif starts_with(obj.name, "Door_Frame"):
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif obj.name == "Building_Frame":
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif obj.name == "Door_One_Right":
                    #0.013333
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(-0.670, 0, 0)
                    glRotatef(-doors_theta[0], 0, 0, 1)
                    glTranslatef(0.67, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_One_Left":
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(0.67, 0, 0)
                    glRotatef(doors_theta[0], 0, 0, 1)
                    glTranslatef(-0.67, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Two_Right":
                    #0.013333
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(2.946450, 0, 0)
                    glRotatef(-doors_theta[1], 0, 0, 1)
                    glTranslatef(-2.946450, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Two_Left":
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(4.295177, 0, 0)
                    glRotatef(doors_theta[1], 0, 0, 1)
                    glTranslatef(-4.295177, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Three_Right":
                    #0.013333
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(-4.237305, 0, 0)
                    glRotatef(-doors_theta[2], 0, 0, 1)
                    glTranslatef(4.237305, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Three_Left":
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(-2.888578, 0, 0)
                    glRotatef(doors_theta[2], 0, 0, 1)
                    glTranslatef(2.888578, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Window_Frame":
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif obj.name == "Window_Door":
                    glColor4fv(self.colors["yellow"])
                    glPushMatrix()
                    glTranslatef(-0.001326, -0.200821, -4.78602)
                    glRotatef(doors_theta[3], 0, 0, 1)
                    glTranslatef(0.001326, 0.200821, 4.78602)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Bench":
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif starts_with(obj.name, "Art_Display"):
                    glColor4fv(self.colors["white"])
                    obj.draw()

                elif starts_with(obj.name, "Frame"):
                    glColor4fv(self.colors["red"])
                    obj.draw()

                elif starts_with(obj.name, "Column"):
                    glColor4fv(self.colors["blue"])
                    obj.draw()

                elif starts_with(obj.name, "Ceiling_Frame"):
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif starts_with(obj.name, "Stairs"):
                    glColor4fv(self.colors["light_gray"])
                    obj.draw()

                elif obj.name == "Floor":
                    glColor4fv(self.colors["light_gray"])
                    obj.draw()

                elif obj.name == "Ceiling":
                    glColor4fv(self.colors["brown"])
                    obj.draw()
