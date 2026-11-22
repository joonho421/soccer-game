from cmu_graphics import *
import math

####################################
#Model
####################################
def onAppStart(app):
    
    # Game Settings
    app.playerRadius = 13
    app.ballRadius = 8
    app.playerSpeed = 4
    app.ballSpeed = 10
    app.friction = 0.92
    app.goalSize = 160
    app.scoreToWin = 3
    app.tackleCooldownSteps = 150
    
    #Scores
    app.messiScore = 0
    app.ronaldoScore = 0
    
    #Winner
    app.gameOver = False
    app.winner = None
    
    #Start first round
    resetRound(app)
    
    #players
    app.messi = 'cmu://1166357/46549453/messi.png'
    app.ronaldo = 'cmu://1166357/46549476/ronaldo.png'
    
def resetRound(app):
    # Messi starts on left
    app.messiX = 150
    app.messiY = app.height//2
    
    #ronaldo starts on right
    app.ronaldoX = app.width - 150
    app.ronaldoY = app.height // 2
    
    #Ball starts in middle
    app.ballX = app.width // 2
    app.ballY = app.height // 2
    app.ballDX = 0
    app.ballDY = 0
    
    #Who has the ball: None, 'messi', or 'ronaldo'
    app.possession = None
    
    #Last movement direction of each player. Helps decide which way the ball is shot
    app.messiDirX = 1
    app.messiDirY = 0
    app.ronaldoDirX = -1
    app.ronaldoDirY = 0
    # Tackle Cooldown
    app.messiTackleTimer = 0
    app.ronaldoTackleTimer = 0
    
####################################
# Controller
####################################

def onKeyHold(app, keys):     
    if not app.gameOver:
        moveMessi(app, keys)
        moveRonaldo(app, keys)
        keepPlayersInBounds(app)
    
def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)
    if not app.gameOver:
        if key == 'space' and app.possession == 'messi':
            shootBall(app, 'messi')
        
        if key == 'enter' and app.possession == 'ronaldo':
            shootBall(app, 'ronaldo')
        
        if key == 'q':
            tryTackle(app, 'messi')
        
        if key == '/':
            tryTackle(app, 'ronaldo')
        
            
def onStep(app):
    if not app.gameOver:
        updateTackleTimers(app)
        updatePossession(app)
        updateBall(app)
        checkForGoal(app)
        checkWinner(app)
        
        
        
####################################
# Controller Helpers
####################################

def moveMessi(app, keys):  #AI-helped function
    dx = 0
    dy = 0
    
    if 'w' in keys:
        dy -= 1
    if 's' in keys:
        dy += 1
    if 'a' in keys:
        dx -= 1
    if 'd' in keys:
        dx += 1
    # normalize
    if dx != 0 or dy != 0:
        length = math.sqrt(dx ** 2 + dy ** 2)
        dx /= length
        dy /= length
        
        app.messiX += dx * app.playerSpeed
        app.messiY += dy * app.playerSpeed
        app.messiDirX = dx
        app.messiDirY = dy

def moveRonaldo(app, keys):
    dx = 0
    dy = 0
    
    if 'up' in keys:
        dy -= 1
    if 'down' in keys:
        dy += 1
    if 'left' in keys:
        dx -= 1
    if 'right' in keys:
        dx += 1
    if dx != 0 or dy != 0:
        length = math.sqrt(dx ** 2 + dy ** 2)
        dx /= length
        dy /= length
        
        app.ronaldoX += dx * app.playerSpeed
        app.ronaldoY += dy * app.playerSpeed
        app.ronaldoDirX = dx
        app.ronaldoDirY = dy
        
def keepPlayersInBounds(app):
    r = app.playerRadius
    # Messi
    
    #left boundary
    if app.messiX < r:
        app.messiX = r
    #right boundary
    if app.messiX > app.width - r:
        app.messiX = app.width - r
    #top boundary
    if app.messiY < r:
        app.messiY = r
    #bottom boundary
    if app.messiY > app.height - r:
        app.messiY = app.height - r
    
    # Ronaldo
    if app.ronaldoX < r:
        app.ronaldoX = r
    if app.ronaldoX > app.width - r:
        app.ronaldoX = app.width - r
    if app.ronaldoY < r:
        app.ronaldoY = r
    if app.ronaldoY > app.height - r:
        app.ronaldoY = app.height - r
    

