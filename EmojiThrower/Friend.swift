//
//  Friend.swift
//  EmojiThrower
//
//  Created by Gareth on 6/19/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import Foundation

class Friend: NSObject {
    
    // Insert code here to add functionality to your managed object subclass
    var screenname: String?
    var profilePic: String?
    
    init(screenname: String, profilePic: String) {
        self.screenname = screenname
        self.profilePic = profilePic
    }
}
