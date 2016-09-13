//
//  GameViewController.swift
//

import UIKit
import SpriteKit

class GameViewController: UIViewController {
    
    var opponent: UIImage = UIImage()
    var opponentFriend: Friend?
    var gameTime = 30
    var timer: Timer?
    var timerLayer: UIView?
    var scene: GameScene?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        scene = GameScene(size: view.bounds.size)
        scene?.opponent = opponent
        let skView = view as! SKView
        skView.showsFPS = true
        skView.showsNodeCount = true
        skView.ignoresSiblingOrder = true
        scene?.scaleMode = .resizeFill
        skView.presentScene(scene)
        
        //
        let topLayer=UIView(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: 50))
        topLayer.backgroundColor=UIColor().HexToColor(hexString: "#6E2000")
        self.view.addSubview(topLayer)
        
        timer = Timer.scheduledTimer(timeInterval: 3.0, target: self, selector: #selector(GameViewController.countdown), userInfo: nil, repeats: true)
        timerLayer = UIView(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: 50))
        timerLayer?.backgroundColor=UIColor().HexToColor(hexString: "#C1694F")
        self.view.addSubview(timerLayer!)
    }
    
    func transformFromRect(from: CGRect, toRect to: CGRect) -> CGAffineTransform {
        let transform = CGAffineTransform(translationX: to.midX-from.midX, y: to.midY-from.midY)
        return transform.scaledBy(x: to.width/from.width, y: to.height/from.height)
    }
    
    func countdown()
    {
        self.gameTime = self.gameTime - 3
        //timerLayer?.removeFromSuperview()
        let percentage = CGFloat(self.gameTime)/CGFloat(20)

        if self.gameTime == 0 {
            self.timer?.invalidate()
            timer = nil
            self.gameOver()
        }
        
        UIView.animate(
            withDuration: 0.5,
            delay: 0,
            options: .beginFromCurrentState,
            animations: { () -> Void in
                let width = CGFloat(self.view.frame.width)*CGFloat(percentage)
                let toRect = CGRect(x: 0, y: 0, width: width, height: 50)
                let fromRect = CGRect(x: 0, y: 0, width: self.view.frame.width, height: 50)
                let transform: CGAffineTransform = self.transformFromRect(from: fromRect, toRect: toRect)
                self.timerLayer?.transform = transform
                self.view.layoutIfNeeded()
        }) { (completed:Bool) -> Void in
            //self.view.transform = CGAffineTransform(scaleX: 0.5, y: 0.5)
            // or, to reset:
            // self.view.transform = CGAffineTransformIdentity
        }
    }
    func gameOver() {
        // segue to new ViewController
        self.performSegue(withIdentifier: "shareGame", sender: self)
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(true)
        self.timer?.invalidate()
        self.timer = nil
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if(segue.identifier == "shareGame") {
            if let shareVC:ScoreViewController = (segue.destination as! ScoreViewController){
                shareVC.score = scene?.monstersDestroyed
                shareVC.personImage = self.opponent
                shareVC.opponentFriend = self.opponentFriend
            }
        }
    }
}
