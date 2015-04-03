import action
import baseActions
import hitbox

class NeutralAttack(action.Action):
    def __init__(self):
        action.Action.__init__(self,18)
        self.rapidJabbing = True
        self.nextJab = False
        self.jab1Hitbox = None
        
    def update(self, actor):
        actor.change_x = 0
        if (self.rapidJabbing and actor.keysHeld.count(actor.keyBindings.k_attack) == 0):
            self.rapidJabbing = False
                    
        if (self.frame % 3 == 0):
            actor.changeSprite("jab1_",0)
            actor.changeSpriteImage(self.frame/3)  
        if (self.frame == 3):
            if actor.facing == 1:
                self.jab1Hitbox = hitbox.DamageHitbox([47,37],[27,25],actor,5,1,0,90)
            else:
                self.jab1Hitbox = hitbox.DamageHitbox([-20,37],[27,25],actor,5,1,0,90)    
            self.hitboxes.add(self.jab1Hitbox)
            actor.gameState.active_hitboxes.add(self.jab1Hitbox)
        if self.frame > 3 and self.frame < 9:
            self.jab1Hitbox.update()
        if (self.frame == 9):
            self.jab1Hitbox.kill()
            self.jab1Hitbox = None    
        self.frame += 1
        if self.frame == self.lastFrame:
            if self.nextJab: actor.current_action = NeutralAttack2()
            elif self.rapidJabbing: actor.current_action = NeutralAttack()
            else: actor.current_action = NeutralAction()
            
class NeutralAttack2(action.Action):
    def __init__(self):
        action.Action.__init__(self, 12)
        self.nextJab = False
        self.jab2Hitbox = None
        
    def update(self,actor):
        if (self.frame % 3 == 0):
            actor.sprite.imageText = "jab2_"
            actor.changeSpriteImage(self.frame/3)
        if (self.frame == 3):
            if actor.facing == 1:
                self.jab2Hitbox = hitbox.DamageHitbox([53,31],[42,22],actor,5,1,0,90)
            else:
                self.jab2Hitbox = hitbox.DamageHitbox([-25,31],[42,22],actor,5,1,0,90)    
            self.hitboxes.add(self.jab2Hitbox)
            actor.gameState.active_hitboxes.add(self.jab2Hitbox)
        if (self.frame > 3 and self.frame < 9):
            self.jab2Hitbox.update()
        if (self.frame == 9):
            self.jab2Hitbox.kill()       
            self.jab2Hitbox = None
        
        self.frame += 1
        if self.frame == self.lastFrame:
            if self.nextJab: actor.current_action = NeutralAttack3()
            else: actor.current_action = NeutralAction()
            
        
class NeutralAttack3(action.Action):
    def __init__(self):
        action.Action.__init__(self, 21)
        self.jab3Hitbox = None
        
    def update(self,actor):
        if (self.frame < 3):
            actor.change_y = -4
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(0)
        elif (self.frame < 6):
            if self.frame % 3 == 0:
                actor.sprite.imageText = "jab3_"
                actor.changeSpriteImage(1)
        
        elif self.frame == 6:
            if actor.facing == 1:
                self.jab3Hitbox = hitbox.DamageHitbox([47,37],[43,52],actor,5,1,0.5,120)
            else:
                self.jab3Hitbox = hitbox.DamageHitbox([-20,37],[43,52],actor,5,1,0.5,120)    
            self.hitboxes.add(self.jab3Hitbox)
            actor.gameState.active_hitboxes.add(self.jab3Hitbox)
            
        elif self.frame >= 6 and self.frame < 15:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(2)
            self.jab3Hitbox.update()
        elif self.frame == 15:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(3)
            self.jab3Hitbox.kill()
            self.jab3Hitbox = None       
        elif self.frame == 18:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(4)
            
        self.frame += 1
        if self.frame == self.lastFrame:
            actor.current_action = NeutralAction()
            
