//
//  LoginViewController.swift
//  EmojiThrower
//
//  Created by Gareth on 6/17/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit
import TwitterKit
import Firebase
import FirebaseAuth

class LoginViewController: UIViewController {

    @IBAction func loginBtnTap(_ sender: AnyObject) {
        print("DB: loginBtnTap")
        //
        // Log the user in...
        Twitter.sharedInstance().logIn { (session, error) in
            if (session != nil) {
                //
                print("DB: TwitterLogin")
                // 1. Get Auth Token and Secret
                let authToken = session?.authToken
                let authTokenSecret = session?.authTokenSecret
                // 2. Set Credentials
                let credential = FIRTwitterAuthProvider.credential(withToken: authToken!, secret: authTokenSecret!)
                
                // 3. Store the username
                User.setUsername(userName: (session?.userName)!)
                
                API.getFriends(userID: (session?.userID)!)
                
                // 3. Complete Firebase Authentication
                FIRAuth.auth()?.signIn(with: credential, completion: { (user, error) in
                    //
                    print("DB: FIRAuth")
                    
                    let appDelegate = UIApplication.shared.delegate as! AppDelegate
                    appDelegate.ref?.child("users").child((session?.userName)!).setValue(["user": "active"], withCompletionBlock: { (error, ref) in
                        if error != nil {
                            print("DB Error " + String(describing: error))
                        } else {
                            print("DB Data saved")
                        }
                    })
                    
                    let storyboard = UIStoryboard(name: "Main", bundle: nil)
                    let initialVC = storyboard.instantiateInitialViewController()
                    appDelegate.window?.rootViewController = initialVC
                    
                })
            } // end sesion not nil
                
        } // end loginTap
    }
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
}
