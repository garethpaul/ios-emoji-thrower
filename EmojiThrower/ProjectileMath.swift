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

    static func exitDistance(sceneSize: CGSize, projectileSize: CGSize) -> CGFloat? {
        guard sceneSize.width.isFinite, sceneSize.height.isFinite,
              sceneSize.width > 0, sceneSize.height > 0,
              projectileSize.width.isFinite, projectileSize.height.isFinite,
              projectileSize.width >= 0, projectileSize.height >= 0 else {
            return nil
        }

        let sceneDiagonal = hypot(sceneSize.width, sceneSize.height)
        let projectileClearance = max(projectileSize.width, projectileSize.height)
        let distance = sceneDiagonal + projectileClearance
        guard sceneDiagonal.isFinite, distance.isFinite, distance > 0 else {
            return nil
        }

        return distance
    }
}
