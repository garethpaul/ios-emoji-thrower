//
//  ScoreViewController.swift
//  EmojiThrower
//
//  Created by Gareth on 6/17/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit

class ScoreViewController: UIViewController {

    var score: Int?
    var personImage: UIImage?
    var opponentFriend: Friend?
    
    @IBOutlet weak var person: UIImageView!
    @IBOutlet weak var scoreLabel: UILabel!
    @IBOutlet weak var emojiPlacement: UIImageView!
    
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
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
