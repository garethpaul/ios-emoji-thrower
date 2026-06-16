import Foundation

private var failureCount = 0

private func expectNil(_ value: CGPoint?, _ message: String) {
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
expectNil(ProjectileMath.direction(offset: .zero), "zero-length offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: -1.0, y: 0.0)), "backward offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: .nan, y: 1.0)), "NaN horizontal offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: 1.0, y: .nan)), "NaN vertical offsets are rejected")
expectNil(ProjectileMath.direction(offset: CGPoint(x: .infinity, y: 1.0)), "infinite offsets are rejected")
expectNil(
    ProjectileMath.direction(offset: CGPoint(x: CGFloat.greatestFiniteMagnitude, y: CGFloat.greatestFiniteMagnitude)),
    "overflowing vector lengths are rejected"
)

if failureCount > 0 {
    exit(1)
}

print("ProjectileMath behavioral tests passed")
