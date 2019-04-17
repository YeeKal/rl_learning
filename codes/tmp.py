from math import sin, cos, sqrt,pi
import pyglet
from pyglet.gl import *
import time

box_id=0
cout=0
left_p=[0,0]

# window = pyglet.window.Window(482,482)
# pyglet.resource.path = ['resources']
# pyglet.resource.reindex()


# def update(dt):
#     global cout,box_id
#     cout =cout+1
#     if cout%50==0:
#         cout=0
#         box_id +=1
#         if box_id>8:
#             box_id=0

#     left_p[0] +=5*dt
#     left_p[1] +=5*dt
#     if left_p[0]>window.width:
#         left_p[0]=0
#     if left_p[1]>window.height:
#         left_p[1]=0
#     pass


# @window.event
# def on_draw():
#     time.sleep(0.01)
#    # glClear(GL_COLOR_BUFFER_BIT)
#     window.clear()
#     # window.switch_to()
#     # window.dispatch_events()
#     glClearColor(255, 255, 255, 0.0)
#     glLoadIdentity()
#     #box
#     glColor4f(0.0, 0.8, 0.2,0.5)
#     id_yu3=box_id%3
#     id_sh3=box_id//3
#     glRectf(id_yu3*window.width//3,(3-id_sh3)*window.height//3,(id_yu3+1)*window.width//3,(2-id_sh3)*window.height//3) 

#     #lines
#     glColor4f(0.8, 0.2, 0.2, 0.0)
#     glBegin(GL_LINES)
#     glVertex2f(0, window.height*2//3)
#     glVertex2f(window.width,window.height*2//3)
#     glVertex2f(0, window.height//3)
#     glVertex2f(window.width,window.height//3)
#     glVertex2f(window.width//3,0)
#     glVertex2f(window.width//3,window.height)
#     glVertex2f(window.width*2//3,0)
#     glVertex2f(window.width*2//3,window.height)
#     glEnd()
#     #window.flip()
#    # window.dispatch_events()

# #@window.event
# def on_resize(width, height):
#     glViewport(0, 0, width, height)
#     glMatrixMode(gl.GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0, width, 0, height, -1, 1)
#     glMatrixMode(gl.GL_MODELVIEW)

#pyglet.app.event_loop.clock.schedule(update)
#pyglet.app.run()
# while True:
#     tx=input("command:")
#     if tx=='c':
#         on_draw()
#     elif tx=='q':
#         break

class FrozenLake(pyglet.window.Window):
    def __init__(self,width,height,column,row):
        super(FrozenLake,self).__init__(width, height, fullscreen = False)
        self.row=row
        self.column=column
        self.render(0)
        self.obstacles=[5,7]
        
    def setObstacles(self,obstacles):
        self.obstacles=obstacles

    def onDraw(self):
        self.clear()
        # glClear(GL_COLOR_BUFFER_BIT)
 
        glClearColor(255, 255, 255, 0.0)
        glLoadIdentity()
        #box
        glColor4f(0.0, 0.8, 0.2,0.5)
        id_yu3=self.box_id%self.column
        id_sh3=self.box_id//self.column
        glRectf(id_yu3*self.width//self.column,(self.row-id_sh3)*self.height//self.row,(id_yu3+1)*self.width//self.column,(self.row-1-id_sh3)*self.height//self.row) 
        #lines
        glColor4f(0.8, 0.2, 0.2, 0.0)
        glBegin(GL_LINES)
        #plot row
        for i in range(1,self.row):
            glVertex2f(0, self.height*i//self.row)
            glVertex2f(self.width,self.height*i//self.row)
        for i in range(1,self.column):
            glVertex2f(self.width*i//self.column,0)
            glVertex2f(self.width*i//self.column,self.height)
        glEnd()

        #obstacles
        glColor4f(0.1, 0.1, 0.1, 0.0)
        
        n=1000
        for o in [5,7]:
            glBegin(GL_POLYGON)
            r_yu3=o%self.column
            r_sh3=o//self.column
            r_x=(2*r_yu3+1)*self.width//self.column/2
            r_y=(2*self.row-1-2*r_sh3)*self.height//self.row/2
            R=min(self.width//self.column,self.height//self.row)/4
            for i in range(n):
                glVertex2f(R*cos(2*pi*i/n)+r_x,R*sin(2*pi*i/n)+r_y)
            glEnd()
        
        #start target
        self.flip()
    def render(self,box_id):
        if box_id>=0 and box_id<self.row*self.column:
            self.box_id=box_id
        else:
            self.box_id=0
        self.onDraw()
        event = self.dispatch_events()

lake=FrozenLake(643,643,4,4)
 
while True:
    tx=input("command:")
    if tx=='c':
        lake.render(box_id)
    elif tx=='q':
        break
    box_id +=1
    if box_id>15:
        box_id=0
    
