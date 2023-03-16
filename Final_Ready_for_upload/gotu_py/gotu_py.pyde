add_library('minim')
import os
import time
import math
import random

path = os.getcwd()
player = Minim(this)

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# ------------------------------------------------------------------------------------------------------------------

#Class for ALL THE SPACESHIPS:
class SpaceShip:
    def __init__(self, r, x, y, img, w, h, num_slices):
        self.radius = r
        self.x = x
        self.y = y
        self.img_w = w
        self.img_h = h
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img)
        self.slice = 0
        self.num_slices = num_slices
        self.health = 0
    
    def update(self):
        self.y += self.vy
        self.x += self.vx
    
    def display(self):
        self.update()
        fill(255,0,0)
        noStroke()
        ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
    
    # Function for taking damage
    def take_damage(self, value):
        self.health = self.health - value
    
    # The num argument here is used to adjust the probability of spawning a powerup. Higher num, means lower probability
    def spawn_powerup(self, num):
        chance = random.randint(1,num)
        if chance == 1:
            type = random.randint(1,3) # Use this to randomly determine which powerup to spawn
            if type == 1:
                main_game.powerups.append(HealthPowerUp(self.x, self.y))
            elif type == 2:
                main_game.powerups.append(ShieldPowerUp(self.x, self.y))
            elif type == 3:
                main_game.powerups.append(ROFPowerUp(self.x, self.y))



# ------------------------------------------------------------------------------------------------------------------

