//
//  User.swift
//  EmojiThrower
//
//  Created by Gareth on 6/19/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import Foundation

class User : NSObject {
    
    class func hasOnboarded() -> Bool {
        return UserDefaults.standard.bool(forKey: "user_has_onboarded");
    }
    
    class func completeOnboarding() -> Void {
        UserDefaults.standard.set(true, forKey: "user_has_onboarded")
    }
    
    class func getUsername() -> String {
        return UserDefaults.standard.string(forKey: "username")!
    }
    
    class func setUsername(userName: String) -> Void {
        return UserDefaults.standard.set(userName, forKey: "username")
    }
    
    class func getNonce() -> String {
        return UserDefaults.standard.string(forKey: "nonce")!
    }
    
    class func setNonce(nonce: String) -> Void {
        return UserDefaults.standard.set(nonce, forKey: "nonce")
    }
}
    