class NeutralAir(action.Action):
    def __init__(self):
        action.Action.__init__(self, 42)
        self.neutralAirHitbox = None
        
    def update(self,actor):
        actor.landingLag = 16
        
        if (actor.grounded):
            actor.current_action = Land()
            
        if (self.frame < 3):
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(0)
        elif (self.frame < 6):
            if self.frame % 3 == 0:
                actor.sprite.imageText = "jab3_"
                actor.changeSpriteImage(1)
        
        elif self.frame == 6:
            if actor.facing == 1:
                self.neutralAirHitbox = hitbox.DamageHitbox([42,37],[43,52],actor,5,10,0.5,60)
            else:
                self.neutralAirHitbox = hitbox.DamageHitbox([-24,37],[43,52],actor,5,10,0.5,120)    
            self.hitboxes.add(self.neutralAirHitbox)
            actor.gameState.active_hitboxes.add(self.neutralAirHitbox)
        elif self.frame >= 6 and self.frame < 36:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(2)
            self.neutralAirHitbox.update()
            baseActions.airControl(actor)
        elif self.frame == 36:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(3)
            self.neutralAirHitbox.kill()
        elif self.frame == 39:
            actor.sprite.imageText = "jab3_"
            actor.changeSpriteImage(4)
        
        if actor.grounded:
            self.neutralAirHitbox.kill()    
        self.frame += 1
        if self.frame == self.lastFrame:
            self.neutralAirHitbox.kill()
            actor.current_action = Fall()

class ForwardAttack(action.Action):
    def __init__(self):
        action.Action.__init__(self, 42)
    
    def setUp(self,actor):
        self.fSmashHitbox = hitbox.DamageHitbox([20,0],[60,40],actor,15,5,1.0,20)
            
    def update(self,actor):
        if self.frame == 0:
            actor.change_x = 0
            actor.preferred_xspeed = 0
            actor.changeSprite("hitboxie_fsmash",0)
        elif self.frame == 3:
            actor.changeSpriteImage(1)
        elif self.frame == 6:
            actor.changeSpriteImage(2)
        elif self.frame == 9:
            actor.changeSpriteImage(3)
        elif self.frame == 12:
            actor.changeSpriteImage(4)
        elif self.frame == 15:
            actor.changeSpriteImage(5)
        elif self.frame == 18:
            actor.changeSpriteImage(6)
        elif self.frame == 21:
            actor.changeSpriteImage(7)
            self.hitboxes.add(self.fSmashHitbox)
        elif self.frame == 36:
            actor.changeSpriteImage(8)
            self.fSmashHitbox.kill()
        elif self.frame == 39:
            actor.changeSpriteImage(9)
        elif self.frame == self.lastFrame:
            actor.doIdle()
        
        self.frame += 1
        
        def stateTransitions(self,actor):
            if self.frame > 36:
                baseActions.neutralState(actor)    
                
########################################################
#            BEGIN OVERRIDE CLASSES                    #
########################################################

class Move(baseActions.Move):
    def __init__(self,accel = True):
        baseActions.Move.__init__(self,15)
        self.accel = accel
        
    def update(self, actor):
        if self.accel:
            if (self.frame == 0):
                actor.changeSprite("hitboxie_run",0)
            elif (self.frame == 3):
                actor.changeSpriteImage(1)
            elif (self.frame == 6):
                actor.changeSpriteImage(2)
            elif (self.frame == 9):
                actor.changeSpriteImage(3)
            elif (self.frame == 12):
                actor.changeSpriteImage(4)
        else:
            if (self.frame == 0):
                actor.changeSprite("hitboxie_run",4)
                
        if actor.grounded == False:
            actor.current_action = Fall()
        baseActions.Move.update(self, actor)
        if (self.frame == self.lastFrame):
            self.frame = 12
        
