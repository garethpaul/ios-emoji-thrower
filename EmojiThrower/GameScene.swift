//
//  GameScene.swift
//
import SpriteKit

//MARK: - Vector Calculation Functions
func + (left: CGPoint, right: CGPoint) -> CGPoint {
    return CGPoint(x: left.x + right.x, y: left.y + right.y)
}

func - (left: CGPoint, right: CGPoint) -> CGPoint {
    return CGPoint(x: left.x - right.x, y: left.y - right.y)
}

func * (point: CGPoint, scalar: CGFloat) -> CGPoint {
    return CGPoint(x: point.x * scalar, y: point.y * scalar)
}

func / (point: CGPoint, scalar: CGFloat) -> CGPoint {
    return CGPoint(x: point.x / scalar, y: point.y / scalar)
}

#if !(arch(x86_64) || arch(arm64))
    func sqrt(a: CGFloat) -> CGFloat {
        return CGFloat(sqrtf(Float(a)))
    }
#endif

extension CGPoint {
    func length() -> CGFloat {
        return sqrt(x*x + y*y)
    }
    
    func normalized() -> CGPoint {
        return self / length()
    }
}

//MARK: - Create Physics
struct PhysicsCategory {
    static let None      : UInt32 = 0
    static let All       : UInt32 = UInt32.max
    static let Monster   : UInt32 = 0b1       // 1
    static let Projectile: UInt32 = 0b10      // 2
    static let Player    : UInt32 = 0b100     // 3
}


class GameScene: SKScene, SKPhysicsContactDelegate {
    
    //MARK: - Set up player sprite
    let player = SKSpriteNode(imageNamed: "player")
    
    var opponent: UIImage = UIImage()
    
    var monstersDestroyed = 0
    
    var playerDestroyed = false
    
    let scoreLabel = SKLabelNode(fontNamed: "Sketch3D")
    let backgroundVelocity : CGFloat = 2.0
    
    override func didMove(to view: SKView) {
        // set background color
        self.backgroundColor = SKColor.white()
        self.initializingScrollingBackground()
        // background music
        //let backgroundMusic = SKAudioNode(fileNamed: "background-music-aac.caf")
        //backgroundMusic.autoplayLooped = true
        //addChild(backgroundMusic)
        // set starting position
        player.position = CGPoint(x: size.width * 0.1, y: size.height * 0.5)
        // create sprite
        addChild(player)
        // add physics to player
        player.physicsBody = SKPhysicsBody(rectangleOf: player.size)
        player.physicsBody?.isDynamic = true
        player.physicsBody?.categoryBitMask = PhysicsCategory.Player
        player.physicsBody?.contactTestBitMask = PhysicsCategory.Monster
        player.physicsBody?.collisionBitMask = PhysicsCategory.None
        // set gravity to none and set scene as the delegate
        physicsWorld.gravity = CGVector(dx: 0, dy: 0)
        physicsWorld.contactDelegate = self
        // create monsters
        run(SKAction.repeatForever(
            SKAction.sequence([
                SKAction.run(addMonster),
                SKAction.wait(forDuration: 1.0)
                ])
            ))
        scoreLabel.fontSize = 50
        scoreLabel.position = CGPoint(x: (self.view?.frame.width)!/2, y: (self.view?.frame.height)!-40)
        scoreLabel.fontColor = #colorLiteral(red: 0.137254902, green: 0.137254902, blue: 0.3450980392, alpha: 1)
        addChild(scoreLabel)
    }
    //MARK: - Create a random number
    func random() -> CGFloat {
        return CGFloat(Float(arc4random()) / 0xFFFFFFFF)
    }
    // sets parameters of the random number
    func random(min: CGFloat, max: CGFloat) -> CGFloat {
        return random() * (max - min) + min
    }
    
    //MARK: - Get Profile Picture
    func roundSquareImage(imageName: String) -> SKSpriteNode {
        let originalPicture = UIImage(named: imageName)
        // create the image with rounded corners
        UIGraphicsBeginImageContextWithOptions(originalPicture!.size, false, 0)
        let rect = CGRect(x: 0, y: 0, width: originalPicture!.size.width, height: (originalPicture?.size.height)!)
        
        let rectPath : UIBezierPath = UIBezierPath(roundedRect: rect, cornerRadius: 30.0)
        rectPath.addClip()
        originalPicture!.draw(in: rect)
        let scaledImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext();
        
        let texture = SKTexture(image: scaledImage!)
        let roundedImage = SKSpriteNode(texture: texture, size: CGSize(width: (originalPicture?.size.width)!, height: (originalPicture?.size.height)!))
        roundedImage.name = imageName
        return roundedImage
    }
    
    //MARK: - Create Monster Sprite
    func addMonster() {
        
        // Create sprite
        // let paths = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)[0] as String
        // let getImagePath = paths.appending("opponent.png")
        let imageis: UIImage = opponent
        let Texture = SKTexture(image: imageis)
//        let mySprite =
        
        let monster = SKSpriteNode(texture: Texture) //SKSpriteNode(imageNamed: "Goblin")
        
        
        // Determine where to spawn the monster along the Y axis
        let actualY = random(min: monster.size.height/2, max: size.height - monster.size.height/2)
        
        // Position the monster slightly off-screen along the right edge,
        // and along a random position along the Y axis as calculated above
        monster.position = CGPoint(x: size.width + monster.size.width/2, y: actualY)
        
        // Add the monster to the scene
        addChild(monster)
        
        // Add physics qualities to monster
        monster.physicsBody = SKPhysicsBody(rectangleOf: monster.size)
        monster.physicsBody?.isDynamic = true
        monster.physicsBody?.categoryBitMask = PhysicsCategory.Monster
        monster.physicsBody?.contactTestBitMask = PhysicsCategory.Projectile
        monster.physicsBody?.collisionBitMask = PhysicsCategory.None
        
        // Determine speed of the monster
        let actualSpeed = random(min: CGFloat(4.0), max: CGFloat(10.0))
        
        // Create the actions
        let actionMove = SKAction.move(to: CGPoint(x: -monster.size.width/2, y: actualY), duration: TimeInterval(actualSpeed))
        // !this is important to not over-load the memory of the decvice!
        let actionMoveDone = SKAction.removeFromParent()
        

        // Apply the actions to the monster
        monster.run(SKAction.sequence([actionMove, actionMoveDone]))
        
    }
    
