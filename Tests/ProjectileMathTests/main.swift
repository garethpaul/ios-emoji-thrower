import Foundation

private var failureCount = 0

private func expectNil<T>(_ value: T?, _ message: String) {
    if value != nil {
        failureCount += 1
        fputs("FAIL: \(message): expected nil\n", stderr)
    }
}

private func expectPoint(
    _ actual: CGPoint?,
    x expectedX: CGFloat,
    y expectedY: CGFloat,
    accuracy: CGFloat = 0.000_001,
    _ message: String
) {
    guard let actual else {
        failureCount += 1
        fputs("FAIL: \(message): expected a direction\n", stderr)
        return
    }
    if !actual.x.isFinite || !actual.y.isFinite ||
        abs(actual.x - expectedX) > accuracy || abs(actual.y - expectedY) > accuracy {
        failureCount += 1
        fputs("FAIL: \(message): expected (\(expectedX), \(expectedY)), got (\(actual.x), \(actual.y))\n", stderr)
    }
}

private func expectDistance(
    _ actual: CGFloat?,
    _ expected: CGFloat,
    accuracy: CGFloat = 0.000_001,
    _ message: String
) {
    guard let actual else {
        failureCount += 1
        fputs("FAIL: \(message): expected a distance\n", stderr)
        return
    }
    if !actual.isFinite || abs(actual - expected) > accuracy {
        failureCount += 1
        fputs("FAIL: \(message): expected \(expected), got \(actual)\n", stderr)
    }
}

expectPoint(
    ProjectileMath.direction(offset: CGPoint(x: 3.0, y: 4.0)),
    x: 0.6,
    y: 0.8,
    "finite forward offsets normalize to unit direction"
)
expectPoint(
    ProjectileMath.direction(offset: CGPoint(x: 3.0, y: -4.0)),
    x: 0.6,
    y: -0.8,
    "negative vertical offsets preserve direction"
)
expectNil(
    ProjectileMath.direction(offset: CGPoint(x: 0.0, y: 0.0)),
    "zero-length offsets are rejected"
)
expectNil(ProjectileMath.direction(offset: CGPoint(x: -1.0, y: 0.0)), "backward offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: .nan, y: 1.0)), "NaN horizontal offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: 1.0, y: .nan)), "NaN vertical offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: .infinity, y: 1.0)), "infinite offsets are rejected")
expectNil(
    ProjectileMath.direction(offset: CGPoint(x: CGFloat.greatestFiniteMagnitude, y: CGFloat.greatestFiniteMagnitude)),
    "overflowing vector lengths are rejected"
)

expectDistance(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 1366.0, height: 1024.0),
        projectileSize: CGSize(width: 40.0, height: 30.0)
    ),
    hypot(1366.0, 1024.0) + 40.0,
    "wide scenes use their diagonal plus projectile clearance"
)
expectDistance(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 768.0, height: 1366.0),
        projectileSize: CGSize(width: 20.0, height: 60.0)
    ),
    hypot(768.0, 1366.0) + 60.0,
    "tall scenes use their diagonal plus the largest projectile dimension"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 0.0, height: 1024.0),
        projectileSize: CGSize(width: 40.0, height: 30.0)
    ),
    "zero-width scenes are rejected"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 1366.0, height: -1.0),
        projectileSize: CGSize(width: 40.0, height: 30.0)
    ),
    "negative scene dimensions are rejected"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: .nan, height: 1024.0),
        projectileSize: CGSize(width: 40.0, height: 30.0)
    ),
    "non-finite scene dimensions are rejected"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 1366.0, height: 1024.0),
        projectileSize: CGSize(width: -1.0, height: 30.0)
    ),
    "negative projectile dimensions are rejected"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: 1366.0, height: 1024.0),
        projectileSize: CGSize(width: .infinity, height: 30.0)
    ),
    "non-finite projectile dimensions are rejected"
)
expectNil(
    ProjectileMath.exitDistance(
        sceneSize: CGSize(width: CGFloat.greatestFiniteMagnitude, height: CGFloat.greatestFiniteMagnitude),
        projectileSize: CGSize(width: CGFloat.greatestFiniteMagnitude, height: CGFloat.greatestFiniteMagnitude)
    ),
    "overflowing exit distances are rejected"
)

if failureCount > 0 {
    exit(1)
}

print("ProjectileMath behavioral tests passed")