#Class for the MAIN PLAYER SHIP:
class HeroShip(SpaceShip):
    def __init__(self, r, x, y, img, w, h, num_slices):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.control_speed = 13 # This is used to adjust the movement speed
        self.key_handler = {"a":False, "d":False, "w":False, "s":False}
        self.rateOfFire = 60 # Used to control how fast our player shoots
        self.health = 100
        self.lives = 3
        self.projectileSpeed = 40
        self.shieldAmount = 70
        self.img_shielded = loadImage(path + "/images/player_ship_shield_spritesheet.png")
        self.shoot_sound = player.loadFile(path + "/sounds/shoot1.mp3")
        self.maxROF = False
    
    def update(self):
        # Adding movement
        self.y += self.vy
        self.x += self.vx
        
        # Input control for movement
        if self.key_handler["a"]:
            self.vx = -self.control_speed
        elif self.key_handler["d"]:
            self.vx = self.control_speed
        else:
            self.vx = 0
        
        if self.key_handler["w"]:
            self.vy = -self.control_speed
        elif self.key_handler["s"]:
            self.vy = self.control_speed
        else:
            self.vy = 0
        
        # Restricting movement to screen bounds
        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
        if self.y - self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
        
        # Use framecount for the ship's animation
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        
        # COMMENT THE FOLLOWING LINES OF CODE TO STOP SHOOTING IF NEEDED FOR TESTING
        # Use framecount to implement rate of fire
        if frameCount % self.rateOfFire == 0:
            self.shoot() # Instantiate projectiles in front of the player ship
            self.shoot_sound.rewind()
            self.shoot_sound.play()
            
            
        #Testing rate of fire increase
        # if main_game.score >= 100:
        #     self.rateOfFire = 20
    
    def display(self):
        self.update() # The following line displays the image with the proper slicing based on the animation
        if self.shieldAmount > 0:
            image(self.img_shielded, self.x - self.radius - 20, self.y - self.radius * 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        else:
            image(self.img, self.x - self.radius - 20, self.y - self.radius * 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        #print(self.x)
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
    
    # Function that instantiates the projectiles
    def shoot(self):
        main_game.playerProjectiles.append(Projectile(5, self.x - 2, self.y - 75, 12, self.projectileSpeed))
    
    def take_damage(self, value):
        if self.shieldAmount > 0:
            self.shieldAmount -= value
        else:
            self.health = self.health - value
            if self.health <= 0 and self.lives > 0:
                self.lives -= 1
                self.health = 100
            elif self.health <= 0 and self.lives == 0:
                main_game.gameLost = True
        
        
    
# ------------------------------------------------------------------------------------------------------------------
#Class for the ENEMY SHIPS:
class Pawn(SpaceShip):
    def __init__(self, x, y, r = 25, img = "pawn.png", w = 62, h = 90, num_slices = 4):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.vy = 0.5
        self.health = 10
        self.scoreAmount = 10
        self.projectileSpeed = 7
        
    def update(self):
        
        self.y += self.vy
        if self.y > 300:
            self.vy = 1.5
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        if frameCount % 60 == 0:
            chance = random.randint(0,4)
            if chance == 1:
                self.shoot()
    
    def shoot(self):
        main_game.enemyProjectiles.append(Projectile(5, self.x, self.y + 25, 6, self.projectileSpeed, True))
        
    def display(self):
        self.update()
        image(self.img, self.x - self.radius - 5, self.y - 65, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        fill(255,30,30)
        rect(self.x - 25, self.y - 37, 56 * self.health/10, 4)
        if self.health <= 0:
            main_game.score += self.scoreAmount
            self.spawn_powerup(9)
        
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
        # The following will increment the game score if health goes down to 0, aka, the ship dies
  
# ------------------------------------------------------------------------------------------------------------------    
        
class Knight(SpaceShip):
    def __init__(self, x, y, r = 50, img = "knight.png", w = 131, h = 170, num_slices = 4):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.vy = 0.5
        self.vx = 10
        self.health = 40
        self.scoreAmount = 100
        self.projectileSpeed = 6
        
    def update(self):
        
        self.y += self.vy
        self.x += self.vx
        
        if self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
        
        if self.x - self.radius < 0:
            self.vx = -self.vx
            
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        if frameCount % 60 == 0:
            chance = random.randint(0,1)
            if chance == 1:
                self.shoot()
                

    
    def shoot(self):
        main_game.enemyProjectiles.append(Projectile(5, self.x + 50, self.y + 50, 6, self.projectileSpeed, True))
        main_game.enemyProjectiles.append(Projectile(5, self.x - 50, self.y + 50, 6, self.projectileSpeed, True))
        
    def display(self):
        self.update()
        image(self.img, self.x - 65, self.y - 110, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        fill(255,30,30)
        rect(self.x - 30, self.y - 55, 58 * self.health/40, 4)
        
        if self.health <= 0:
            main_game.score += self.scoreAmount
            self.spawn_powerup(6)
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
        
        

# ------------------------------------------------------------------------------------------------------------------

class Bishop(SpaceShip):
    def __init__(self, x, y, r = 36, img = "bishop.png", w = 93, h = 131, num_slices = 4):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.vy = 0.9
        self.vx = 6
        self.health = 20
        self.scoreAmount = 50
        self.projectileSpeed = 7
        self.initialX = self.x
    
    def update(self):
        
        self.y += self.vy
        self.x += self.vx
        if self.y > 500:
            self.vy = 3
        
        if self.x > self.initialX + 85:
            self.vx = -self.vx
        
        if self.x < self.initialX - 85:
            self.vx = -self.vx
            
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        if frameCount % 60 == 0:
            chance = random.randint(1,2)
            if chance == 1:
                self.shoot()
    
    def shoot(self):
        main_game.enemyProjectiles.append(Projectile(5, self.x, self.y - 20, 6, self.projectileSpeed, True))

        
    def display(self):
        self.update()
        image(self.img, self.x - 48, self.y - 100, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        fill(255,30,30)
        rect(self.x - 30, self.y - 52, 58 * self.health/20, 4)
        
        if self.health <= 0:
            main_game.score += self.scoreAmount
            self.spawn_powerup(5)
        
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
        
#------------------------------------------------------------------------------------------------------------------

class Queen(SpaceShip):
    def __init__(self, x, y, r = 80, img = "queen.png", w = 154, h = 215, num_slices = 4):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.vy = 0.4
        self.vx = 0
        self.health = 80
        self.scoreAmount = 200
        self.projectileSpeed = 5
        self.initialX = self.x
    
    def update(self):
        
        self.y += self.vy
        self.x += self.vx
        
        if self.y > 550:
            self.vy = 1.5
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        if frameCount % 130 == 0:
            chance = random.randint(1,2)
            if chance == 1:
                self.shoot()
    
    def shoot(self):
        main_game.enemyProjectiles.append(Projectile(5, self.x + 32, self.y + 50, 6, self.projectileSpeed, True))
        main_game.enemyProjectiles.append(Projectile(5, self.x + 65, self.y + 50, 6, self.projectileSpeed, True))
        main_game.enemyProjectiles.append(Projectile(5, self.x - 32, self.y + 50, 6, self.projectileSpeed, True))
        main_game.enemyProjectiles.append(Projectile(5, self.x - 65, self.y + 50, 6, self.projectileSpeed, True))

        
    def display(self):
        self.update()
        image(self.img, self.x - 75, self.y - 100, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        fill(255,30,30)
        rect(self.x - 48, self.y - 38, 96 * self.health/80, 4)
        
        if self.health <= 0:
            main_game.score += self.scoreAmount
            self.spawn_powerup(2)
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
        

        
# ------------------------------------------------------------------------------------------------------------------

class King(SpaceShip):
    def __init__(self, x, y, r = 200, img = "boss.png", w = 400, h = 400, num_slices = 4):
        SpaceShip.__init__(self, r, x, y, img, w, h, num_slices)
        self.vy = 0.4
        self.vx = 2 
        self.health = 650
        self.scoreAmount = 1000
        self.projectileSpeed = 5
        self.initialX = self.x
    
    def update(self):
        
        self.y += self.vy
        self.x += self.vx
        
        if self.y > 100:
            self.vy = 0
        
        if self.x > SCREEN_WIDTH or self.x < 0:
            self.vx = -self.vx
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        if frameCount % 130 == 0:
            self.shootTwo()
        if frameCount % 100 == 0:
            self.shoot()
    
    def shoot(self):
        main_game.enemyProjectiles.append(Projectile(27, self.x + 70, self.y + self.radius - 20, 6, 3.5, False, True))
        main_game.enemyProjectiles.append(Projectile(27, self.x - 70, self.y + self.radius - 20, 6, 3.5, False, True))
    
    def shootTwo(self):
        main_game.enemyProjectiles.append(Projectile(27, self.x - 150, self.y + self.radius - 20, 6, 6, True))
        main_game.enemyProjectiles.append(Projectile(27, self.x + 200, self.y + self.radius - 20, 6, 6, True))


        
    def display(self):
        self.update()
        image(self.img, self.x - self.radius, self.y - self.radius + 20, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        fill(255,30,30)
        rect(self.x - 150, self.y , 295 * self.health/650, 5)
        
        if self.health <= 0:
            main_game.score += self.scoreAmount
            main_game.gameWon = True
        # fill(255,0,0)
        # noStroke()
        # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)

# ------------------------------------------------------------------------------------------------------------------


# PROJECTILE class    
class Projectile:
    def __init__(self, r, x, y, dir, s, isImage = False, isRed = False):
        self.radius = r
        self.x = x
        self.y = y
        self.dir = dir # This direction is set based on the clock. So 12 means up, 6 means down, 4 means south east etc...
        self.speed = s
        self.vx = 0
        self.vy = 0
        self.used = False # This variable is used to detect when a projectile has already collided once
        self.isImage = isImage
        self.img = loadImage(path + "/images/rocket2.png")
        self.img_w = 12
        self.img_h = 50
        self.slice = 0
        self.num_slices = 4
        self.isRed = isRed
    
    def update(self):
        # The following if conditions sets the right velocity based on the direction the shots should move in
        if self.dir == 12:
            self.vx = 0
            self.vy = -self.speed
        elif self.dir == 6:
            self.vx = 0
            self.vy = self.speed
        elif self.dir == 4:
            self.vx = self.speed
            self.vy = self.speed
        elif self.dir == 7:
            self.vx = -self.speed
            self.vy = self.speed
        elif self.dir == 1:
            self.vx = self.speed
            self.vy = -self.speed
        elif self.dir == 11:
            self.vx = -self.speed
            self.vy = -self.speed
        
        self.x += self.vx
        self.y += self.vy
        
        if frameCount % 3 == 0:
            self.slice = (self.slice + 1) % self.num_slices
    
    def display(self):
        if self.used == False: # Only if the projectile hasn't collided already, the following code will execute
            self.update()
            if self.isImage == False:
                if self.isRed == False:
                    fill(0,255,126)
                else:
                    fill(255,0,0)
                noStroke()
                ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
            else:
                image(self.img, self.x - self.radius, self.y - self.radius - 30, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
                # fill(0,255,126)
                # noStroke()
                # ellipse(self.x, self.y, self.radius * 2, self.radius * 2)
                
    def collision(self, target):
        distance = ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5 # Check collision with target
        if distance <= self.radius + target.radius:
            self.used = True # If a collision is detected, then the projectile is used, it won't be displayed anymore
            return True
        else:
            return False
        
# ------------------------------------------------------------------------------------------------------------------

        
class HealthPowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/HP_Bonus.png")
        self.radius = 30
        self.img_w = self.radius * 2
        self.img_h = self.radius * 2
        self.healAmount = 30
        self.type = "health"
        self.used = False
    
    def give_health(self):
        main_game.player.health += self.healAmount
        if main_game.player.health > 100:
            main_game.player.health = 100
        
    def collision(self, target):
        distance = ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5 # Check collision with target
        if distance <= self.radius + target.radius:
            self.used = True # If a collision is detected, then the powerup is used, it won't be displayed anymore
            return True
        else:
            return False
    
    def display(self):
        image(self.img, self.x - self.radius, self.y - self.radius, self.img_w, self.img_h) 

# ------------------------------------------------------------------------------------------------------------------

# Rate of fire powerup
class ROFPowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.img = loadImage(path + "/images/Rockets_Bonus.png")
        self.img_w = self.radius * 2
        self.img_h = self.radius * 2
        self.type = "ROF"
        self.used = False
        
    def increase_ROF(self):
        main_game.player.rateOfFire -= 20
        if main_game.player.rateOfFire <= 15:
            main_game.player.rateOfFire = 15
            main_game.player.maxROF = True
        
        
    def collision(self, target):
        distance = ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5 # Check collision with target
        if distance <= self.radius + target.radius:
            self.used = True # If a collision is detected, then the powerup is used, it won't be displayed anymore
            return True
        else:
            return False
    
    def display(self):
        image(self.img, self.x - self.radius, self.y - self.radius, self.img_w, self.img_h)
        



# ------------------------------------------------------------------------------------------------------------------

class ShieldPowerUp:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/Armor_Bonus.png")
        self.radius = 30
        self.img_w = self.radius * 2
        self.img_h = self.radius * 2
        self.type = "shield"
        self.used = False 
    
    def collision(self, target):
        distance = ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5 # Check collision with target
        if distance <= self.radius + target.radius:
            self.used = True # If a collision is detected, then the powerup is used, it won't be displayed anymore
            return True
        else:
            return False
    def give_shield(self):
        main_game.player.shieldAmount = 70
    
    def display(self):
        image(self.img, self.x - self.radius, self.y - self.radius, self.img_w, self.img_h) 

# ------------------------------------------------------------------------------------------------------------------


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/explo.png")
        self.slice = 0
        self.numSlices = 4
        self.img_w = 100
        self.img_h = 95
        self.done = False
    
    def update(self):
        if self.slice < self.numSlices:
            if frameCount % 5 == 0:
                self.slice += 1
        else:
            self.done = True
                
    def display(self):
        image(self.img, self.x, self.y, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        
        self.update()

# ------------------------------------------------------------------------------------------------------------------

#GAME CLASS, the heart of everything
class Game:
    def __init__(self):
        self.player = HeroShip(45, 500, 500, "player_ship_spritesheet1.png", 128, 180, 4)
        self.explosions = []
        self.enemyProjectiles = []
        self.powerups = []
        self.playerProjectiles = [] # Use different lists for incoming projectiles and for player projectiles
        self.playerProjectileLimit = 10 # This limits the number of projectiles being rendered at a time, to improve performance
        self.timer = 0
        self.score = 0
        self.enemies = []
        self.y_shift = 0 # Used for background movement
        self.bg_img = loadImage(path + "/images/bg.jpeg") # For backgroundw
        self.bg_sound = player.loadFile(path + "/sounds/bg_music.mp3")
        self.bg_sound.loop()
        self.powerup_sound = player.loadFile(path + "/sounds/powerup.mp3")
        self.heart_img = loadImage(path + "/images/heart.png") # For heart/lives ui
        self.health_img = loadImage(path + "/images/healthbar.png") # For healthbar ui
        self.shield_img = loadImage(path + "/images/shield.png") # For shield ui
        self.intro_img = loadImage(path + "/images/intropage.png")
        self.lose_img = loadImage(path + "/images/gameover.png")
        self.win_img = loadImage(path + "/images/victory.png")
        self.gameStarted = False
        self.gameLost = False
        self.gameWon = False
        
        # for i in range(1):
        #     self.enemies.append(King(200 + 200*i, 100))

        self.wave1spawned = False
        self.wave2spawned = False
        self.wave3spawned = False
        self.wave4spawned = False
        self.wave5spawned = False
        self.wave6spawned = False
        self.wave7spawned = False
        self.wave8spawned = False
        self.wave9spawned = False
        self.wave10spawned = False
        self.wave11spawned = False

    
    def display_game(self):
        if self.gameStarted and self.gameLost == False and self.gameWon == False:
            self.y_shift += 1
            
            height_bottom = self.y_shift % SCREEN_HEIGHT
            height_top = SCREEN_HEIGHT - height_bottom
            image(self.bg_img, 0, 0, SCREEN_WIDTH, height_bottom, 0, height_top, SCREEN_WIDTH, SCREEN_HEIGHT)
            image(self.bg_img, 0, height_bottom, SCREEN_WIDTH, height_top, 0, 0, SCREEN_WIDTH, height_top)
            
            for projectile in self.enemyProjectiles:
                projectile.display()
                if projectile.used == False and projectile.collision(self.player):
                    if projectile.isRed == True:
                        self.player.take_damage(50)
                    else:
                        self.player.take_damage(10)
            
            for i in range(len(self.enemyProjectiles)):
                if self.enemyProjectiles[i].used == True:
                    self.enemyProjectiles.pop(i)
                    break
                
            for projectile in self.playerProjectiles:
                projectile.display()
                for enemy in self.enemies: # Check if the projectile collides with any enemy
                    if projectile.used == False and projectile.collision(enemy):
                        enemy.take_damage(10)
            
            # Loop through all powerups and use them based on their type
            for powerup in self.powerups:
                powerup.display()
                if powerup.used == False and powerup.collision(self.player):
                    if powerup.type == "health":
                        powerup.give_health()
                    elif powerup.type == "shield":
                        powerup.give_shield()
                    elif powerup.type == "ROF":
                        powerup.increase_ROF()
            
            # Remove any used powerups from the list
            for i in range(len(self.powerups)):
                if self.powerups[i].used == True:
                    self.powerup_sound.rewind()
                    self.powerup_sound.play()
                    self.powerups.pop(i)
                    break
                    
                
            #print(self.enemies[0].health)
            for enemy in self.enemies:
                enemy.display()
                
            for i in range(len(self.enemies)): # Check if any enemy is dead, if so, remove them from the list
                if self.enemies[i].health <= 0:
                    self.explosions.append(Explosion(self.enemies[i].x - self.enemies[i].radius, self.enemies[i].y - self.enemies[i].radius))
                    self.enemies.pop(i)
                    break
                elif self.enemies[i].y > 880:
                    self.enemies.pop(i)
                    self.score -= 10
                    # print("enemy removed")
                    break
                
            for explosion in self.explosions:
                explosion.display()
            
            for i in range(len(self.explosions)):
                if self.explosions[i].done == True:
                    self.explosions.pop(i)
                    break
            
            self.player.display()
            
            # This limits the number of projectiles that are present, so basically the first projectile (the furthest one) is removed when the limit is reached
            if len(self.playerProjectiles) == self.playerProjectileLimit:
                self.playerProjectiles.pop(0)
    
            if frameCount % 60 == 0:
                self.timer += 1
                print(self.timer)
            
            # Level design:
            
            if self.timer == 3 and self.wave1spawned == False:
                self.enemies.append(Pawn(200, -40))
                self.enemies.append(Pawn(400, -40))
                self.enemies.append(Pawn(600, -40))
                self.enemies.append(Pawn(800, -40))
                # self.enemies.append(Pawn(200, -50))
                self.wave1spawned = True
            elif self.timer == 13 and self.wave2spawned == False:
                self.enemies.append(Bishop(200, -40))
                self.enemies.append(Bishop(800, -40))
                self.wave2spawned = True
            elif self.timer == 23 and self.wave3spawned == False:
                self.enemies.append(Pawn(100, -40))
                self.enemies.append(Pawn(200, -40))
                self.enemies.append(Pawn(300, -40))
                self.enemies.append(Pawn(400, -40))
                self.enemies.append(Pawn(500, -40))
                self.enemies.append(Pawn(600, -40))
                self.enemies.append(Pawn(700, -40))
                self.enemies.append(Pawn(800, -40))
                self.enemies.append(Pawn(900, -40))
                self.enemies.append(Bishop(500, -90))
                self.wave3spawned = True
            elif self.timer == 30 and self.wave4spawned == False:
                self.enemies.append(Pawn(200, -40))
                self.enemies.append(Pawn(500, -40))
                self.enemies.append(Pawn(800, -40))
                self.enemies.append(Queen(350, -90))
                self.wave4spawned = True
            elif self.timer == 44 and self.wave5spawned == False:
                self.enemies.append(Knight(200, -40))
                self.enemies.append(Knight(400, -150))
                self.enemies.append(Knight(800, -40))
                self.wave5spawned = True
            elif self.timer == 66 and self.wave6spawned == False:
                self.enemies.append(Pawn(100, -40))
                self.enemies.append(Pawn(200, -40))
                self.enemies.append(Pawn(500, -40))
                self.enemies.append(Pawn(800, -40))
                self.enemies.append(Pawn(900, -40))
                self.enemies.append(Queen(400, -100))
                self.enemies.append(Queen(600, -100))
                self.enemies.append(Queen(500, -200))
                self.wave6spawned = True
            elif self.timer == 92 and self.wave7spawned == False:
                self.enemies.append(Pawn(200, -40))
                self.enemies.append(Pawn(300, -40))
                self.enemies.append(Pawn(700, -40))
                self.enemies.append(Pawn(800, -40))
                self.enemies.append(Knight(200, -60))
                self.enemies.append(Knight(500, -60))
                self.enemies.append(Knight(800, -60))
                self.enemies.append(Bishop(300, -150))
                self.enemies.append(Bishop(700, -150))
                self.wave7spawned = True
            elif self.timer == 117 and self.wave8spawned == False:
                self.enemies.append(Queen(150, -100))
                self.enemies.append(Queen(950, -100))
                self.enemies.append(Pawn(400, -40))
                self.enemies.append(Pawn(700, -40))
                self.enemies.append(Pawn(350, -80))
                self.enemies.append(Pawn(750, -80))
                self.enemies.append(Pawn(450, -80))
                self.enemies.append(Pawn(550, -90))
                self.enemies.append(Pawn(650, -90))
                self.wave8spawned = True
            elif self.timer == 137 and self.wave9spawned == False:
                self.enemies.append(Knight(200, -60))
                self.enemies.append(Knight(200, -200))
                self.enemies.append(Bishop(700, -60))
                self.enemies.append(Bishop(700, -200))
                self.enemies.append(Pawn(300, -40))
                self.enemies.append(Pawn(700, -40))
                self.enemies.append(Pawn(800, -40))
                self.enemies.append(Queen(450, -200))
                self.wave9spawned = True
            elif self.timer == 158 and self.wave10spawned == False:
                self.enemies.append(Queen(250, -260))
                self.enemies.append(Queen(650, -260))
                self.enemies.append(Bishop(700, -60))
                self.enemies.append(Bishop(800, -60))
                self.enemies.append(Bishop(200, -60))
                self.enemies.append(Bishop(100, -60))
                self.enemies.append(Knight(200, -200))
                self.enemies.append(Knight(800, -200))
                self.wave10spawned = True
            elif self.timer == 180 and self.wave11spawned == False:
                self.enemies.append(King(500, -250))
                self.wave11spawned = True
                
            self.show_ui()
        elif self.gameStarted == False and self.gameLost == False and self.gameWon == False:
            image(self.intro_img, 0, 0)
        elif self.gameLost:
            image(self.lose_img, 0, 0)
            fill(255)
            textSize(35)
            text("Score: " + str(self.score), 410, 400)
            self.bg_sound.mute()
            self.bg_sound.pause()
        elif self.gameWon:
            image(self.win_img, 0, 0)
            textSize(35)
            text("Score: " + str(self.score), 420, 400)
            self.bg_sound.mute()
            self.bg_sound.pause()
            
    def show_ui(self):
        fill(255)
        textSize(25)
        text("Score: " + str(self.score), 900, 40)
        image(self.health_img, 900, 95, 150 * self.player.health/100, 13, 0, 0, 150 * self.player.health/100, 13)
        image(self.shield_img, 900, 115, 150 * self.player.shieldAmount/70, 13, 0, 0, 150 * self.player.shieldAmount/70, 13)
        for i in range(self.player.lives):
            image(self.heart_img, 900 + 45*i, 50)
        if self.player.maxROF == True:
            textSize(15)
            text("Max fire-rate reached", 900, 150)




#Instantiating the game class
main_game = Game()


#SETUP AND DRAW
def setup():
    size(1080, 720)
    background(0)

def draw():
    background(0)
    main_game.display_game()

    
def keyPressed():
    if key == "a":
        main_game.player.key_handler["a"] = True
    elif key == "d":
        main_game.player.key_handler["d"] = True
    elif key == "s":
        main_game.player.key_handler["s"] = True
    elif key == "w":
        main_game.player.key_handler["w"] = True
    if main_game.gameStarted == False and key == "p":
        main_game.gameStarted = True
    if main_game.gameLost == True and key == "p" or main_game.gameWon == True and key == "p":
        global main_game
        main_game = Game()

def keyReleased():
    if key == "a":
        main_game.player.key_handler["a"] = False
    elif key == "d":
        main_game.player.key_handler["d"] = False
    elif key == "s":
        main_game.player.key_handler["s"] = False
    elif key == "w":
        main_game.player.key_handler["w"] = False
    
    
    
    
    
    
    
    
