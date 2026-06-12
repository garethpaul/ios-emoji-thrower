//
//  GameOverScene.swift
//

import Foundation
import SpriteKit

class GameOverScene: SKScene {
    
    init(size: CGSize, won: Bool) {
        
        super.init(size: size)

        backgroundColor = .white

        let message = won ? "You Won!" : "You Lose!"

        let label = SKLabelNode(fontNamed: "Helvetica")
        label.text = message
        label.fontSize = 40
        label.fontColor = .black
        label.position = CGPoint(x: size.width/2, y: size.height/2)
        addChild(label)

        run(SKAction.sequence([
            SKAction.wait(forDuration: 3.0),
            SKAction.run {
                let reveal = SKTransition.flipHorizontal(withDuration: 0.2)
                self.restartGame(size: size, transition: reveal)
            }
            ]))
        
    }

    func restartGame(size: CGSize, transition: SKTransition) -> Bool {
        guard let view = self.view, view.scene === self else {
            return false
        }

        let scene = GameScene(size: size)
        scene.scaleMode = .resizeFill
        view.presentScene(scene, transition: transition)
        return true
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