def updatePossession(app):
    if app.possession == None:
        if circlesOverlap(app.messiX, app.messiY, app.playerRadius, app.ballX, app.ballY, app.ballRadius):
            app.possession = 'messi'
            app.ballDX = 0
            app.ballDY = 0
        
        
        elif circlesOverlap(app.ronaldoX, app.ronaldoY, app.playerRadius, app.ballX, app.ballY, app.ballRadius):
            app.possession = 'ronaldo'
            app.ballDX = 0
            app.ballDY = 0
            

def updateBall(app):  #AI-helped function
    if app.possession == 'messi':
        offset = app.playerRadius + app.ballRadius + 2
        app.ballX = app.messiX + app.messiDirX * offset
        app.ballY = app.messiY + app.messiDirY * offset
    
    elif app.possession == 'ronaldo':
        offset = app.playerRadius + app.ballRadius + 2
        app.ballX = app.ronaldoX + app.ronaldoDirX * offset
        app.ballY = app.ronaldoY + app.ronaldoDirY * offset
    
    else:
        app.ballX += app.ballDX
        app.ballY += app.ballDY
        
        app.ballDX *= app.friction
        app.ballDY *= app.friction
        
        #stops tiny movement
        if abs(app.ballDX) < 0.1:
            app.ballDX = 0
        if abs(app.ballDY) < 0.1:
            app.ballDY = 0
            
        bounceBallOffWalls(app)
        

def shootBall(app, player):
    app.possession = None
    if player == 'messi':
        offset = app.playerRadius + app.ballRadius + 8
        app.ballX = app.messiX + app.messiDirX * offset
        app.ballY = app.messiY + app.messiDirY * offset
        app.ballDX = app.messiDirX * app.ballSpeed
        app.ballDY = app.messiDirY * app.ballSpeed
    
 
 
    elif player == 'ronaldo':
        #to make it look like shooting
        offset = app.playerRadius + app.ballRadius + 8
        app.ballX = app.ronaldoX + app.ronaldoDirX * offset
        app.ballY = app.ronaldoY + app.ronaldoDirY * offset
        app.ballDX = app.ronaldoDirX * app.ballSpeed
        app.ballDY = app.ronaldoDirY * app.ballSpeed
    
    
def bounceBallOffWalls(app):
    goalTop = app.height/2 - app.goalSize /2
    goalBottom = app.height/2 + app.goalSize /2
    inGoalOpening = (goalTop <= app.ballY <= goalBottom)
    
    # Top wall
    if app.ballY - app.ballRadius <= 0:
        app.ballY = app.ballRadius
        app.ballDY *= -1
    
    #Bottom Wall
    elif app.ballY + app.ballRadius >= app.height:
        app.ballY = app.height - app.ballRadius
        app.ballDY *= -1
    
    
    
        
    
def checkForGoal(app):
    goalTop = app.height/2 - app.goalSize /2
    goalBottom = app.height/2 + app.goalSize /2
    inGoalOpening = (goalTop <= app.ballY <= goalBottom)
    
    if app.ballX - app.ballRadius <= 0:
        if inGoalOpening:
            app.ronaldoScore += 1
            resetRound(app)
        else:
            app.ballX = app.ballRadius
            app.ballDX *= -1
    
    elif app.ballX + app.ballRadius >= app.width:
        if inGoalOpening:
            app.messiScore += 1
            resetRound(app)
        else:
            app.ballX = app.width - app.ballRadius
            app.ballDX *= -1
        
def checkWinner(app):
    if app.messiScore >= app.scoreToWin:
        app.gameOver = True
        app.winner = 'Messi'
    
    elif app.ronaldoScore >= app.scoreToWin:
        app.gameOver = True
        app.winner = 'Ronaldo'
        
def circlesOverlap(x1, y1, r1, x2, y2, r2):     #AI generated
    distance = math.dist((x1, y1), (x2, y2))
    return distance <= r1 + r2
    
    
