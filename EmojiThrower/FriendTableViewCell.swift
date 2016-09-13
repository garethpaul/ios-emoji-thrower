//
//  FriendViewCell.swift
//  EmojiThrower
//
//  Created by Gareth on 6/21/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit

struct MyModel {
    let imageUrl: NSURL
}

class FriendTableViewCell: UITableViewCell {

    @IBOutlet weak var profilePic: UIImageView!
    @IBOutlet weak var screenName: UILabel!
    var imageUrl: NSURL!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code

    }
    
    override func prepareForReuse() {
        super.prepareForReuse()
        self.profilePic.image = nil
        
    }
    
    
    func setData(f: Friend, completion: (_ completed: Bool) -> Void) {
        //
        self.screenName.text = f.screenname
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
