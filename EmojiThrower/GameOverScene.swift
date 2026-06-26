//
//  GameOverScene.swift
//

import Foundation
import SpriteKit

class GameOverScene: SKScene {
    let resultLabel = SKLabelNode(fontNamed: "Helvetica")
    
    init(size: CGSize, won: Bool) {
        
        super.init(size: size)

        backgroundColor = .white

        let message = won ? "You Won!" : "You Lose!"

        resultLabel.text = message
        resultLabel.fontSize = 40
        resultLabel.fontColor = .black
        addChild(resultLabel)
        layoutResultLabel()

        run(SKAction.sequence([
            SKAction.wait(forDuration: 3.0),
            SKAction.run {
                let reveal = SKTransition.flipHorizontal(withDuration: 0.2)
                self.restartGame(size: self.size, transition: reveal)
            }
            ]))
        
    }

    func layoutResultLabel() {
        resultLabel.position = CGPoint(x: size.width/2, y: size.height/2)
    }

    override func didChangeSize(_ oldSize: CGSize) {
        super.didChangeSize(oldSize)
        layoutResultLabel()
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