class Run(baseActions.Run):
    def __init__(self,accel = True):
        baseActions.Run.__init__(self,15)
        self.accel = accel
        
    def update(self, actor):
        if self.accel:
            if (self.frame == 0):
                actor.changeSprite("hitboxie_run",0)
            elif (self.frame == 3):
                actor.changeSpriteImage(1)
            elif (self.frame == 6):
                actor.changeSpriteImage(2)
            elif (self.frame == 9):
                actor.changeSpriteImage(3)
            elif (self.frame == 12):
                actor.changeSpriteImage(4)
        else:
            if (self.frame == 0):
                actor.changeSprite("hitboxie_run",4)
                
        if actor.grounded == False:
            actor.current_action = Fall()
        baseActions.Run.update(self, actor)
        if (self.frame == self.lastFrame):
            self.frame = 12
                   
class Pivot(baseActions.Pivot):
    def __init__(self):
        baseActions.Pivot.__init__(self,10)
        
    def update(self,actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_pivot",4)
        elif self.frame == 2:
            actor.changeSpriteImage(3)
        elif self.frame == 4:
            actor.changeSpriteImage(2)
        elif self.frame == 6:
            actor.changeSpriteImage(1)
        elif self.frame == 8:
            actor.changeSpriteImage(0)
        elif self.frame == self.lastFrame:
            actor.changeAction(Move(False))
        baseActions.Pivot.update(self, actor)
        
class NeutralAction(baseActions.NeutralAction):
    def __init__(self):
        baseActions.NeutralAction.__init__(self,1)
        
    def update(self, actor):
        actor.changeSprite("hitboxie_idle")
        if actor.grounded == False: actor.current_action = Fall()
        
class Stop(baseActions.Stop):
    def __init__(self):
        baseActions.Stop.__init__(self, 9)
    
    def update(self, actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_pivot",0)
        elif self.frame == 3:
            actor.changeSpriteImage(1)
        elif self.frame == 6:
            actor.changeSpriteImage(2)
        elif self.frame == self.lastFrame:
            if actor.inputBuffer.contains(actor.keyBindings.k_up,5):
                actor.current_action = Jump()
            else: actor.current_action = NeutralAction()
        if actor.grounded == False: actor.current_action = Fall()
        baseActions.Stop.update(self, actor)
        
class HitStun(baseActions.HitStun):
    def __init__(self,hitstun,direction):
        baseActions.HitStun.__init__(self, hitstun, direction)
        
    def update(self,actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_fall")
            
        if self.frame == self.lastFrame:
            actor.current_action = Fall()
        baseActions.HitStun.update(self, actor)
             
class Jump(baseActions.Jump):
    def __init__(self):
        baseActions.Jump.__init__(self,9,8)
        
    def update(self,actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_land",0)
        elif self.frame == 2:
            actor.changeSpriteImage(1)
        elif self.frame == 4:
            actor.changeSpriteImage(2)
        elif self.frame == 6:
            actor.changeSpriteImage(3)
        elif self.frame == 8:
            actor.changeSprite("hitboxie_jump")
        elif self.frame == self.lastFrame:
            actor.current_action = Fall()
        baseActions.Jump.update(self, actor)
        

class AirJump(baseActions.AirJump):
    def __init__(self):
        baseActions.AirJump.__init__(self,10,4)
        
    def update(self,actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_airjump",0)
        elif self.frame == 2:
            actor.changeSpriteImage(1)
        elif self.frame == 4:
            actor.changeSpriteImage(2)
        elif self.frame == 6:
            actor.changeSpriteImage(3)
        elif self.frame == 8:
            actor.changeSpriteImage(4)
        elif self.frame == self.lastFrame:
            actor.current_action = Fall()
        baseActions.AirJump.update(self, actor)
            
class Fall(baseActions.Fall):
    def __init__(self):
        baseActions.Fall.__init__(self)
        
    def update(self,actor):
        actor.changeSprite("hitboxie_jump")
        baseActions.Fall.update(self, actor)
            
class Land(baseActions.Land):
    def __init__(self):
        baseActions.Land.__init__(self)
        
    def update(self,actor):
        if self.frame == 0:
            actor.changeSprite("hitboxie_land",0)
        else:
            if self.frame < 12:
                if self.frame % 3 == 0:
                    actor.changeSpriteImage(self.frame / 3)
        
        baseActions.Land.update(self, actor)
            
        
        
########################################################
#             BEGIN HELPER METHODS                     #
########################################################