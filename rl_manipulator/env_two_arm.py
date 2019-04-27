import pyglet
import numpy as np
from math import cos,sin,pi,sqrt
import time

bw=10        #bar width

## display link chain 
"""
obstacle will be viewed as a plane
"""
class Viewer(pyglet.window.Window):
    def __init__(self,window_info,arm_length,target,obstacle):
        super(Viewer,self).__init__(window_info[0], window_info[1],
                        resizable=False, caption='Arm', 
                        vsync=False,fullscreen = False)
                    
        #joint values
        self.al=arm_length          #arm length array:[l1,l2]
        self.ob=target               #target info
        self.oc=[50,50,50,100,100,100,100,50] #target current points
        self.ob_info=obstacle
        self.ob_p=self.oc
        self.theta=np.zeros(len(self.al))
        self.center=np.array([self.width//2,self.height//2])
        self.armsp=self.iniArmPs()      #initial arm points in self coordinate
        self.armsc=self.iniArmPs()      #current arm points
        

        pyglet.gl.glClearColor(1,1,1,1)
        self.batch=pyglet.graphics.Batch() #display as batch
        #target
        self.target=self.batch.add(
            4,pyglet.gl.GL_QUADS,None,
            ('v2f',self.oc),
            ('c3B',(86,109,249)*4)
        )
        self.obstacle=self.batch.add(
            4,pyglet.gl.GL_QUADS,None,
            ('v2f',self.ob_p),
            ('c3B',(0,0,0)*4)
        )
        self.arms=[]                    #opengl arms
        for i in range(len(self.al)):
            arm=self.batch.add(
                4,pyglet.gl.GL_QUADS,None,
                ('v2f',self.armsc[i]),
                ('c3B',(249, 86, 86)*4)
            )
            self.arms.append(arm)
        self.upadteJnvs(self.theta)
        self.render()
        
    def settarget(self,target):
        self.target=target

    def on_draw(self):
        self.clear()
        self.batch.draw()
    #jnv:joint values array [jnv1,jnv2]
    def render(self):
        for i in range(len(self.al)):
            self.arms[i].vertices=self.armsc[i]
        self.target.vertices=self.oc
        self.obstacle.vertices=self.ob_p
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
    def upadteJnvs(self,jnvs):
        #update arms
        assert len(jnvs)==len(self.al)
        self.theta=jnvs
        bias=self.center
        
        for i in range(len(self.al)):
            rot=self.rotation2D(np.sum(jnvs[:i+1]))
            p0=np.dot(rot,self.armsp[i][0:2])+bias
            p1=np.dot(rot,self.armsp[i][2:4])+bias
            p2=np.dot(rot,self.armsp[i][4:6])+bias
            p3=np.dot(rot,self.armsp[i][6:8])+bias
            self.armsc[i]=np.concatenate((p0,p1,p2,p3))
            bias=(p1+p2)/2
        #update target
    def updatetarget(self,ta_xy,ob_xy):
        self.ob['x'] =ta_xy[0]
        self.ob['y'] =ta_xy[1]
        self.ob_info['x'] =ob_xy[0]
        self.ob_info['y'] =ob_xy[1]
        p0=[self.ob['x']-self.ob['l']/2,self.ob['y']+self.ob['l']/2]
        p1=[self.ob['x']+self.ob['l']/2,self.ob['y']+self.ob['l']/2]
        p2=[self.ob['x']+self.ob['l']/2,self.ob['y']-self.ob['l']/2]
        p3=[self.ob['x']-self.ob['l']/2,self.ob['y']-self.ob['l']/2]
        self.oc=np.concatenate((p0,p1,p2,p3))

        p0=[self.ob_info['x']-self.ob_info['l']/2,self.ob_info['y']+self.ob_info['l']/2]
        p1=[self.ob_info['x']+self.ob_info['l']/2,self.ob_info['y']+self.ob_info['l']/2]
        p2=[self.ob_info['x']+self.ob_info['l']/2,self.ob_info['y']-self.ob_info['l']/2]
        p3=[self.ob_info['x']-self.ob_info['l']/2,self.ob_info['y']-self.ob_info['l']/2]
        self.ob_p=np.concatenate((p0,p1,p2,p3))
    

    def rotation2D(self,angle):
        return np.array([[cos(angle),-sin(angle)],[sin(angle),cos(angle)]])

    #initialize all arm points in home
    ###     0----1
    ###     3----2
    def iniArmPs(self):
        armsp=[]
        for i in range(len(self.al)):
            p0=[0,bw/2]
            p1=[self.al[i],bw/2]
            p2=[self.al[i],-bw/2]
            p3=[0,-bw/2]
            arm=np.array(p0+p1+p2+p3)
            armsp.append(arm)
        
        p0=[self.ob['x']-self.ob['l']/2,self.ob['y']+self.ob['l']/2]
        p1=[self.ob['x']+self.ob['l']/2,self.ob['y']+self.ob['l']/2]
        p2=[self.ob['x']+self.ob['l']/2,self.ob['y']-self.ob['l']/2]
        p3=[self.ob['x']-self.ob['l']/2,self.ob['y']-self.ob['l']/2]
        self.oc=np.concatenate((p0,p1,p2,p3))

        p0=[self.ob_info['x']-self.ob_info['l']/2,self.ob_info['y']+self.ob_info['l']/2]
        p1=[self.ob_info['x']+self.ob_info['l']/2,self.ob_info['y']+self.ob_info['l']/2]
        p2=[self.ob_info['x']+self.ob_info['l']/2,self.ob_info['y']-self.ob_info['l']/2]
        p3=[self.ob_info['x']-self.ob_info['l']/2,self.ob_info['y']-self.ob_info['l']/2]
        self.ob_p=np.concatenate((p0,p1,p2,p3))
        return armsp
    
    ##middle point of p2/p3 in the target
    def reachGoal(self):
        p0=self.armsc[-1][0:2]
        p1=self.armsc[-1][2:4]
        p2=self.armsc[-1][4:6]
        p3=self.armsc[-1][6:8]
        e1=p0+p3/2
        e2=(p1+p2)/2
        d1=[(self.ob['x']-e1[0])/self.width,(self.ob['y']-e1[1])/self.height]
        d2=[(self.ob['x']-e2[0])/self.width,(self.ob['y']-e2[1])/self.height]
        delta_x=abs(d2[0]*self.width)
        delta_y=abs(d2[1]*self.height)
        dist=np.sqrt(d2[0]**2+d2[1]**2)
        h=self.ob['l']/2
        if delta_x<h and delta_y<h:
            return True,dist,e1/self.width*2,e2/self.width*2,d1+d2    
        return False,dist,e1/self.width*2,e2/self.width*2,d1+d2
    def reachObstacle(self):
        """
        @return: [d1,d2,...]
        """
        d=[]
        for i in range(len(self.al)):
            rot=self.rotation2D(-np.sum(self.theta[:i+1]))
            armc=np.array(self.armsc[i]).copy()
            armc[:2]=np.dot(rot,armc[:2])
            armc[4:6]=np.dot(rot,armc[4:6])
            point=[self.ob_info['x'],self.ob_info['y']]
            point=np.dot(rot,point)

            d.append(self.point2Rec(armc,point))
        return d
        pass
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        ta_x=abs(x-self.ob['x'])
        ta_y=abs(y-self.ob['y'])
        ob_x=abs(x-self.ob_info['x'])
        ob_y=abs(y-self.ob_info['y'])
        h=self.ob['l']/2
        if ta_x<h and ta_y<h:
            self.updatetarget([self.ob['x']+dx,self.ob['y']+dy],[self.ob_info['x'],self.ob_info['y']])
        elif ob_x<h and ob_y<h:
            self.updatetarget([self.ob['x'],self.ob['y']],[self.ob_info['x']+dx,self.ob_info['y']+dy])

        pass
    def point2Rec(self,rect,p):
        """
        @desp: calculate the nearest distance from a point to rectangular
            dx = Math.max(rect.min.x - p.x, 0, p.x - rect.max.x);
            dy = Math.max(rect.min.y - p.y, 0, p.y - rect.max.y);
            d = Math.sqrt(dx*dx + dy*dy);
        """
        dx=np.max([
                np.min([rect[0],rect[4]])-p[0],
                0,
                p[0]-np.max([rect[0],rect[4]])])
        dy=np.max([
            np.min([rect[1],rect[5]])-p[1],
            0,
            p[1]-np.max([rect[1],rect[5]])])
        return np.sqrt(dx**2+dy**2)

class TwoArms(object):
    def __init__(self):
        self.state_dim=9+2
        self.action_dim=2
        self.action_bound=[-1,1]    #joint angle range
        self.dt=0.1                 #minimua step
        self.target = {'x': 100., 'y': 100., 'l': 40}
        self.obstacle={'x':300,'y':300,'l':20}
        self.window=[400,400]
        self.arms=[100,100]
        self.theta=np.array([0.0,0.0])        #initial
        self.viewer=Viewer(self.window,self.arms,self.target,self.obstacle)
        self.on_goal=0

    def reset(self):
        self.updateTO()
        
        
        self.on_goal=0
        self.theta=2*np.pi*np.random.rand(2)
        self.viewer.theta=self.theta
        self.viewer.upadteJnvs(self.theta)
        reach,dist,e1,e2,d=self.viewer.reachGoal()
        d2o=self.viewer.reachObstacle()
        
        self.state=np.concatenate((e1,e2,d,np.dot(d2o,2/np.linalg.norm(self.window)),[1.0 if reach else 0.0]))
        return self.state
    def sample_action(self):
        return np.random.rand(2)-0.5

    def step(self,action):
        done=False
        r=0
        action=self.dt*np.clip(action,*self.action_bound)

        self.theta=self.theta+action
        self.theta %=np.pi*2  #normalize
        self.viewer.upadteJnvs(self.theta)
        reach,dist,e1,e2,d=self.viewer.reachGoal()
        d2o=self.viewer.reachObstacle()
        r=-dist
        r +=self.obstacleReward(d2o)
        if reach:
            r +=1
            #if reach, extra action will be punishment
            # if self.on_goal>0:
            #     r+=-np.linalg.norm(action)
            self.on_goal+=1
            if self.on_goal>50:
                done=True
        else:
            self.on_goal=0
        self.state=np.concatenate((e1,e2,d,np.dot(d2o,2/np.linalg.norm(self.window)),[1.0 if reach else 0.0]))

        return self.state,r,done

    def render(self):
        self.viewer.render()
    def updateTO(self):
        tx=np.random.randint(self.window[0])
        ty=np.random.randint(self.window[1])
        ox=np.random.randint(self.window[0])
        oy=np.random.randint(self.window[1])

        while np.sqrt((tx-ox)**2+(ty-oy)**2) < self.target['l']+self.obstacle['l'] or np.sqrt((ox-self.window[0]//2)**2+(oy-self.window[1]//2)**2)<self.obstacle['l']:
            tx=np.random.randint(self.window[0])
            ty=np.random.randint(self.window[1])
            ox=np.random.randint(self.window[0])
            oy=np.random.randint(self.window[1])
        self.viewer.updatetarget([tx,ty],[ox,oy])
    def obstacleReward(self,d2o):
        r=self.obstacle['l']/2
        reward=0
        for i in range(len(d2o)):
            if d2o[i]<r:
                reward +=-0.5
            elif d2o[i]<2*r:
                reward +=((d2o[i]-r)**2-r**2)/(2*r**2)
        return reward

if __name__=='__main__':
    env=TwoArms()
    env.reset()
    while True:
        env.render()
        s,r,d=env.step(env.sample_action())
        time.sleep(0.2)

