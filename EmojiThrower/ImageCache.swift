//
//  ImageCache.swift
//  EmojiThrower
//
//  Created by Gareth on 6/21/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import Foundation
import UIKit

public class MyImageCache {
    
    var sharedCache: NSCache<AnyObject, AnyObject>;
    
    init() {
        sharedCache = NSCache()
        sharedCache.name = "MyImageCache"
        sharedCache.countLimit = 200 // Max 200 images in memory.
        sharedCache.totalCostLimit = 100*1024*1024 // Max 100MB used.
    }
}


extension NSURL {
    
    typealias ImageCacheCompletion = (UIImage) -> Void
    
    /// Retrieves a pre-cached image, or nil if it isn't cached.
    /// You should call this before calling fetchImage.
    var cachedImage: UIImage? {
        return MyImageCache.init().sharedCache.object(
            forKey: absoluteString! as AnyObject) as? UIImage
    }
    
    /// Fetches the image from the network.
    /// Stores it in the cache if successful.
    /// Only calls completion on successful image download.
    /// Completion is called on the main thread.
    func fetchImage(completion: @escaping ImageCacheCompletion) {
        let task = URLSession.shared.dataTask(with: self as URL) {
            data, response, error in
            if error == nil {
                if let  data = data,
                    let image = UIImage(data: data) {
                    MyImageCache.init().sharedCache.setObject(
                        image,
                        forKey: self.absoluteString! as AnyObject,
                        cost: data.count)

                    
                    DispatchQueue.main.async(execute: {
                        completion(image)
                    })
                }
            }
        }
        task.resume()
    }
    
}
