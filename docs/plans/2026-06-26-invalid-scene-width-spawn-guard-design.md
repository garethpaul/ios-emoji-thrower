# Invalid Scene Width Spawn Guard Design

Status: Completed

## Problem

`monsterSpawnY` rejects unusable vertical geometry before `addMonster` creates a
node, but `addMonster` also uses `size.width` to derive the monster's off-screen
x position. A transient zero, negative, NaN, or infinite width can therefore
pass the helper and create a monster with unusable horizontal geometry.

## Options

1. Validate width after adding the node. This permits invalid scene mutation.
2. Add a separate width guard in `addMonster`. This splits spawn geometry
   authority across two locations.
3. Extend the existing optional spawn-geometry helper to reject invalid width
   before returning a valid y coordinate.

## Decision

Use option 3. Preserve normal spawn cadence, random vertical placement, speed,
physics, scoring, and assets while keeping all scene-geometry admission ahead
of node insertion.
