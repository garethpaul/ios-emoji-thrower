//
//  ScoreViewController.swift
//  EmojiThrower
//
//  Created by Gareth on 6/17/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit
import QuartzCore
import TwitterKit

class ScoreViewController: UIViewController {

    var score: Int?
    var personImage: UIImage?
    var opponentFriend: Friend?
    
    @IBOutlet weak var person: UIImageView!
    @IBOutlet weak var scoreLabel: UILabel!
    @IBOutlet weak var emojiPlacement: UIImageView!
    
    @IBAction func shareBtn(_ sender: AnyObject) {
        let screen = captureScreen()
        
        let composer = TWTRComposer()
        
        composer.setText("@" + (opponentFriend?.screenname)! + " was hit " + (self.score?.stringValue)! + " times.")
        composer.setImage(screen)
        
        // Called from a UIViewController
        composer.show(from: self) { result in
            if (result == TWTRComposerResult.cancelled) {
                print("Tweet composition cancelled")
            }
            else {
                print("Sending tweet!")
            }
        }
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        person.image = personImage
        scoreLabel.font = UIFont(name: "Sketch3D", size: 34)
        scoreLabel.text = "@" + (opponentFriend?.screenname)! + " was hit " + (self.score?.stringValue)! + " times."
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    func captureScreen() -> UIImage {
        var window: UIWindow? = UIApplication.shared.keyWindow
        window = UIApplication.shared.windows[0]
        let size = CGSize(width: (window?.frame.width)!*0.99, height: (window?.frame.height)!*0.50)
        UIGraphicsBeginImageContextWithOptions(size, false, 0)
        var image:UIImage = UIGraphicsGetImageFromCurrentImageContext()!
        let rect = CGRect(x: -1, y: -1, width: (window?.frame.width)!, height: (window?.frame.height)!)
        self.view?.drawHierarchy(in: rect, afterScreenUpdates: true)
        let screenShot  = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        return screenShot!
        
    }
    
}