def updateTackleTimers(app):
    if app.messiTackleTimer > 0:
        app.messiTackleTimer -= 1
    
    if app.ronaldoTackleTimer > 0:
        app.ronaldoTackleTimer -= 1
        
def tryTackle(app, player):
    if player == 'messi':
        if app.messiTackleTimer > 0:
            return
        if circlesOverlap(app.messiX, app.messiY, app.playerRadius, app.ronaldoX, app.ronaldoY, app.playerRadius):
            if app.possession == 'ronaldo':
                app.possession = 'messi'
                app.ballDX = 0
                app.ballDY = 0
                app.messiTackleTimer = app.tackleCooldownSteps
    
    elif player == 'ronaldo':
        if app.ronaldoTackleTimer > 0:
            return
        
        if circlesOverlap(app.ronaldoX, app.ronaldoY, app.playerRadius, app.messiX, app.messiY, app.playerRadius):
            if app.possession == 'messi':
                app.possession = 'ronaldo'
                app.ballDX = 0
                app.ballDY = 0
                app.ronaldoTackleTimer = app.tackleCooldownSteps
                

                            
    
    
    
    
    
    
    
    
    
    
####################################
# View
####################################

def redrawAll(app):
    drawField(app)
    drawGoals(app)
    drawBall(app)
    drawPlayers(app)
    drawScore(app)
    drawInstructions(app)
    drawPenaltyBox(app)
    drawCooldownTimers(app)
    
    if app.gameOver:
        drawGameOverScreen(app)
        
def drawField(app):
    drawRect(0, 0, app.width, app.height, fill = 'green')
    drawLine(app.width/2, 0, app.width/2, app.height, fill = 'white')
    drawCircle(app.width/2, app.height/2, 40, fill = None, border = 'white')
    
def drawGoals(app):
    goalTop = app.height/2 - app.goalSize/2
    drawRect(0, goalTop, 10, app.goalSize, fill = 'white')
    drawRect(app.width -10, goalTop, 10, app.goalSize, fill = 'white')
    
def drawBall(app):
    drawCircle(app.ballX, app.ballY, app.ballRadius, fill = 'white', border = 'black')

def drawPlayers(app):
    size = app.playerRadius * 4
    
    drawImage(app.messi, app.messiX, app.messiY, align = 'center', width = size, height = size)
    drawImage(app.ronaldo, app.ronaldoX, app.ronaldoY, align = 'center', width = size, height = size)
    
def drawScore(app):
    drawLabel(f'{app.messiScore} - {app.ronaldoScore}', 200, 20, size = 30, fill = 'black', font = 'arial')

def drawInstructions(app):
    drawLabel('Messi: WASD + Space shoot + Q tackle', 100, 380, size = 10, fill = 'white')
    drawLabel('Ronaldo: Arrows + Enter shoot + / tackle', 300, 380, size = 10, fill = 'white')

def drawGameOverScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel(f'{app.winner} wins!!!', 200, 180, size = 40, fill = 'white', bold = True, border = 'black')
    drawLabel('Press r to restart', 200, 220, size = 15, fill = 'white')

def drawPenaltyBox(app):
    
    #left
    drawLine(0, 90, 70, 90, fill = 'white')
    drawLine(0, 310, 70, 310, fill = 'white')
    drawLine(70, 90, 70, 310, fill = 'white')
    drawLine(0, 90, 70, 90, fill = 'white')
    
    #right
    drawLine(330, 90, 400, 90, fill = 'white')
    drawLine(330, 310, 400, 310, fill = 'white')
    drawLine(330, 90, 330, 310, fill = 'white')
    
def drawCooldownTimers(app):
    drawLabel(f'Messi Cooldown: {app.messiTackleTimer}', 80, 30, size = 12, fill = 'blue')
    drawLabel(f'Ronaldo Cooldown: {app.ronaldoTackleTimer}', 315, 30, size = 12, fill = 'blue')


######
# Main
######

def main():
    runApp()
    
main()
    

# Image Citations: Messi image: https://wallpapers.com/png/lionel-messi-portraitin-argentina-kit-r71zpm3d9yheba7b.html, Ronaldo image: https://www.kindpng.com/imgv/ibRhTh_cristiano-ronaldo-sofifa-hd-png-download/