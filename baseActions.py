import action
            
class Move(action.Action):
    def __init__(self,length):
        action.Action.__init__(self,length)
        self.direction = -1
        
    def setUp(self,actor):
        self.direction = actor.getForwardWithOffset(0)
        
    def update(self, actor):
        actor.setSpeed(actor.var['maxGroundSpeed'],self.direction)
        
        self.frame += 1
        if self.frame > self.lastFrame: self.frame = 0
        
    def stateTransitions(self,actor):
        moveState(actor,self.direction)
        
class Run(action.Action):
    def __init__(self,length):
        action.Action.__init__(self,length)
        
    def update(self, actor):
        if actor.facing == 1: direction = 0
        else: direction = 180
        actor.setSpeed(actor.var['maxGroundSpeed']*1.5,direction, False)
        
        self.frame += 1
        if self.frame > self.lastFrame: self.frame = 0
        
class Pivot(action.Action):
    def __init__(self,length):
        action.Action.__init__(self, length)
        
    def update(self,actor):
        if self.frame != self.lastFrame:
            self.frame += 1
            actor.preferred_xspeed = 0
            
class Stop(action.Action):
    def __init__(self,length):
        action.Action.__init__(self, length)
        
    def update(self, actor):
        actor.preferred_xspeed = 0
        self.frame += 1
        
    def stateTransitions(self, actor):
        (_,invkey) = actor.getForwardBackwardKeys()
        if actor.bufferContains(invkey,5,notReleased = True):
            actor.doPivot()
                
class NeutralAction(action.Action):
    def __init__(self,length):
        action.Action.__init__(self, length)

        
    def update(self, actor):
        return
    
    def stateTransitions(self, actor):
        neutralState(actor)
        
class HitStun(action.Action):
    def __init__(self,hitstun,direction):
        action.Action.__init__(self, hitstun)
        self.direction = direction
    
    def update(self,actor):
        if self.frame == 0:
            actor.grounded = False
            actor.rotateSprite(self.direction)
            actor.preferred_xspeed = 0
            
        if self.frame == self.lastFrame:
            actor.unRotate()
            
        self.frame += 1

class Jump(action.Action):
    def __init__(self,length,jumpFrame):
        action.Action.__init__(self, length)
        self.jumpFrame = jumpFrame
        
    def update(self,actor):
        if self.frame == self.jumpFrame:
            actor.grounded = False
            actor.change_y = -actor.var['jumpHeight']
            if actor.change_x > actor.var['maxAirSpeed']:
                actor.change_x = actor.var['maxAirSpeed']
            elif actor.change_x < -actor.var['maxAirSpeed']:
                actor.change_x = -actor.var['maxAirSpeed']
            
        self.frame += 1
        
class AirJump(action.Action):
    def __init__(self,length,jumpFrame):
        action.Action.__init__(self, length)
        self.jumpFrame = jumpFrame
        
    def update(self,actor):
        if self.frame == 0:
            actor.jumps -= 1
        
        if self.frame < self.jumpFrame:
            actor.change_y = 0
        if self.frame == self.jumpFrame:
            actor.grounded = False
            actor.change_y = -actor.var['airJumpHeight']
            
            if actor.keysContain(actor.keyBindings.k_left):
                if actor.facing == 1:
                    actor.flip()
                    actor.change_x = actor.facing * actor.var['maxAirSpeed']
            elif actor.keysContain(actor.keyBindings.k_right):
                if actor.facing == -1:
                    actor.flip()
                    actor.change_x = actor.facing * actor.var['maxAirSpeed']    
        self.frame += 1
        
class Fall(action.Action):
    def __init__(self):
        action.Action.__init__(self, 1)

    
    def stateTransitions(self,actor):
        airState(actor)
        
    def update(self,actor):
        actor.grounded = False
            
class Land(action.Action):
    def __init__(self):
        action.Action.__init__(self, 6)

        
    def update(self,actor):
        if self.frame == 0:
            self.lastFrame = actor.landingLag
            if actor.bufferContains(actor.keyBindings.k_shield,distanceBack=22):
                print "l-cancel"
                self.lastFrame = self.lastFrame / 2    
        if self.frame == self.lastFrame:
            actor.landingLag = 6
            if   actor.keysHeld.count(actor.keyBindings.k_left): actor.doGroundMove(180)
            elif actor.keysHeld.count(actor.keyBindings.k_right): actor.doGroundMove(0)
            else: actor.doIdle()
        actor.preferred_xspeed = 0
        self.frame+= 1

########################################################
#               TRANSITION STATES                     #
########################################################
def neutralState(actor):
    if actor.bufferContains(actor.keyBindings.k_attack):
        actor.doGroundAttack()
    if actor.bufferContains(actor.keyBindings.k_up,10):
        actor.doJump()
    if actor.bufferContains(actor.keyBindings.k_left,8):
        actor.doGroundMove(180)
    elif actor.bufferContains(actor.keyBindings.k_right,8):
        actor.doGroundMove(0)
    

def airState(actor):
    airControl(actor)
    if actor.bufferContains(actor.keyBindings.k_up):
        actor.doJump()
    if actor.bufferContains(actor.keyBindings.k_down):
        if actor.change_y >= 0:
            actor.change_y = actor.var['maxFallSpeed']
            actor.landingLag = 14
            
def moveState(actor, direction):
    if actor.bufferContains(actor.keyBindings.k_up):
        actor.doJump()
    (key,_) = actor.getForwardBackwardKeys()
    if actor.bufferContains(key, state=False):
        actor.doStop()
    if actor.bufferContains(actor.keyBindings.k_attack):
        print "attacking"
        actor.doGroundAttack()
            

########################################################
#             BEGIN HELPER METHODS                     #
########################################################

def airControl(actor):
    if actor.keysHeld.count(actor.keyBindings.k_left):
        actor.preferred_xspeed = -actor.var['maxAirSpeed']
    elif actor.keysHeld.count(actor.keyBindings.k_right):
        actor.preferred_xspeed = actor.var['maxAirSpeed']
    
    if (actor.change_x < 0) and not actor.keysHeld.count(actor.keyBindings.k_left):
        actor.preferred_xspeed = 0
    elif (actor.change_x > 0) and not actor.keysHeld.count(actor.keyBindings.k_right):
        actor.preferred_xspeed = 0
        
    actor.checkForGround()
    if actor.grounded:
        actor.doLand()