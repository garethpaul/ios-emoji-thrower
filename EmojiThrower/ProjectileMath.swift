import Foundation

enum ProjectileMath {
    static func direction(offset: CGPoint) -> CGPoint? {
        guard offset.x.isFinite, offset.y.isFinite, offset.x > 0 else {
            return nil
        }

        let offsetLength = sqrt(offset.x * offset.x + offset.y * offset.y)
        guard offsetLength.isFinite, offsetLength > 0 else {
            return nil
        }

        let direction = CGPoint(x: offset.x / offsetLength, y: offset.y / offsetLength)
        guard direction.x.isFinite, direction.y.isFinite else {
            return nil
        }

        return direction
    }
}