    func initializingScrollingBackground() {
        for index in 0 ..< 2 {

            let bg = SKSpriteNode(imageNamed: "bg")
            bg.position = CGPoint(x: index * Int(bg.size.width), y: 0)
            bg.anchorPoint = CGPoint()
            bg.name = "background"
            self.addChild(bg)
        }
    }
    
    //
    func moveBackground() {
        self.enumerateChildNodes(withName: "background", using: { (node, stop) -> Void in
            if let bg = node as? SKSpriteNode {
                bg.size = self.frame.size
                bg.position = CGPoint(x: 0 - self.backgroundVelocity, y: bg.position.y)
                bg.zPosition = -13
                // Checks if bg node is completely scrolled off the screen, if yes, then puts it at the end of the other node.
                if bg.position.x <= -bg.size.width {
                    bg.position = CGPoint(x: bg.position.x + bg.size.width * 2, y: bg.position.y)
                }
            }
        })
    }
    
    override func update(_ currentTime: CFTimeInterval) {
        /* Called before each frame is rendered */
        
        //self.moveBackground()
    }
    
    
    //MARK: - Projectile Launching Function
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        
        // Choose one of the touches to work with
        guard let touch = touches.first else {
            return
        }
        let touchLocation = touch.location(in: self)
        
        // Set up initial location of projectile
        let projectile = SKSpriteNode(imageNamed: "projectile")
        projectile.position = player.position
        
        // Determine offset of touch location to projectile
        let offset = touchLocation - projectile.position
        
        // Cancel shot if you are shooting down or backwards
        if (offset.x < 0) { return }
        
        // Projectile collision set up
        projectile.physicsBody = SKPhysicsBody(circleOfRadius: projectile.size.width/2)
        projectile.physicsBody?.isDynamic = true
        projectile.physicsBody?.categoryBitMask = PhysicsCategory.Projectile
        projectile.physicsBody?.contactTestBitMask = PhysicsCategory.Monster
        projectile.physicsBody?.collisionBitMask = PhysicsCategory.None
        projectile.physicsBody?.usesPreciseCollisionDetection = true
        
        // Add projectile after double-checking direction of shot
        addChild(projectile)
        
        // Get the direction of where to shoot
        let direction = offset.normalized()
        
        // Make it shoot far enough to be guaranteed off screen
        let shootDistance = direction * 1000
        
        // Add the shoot amount to the current position
        let realDest = shootDistance + projectile.position
        
        // Create the actions
        let actionMove = SKAction.move(to: realDest, duration: 2.0)
        let actionMoveDone = SKAction.removeFromParent()
        projectile.run(SKAction.sequence([actionMove, actionMoveDone]))
        
        // Projectile sound effect
        //run(SKAction.playSoundFileNamed("pew-pew-lei.caf", waitForCompletion: false))
    }
    
    //MARK: - Projectile Collision Actions
    func projectileDidCollideWithMonster(_ projectile:SKSpriteNode, monster:SKSpriteNode) {
        monstersDestroyed += 1
        print("\(monstersDestroyed)")
        scoreLabel.text = "Score: \(monstersDestroyed)"
        projectile.removeFromParent()
        monster.removeFromParent()
        
        // check timer and if end then show end
        
        // keep score
        if (monstersDestroyed >= 300) {
            let reveal = SKTransition.flipHorizontal(withDuration: 2)
            let gameOverScene = GameOverScene(size: self.size, won: true)
            self.view?.presentScene(gameOverScene, transition: reveal)
        }
    }
    func monsterDidCollideWithPlayer(_ monster:SKSpriteNode, player:SKSpriteNode) {
        playerDestroyed = true

        player.removeFromParent()
        
        if playerDestroyed == true {
            let reveal = SKTransition.flipVertical(withDuration: 2)
            let gameOverScene = GameOverScene(size: self.size, won: false)
            self.view?.presentScene(gameOverScene, transition: reveal)
        }
    }
    //MARK: - Contact Delegate Methods
    func didBegin(_ contact: SKPhysicsContact) {
        
        var firstBody: SKPhysicsBody
        var secondBody: SKPhysicsBody
        if contact.bodyA.categoryBitMask < contact.bodyB.categoryBitMask {
            firstBody = contact.bodyA
            secondBody = contact.bodyB
        } else {
            firstBody = contact.bodyB
            secondBody = contact.bodyA
        }
        
//
        if (firstBody.categoryBitMask & PhysicsCategory.Monster != 0) && (secondBody.categoryBitMask & PhysicsCategory.Projectile != 0) {
            projectileDidCollideWithMonster(firstBody.node as! SKSpriteNode, monster: secondBody.node as! SKSpriteNode)
        }
        
    }
    func movePlayer() {
        
    }

}
