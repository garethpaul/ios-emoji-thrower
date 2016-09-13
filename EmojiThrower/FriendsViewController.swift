//
//  FriendsViewController.swift
//  EmojiThrower
//
//  Created by Gareth on 6/21/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit

class FriendsViewController: UITableViewController {
    
    var f: [Friend] = []
    var o: UIImage? = nil
    var of: Friend?
    let section = ["People you may know.", "Other folks."]
    let popular: [Friend] = [Friend(screenname: "realdonaldtrump", profilePic: "https://twitter.com/realdonaldtrump/profile_image?size=original"),
                             Friend(screenname: "BorisJohnson", profilePic: "https://twitter.com/borisjohnson/profile_image?size=original"),
                             Friend(screenname: "twitter", profilePic: "https://twitter.com/twitter/profile_image?size=original"),
                             Friend(screenname: "jack", profilePic: "https://twitter.com/jack/profile_image?size=original")]
    
    // MARK: View Did Load : Called after the controller's view is loaded into memory.
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let imageView = UIImageView(frame: CGRect(x: 0, y: 0, width: 50, height: 50))
        imageView.contentMode = .scaleAspectFit
        
        let logoImage = UIImage(named: "logoIcon")
        imageView.image = logoImage
        navigationItem.titleView = imageView
        let nib = UINib(nibName: "FriendTableViewCell", bundle: nil)
        self.tableView.register(nib, forCellReuseIdentifier: "friendCell")
        
        API.fetchFriends { (friends) in
            self.f = friends
            self.do_table_refresh()
        }
    }

    // MARK: - Table view data source
    override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return section.count
    }
    
    // MARK: - Table view data source
    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return self.section[section]
    }
    
    
    // MARK: Refresh the table
    func do_table_refresh() {
        self.tableView.reloadData()
    }

    // MARK: Set number of rows in secton
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        if section == 0 {
            return self.popular.count
        } else if section == 1 {
            return self.f.count
        } else {
            return 0
        }
    }

    // MARK: Set Height
    override func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 70
    }
    
    // MARK: Show cell at row
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell:FriendTableViewCell = self.tableView.dequeueReusableCell(withIdentifier: "friendCell") as! FriendTableViewCell
        
        let friend: Friend?
        print("GET CELL" + String(indexPath.section))
        if indexPath.section == 0 {
            friend = self.popular[indexPath.row]
            return processCell(cell: cell, indexPath: indexPath, friend: friend!)
        } else if indexPath.section == 1 {
            friend = self.f[indexPath.row]
            return processCell(cell: cell, indexPath: indexPath, friend: friend!)
        } else {
            friend = self.f[indexPath.row]
            return processCell(cell: cell, indexPath: indexPath, friend: friend!)
            
            
        }
    }
    
    func processCell(cell: FriendTableViewCell, indexPath: IndexPath, friend: Friend) -> FriendTableViewCell {
        cell.tag = indexPath.row
        
        let profilePictureURL = "https://twitter.com/" + (friend.screenname)! + "/profile_image?size=original"
        
        if cell.profilePic.image == nil {
            UIImage().setImage(url: profilePictureURL, completion: { (image) in
                DispatchQueue.main.async(execute: {
                    let actualCell: FriendTableViewCell = self.tableView.cellForRow(at: indexPath) as! FriendTableViewCell
                    actualCell.profilePic.image = image.circle
                    actualCell.layoutSubviews()
                })
            })
        }
        
        cell.setData(f: friend, completion: { (completed) in
            cell.setNeedsLayout()
        })
        return cell
    }
    // MARK: Did select row
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        // Set data and move to GameView
        let friend: Friend?
        if indexPath.section == 0 {
            friend = self.popular[indexPath.row]
        } else if indexPath.section == 1 {
            friend = self.f[indexPath.row]
        } else {
            friend = self.f[indexPath.row]
        }
        
        let profilePictureURL = "https://twitter.com/" + (friend?.screenname!)! + "/profile_image?size=original"
        UIImage().setImage(url: profilePictureURL, completion: { (image) in
            self.o = image
            self.of = friend
            self.performSegue(withIdentifier: "playGame", sender: self)
        })
    }

    
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        print("preparing to move")
        if(segue.identifier == "playGame") {
            // Move to play game
            print("moving to play the game")
            if let gameVC:GameViewController = (segue.destination as? GameViewController){
                gameVC.opponent = self.o!.resizeImage!.circle!
                gameVC.opponentFriend = of
            }
        }
    }
    
    // MARK: Memory Warning
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

}
