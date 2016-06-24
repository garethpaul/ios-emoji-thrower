//
//  SettingsHelper.swift
//  EmojiThrower
//
//  Created by Gareth on 6/23/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import Foundation

class Settings: NSObject {
    
    //
    class func getTwtrKey() -> String {
        let arrayOfItems = NSArray(contentsOfFile: getPath())
        let twtrKey: String = arrayOfItems!.value(forKeyPath: "twtrKey") as! String
        return twtrKey
    }
    
    // MARK: Get the secret
    class func getTwtrSecret() -> String {
        let arrayOfItems = NSArray(contentsOfFile: getPath())
        let twtrSecret: String = arrayOfItems!.value(forKeyPath: "twtrSecret") as! String
        return twtrSecret
    }
    
    // MARK: Get the path for the resource
    class func getPath() -> String{
        let settingsPath = Bundle.main().pathForResource("Config", ofType: "plist")
        return settingsPath!
    }

}
