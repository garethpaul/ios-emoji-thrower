//
//  API.swift
//  EmojiThrower
//
//  Created by Gareth on 6/20/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import Foundation
import TwitterKit
import FirebaseDatabase
import Firebase

public func chunk<T>(_ size: Int = 2, _ input: [T]) -> [[T]] {
    let count = input.count
    var out = [[T]]()
    let n = count / size
    for x in 0..<n {
        let a = x * size
        let $ = x * size + size
        let chunk = [T](input[a..<$])
        out.append(chunk)
    }
    let remainder = count % size
    if remainder > 0 {
        let start = count - remainder
        out.append([T](input[start..<count]))
    }
    return out
}

class API: NSObject {

    class func getFriends(userID: String) -> Void {
        let client = TWTRAPIClient(userID: userID)
        let statusesShowEndpoint = "https://api.twitter.com/1.1/friends/ids.json"
        let params = ["screen_name": User.getUsername(), "count": "5000"]
        var clientError : NSError?
        
        let request = client.urlRequest(withMethod: "GET", url: statusesShowEndpoint, parameters: params, error: &clientError)
        
        client.sendTwitterRequest(request) { (response, data, connectionError) -> Void in
            if connectionError != nil {
                print("Error: \(connectionError)")
            }
            
            do {
                let json = try JSONSerialization.jsonObject(with: data!, options: []) as! [String:NSArray]
                let friends = json["ids"]
                //print(friends)
                getFriendsDetails(userID: userID, users: friends!)
            } catch let jsonError as NSError {
                print("json error: \(jsonError.localizedDescription)")
            }
        }
    }
    
    class func getFriendsDetails(userID: String, users: NSArray) {
        var input: [String] = []
        for item in users {
            input.append(String(describing: item))
        }
        
        let output = chunk(50, input)
        for friendGroup in output {
            // send api request
            let client = TWTRAPIClient(userID: userID)
            let statusesShowEndpoint = "https://api.twitter.com/1.1/users/lookup.json"
            let params = ["user_id": friendGroup.joined(separator: ",")]
            var clientError : NSError?
            
            let request = client.urlRequest(withMethod: "GET", url: statusesShowEndpoint, parameters: params, error: &clientError)
            
            client.sendTwitterRequest(request) { (response, data, connectionError) -> Void in
                if connectionError != nil {
                    print("Error: \(connectionError)")
                }
                
                var friends = [Friend]()
                do {
                    let json = try JSONSerialization.jsonObject(with: data!, options: [])
                    for anItem in json as! [Dictionary<String, AnyObject>] {
                        let screenName = anItem["screen_name"] as! String
                        let profileImage = anItem["profile_image_url"] as! String
                        let f: Friend = Friend(screenname: screenName, profilePic: profileImage)
                        friends.append(f)
                    }
                    // post friends
                    print("DB saving friends")
                    print("DB" + String(describing: friends))
                    saveFriends(friends: friends)
                    // get friends
                } catch let jsonError as NSError {
                    print("json error: \(jsonError.localizedDescription)")
                }
            }

            
        }
    }

    
    class func saveFriends(friends: [Friend]) {
        var payload = [[String:AnyObject]]()
        for friend in friends {
            payload.append(["screenname": friend.screenname! as AnyObject, "profile": friend.profilePic! as AnyObject])
        }

        print("DB user " + User.getUsername())
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        
        appDelegate.ref?.child("friends").child(User.getUsername()).setValue(payload, withCompletionBlock: { (error, ref) in
            // error
            if error != nil {
                print("DB payload error " + String(describing: error))
            } else {
                print("DB payload success")
            }
        })
    }
    

    
    class func fetchFriends( completion: @escaping (_ friends: [Friend]) -> () = {_ in }) {
        print("DB fetching friends")
        var friends = [Friend]()
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        appDelegate.ref?.child("friends").child(User.getUsername()).observe(FIRDataEventType.value, with: { (snapshot) in
            // Get user value
            print("DB get user values")
            for friend in snapshot.children.allObjects {
                print("DB " + String(describing: friend))
                
                let f = friend as! FIRDataSnapshot
                
                let screenname = (f.value as? NSDictionary)?["screenname"] as? String
                let profilePic = (f.value as? NSDictionary)?["profile"] as? String
                let newFriend = Friend(screenname: screenname!, profilePic: profilePic!)
                friends.append(newFriend)
            }
            completion(friends)
        }) { (error) in
            print(error.localizedDescription)
        }
        print("DB fetchFriends + " + String(describing: friends))
    }
}
