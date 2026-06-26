# Resize-Safe Game Over Design

Status: Completed

## Problem

`GameOverScene` creates a local label at its initial center and captures the
initial size for its delayed restart. If `.resizeFill` changes the scene during
the result delay, the label stays at the old center and the restart begins with
stale geometry.

## Options

1. Keep initial geometry for the short result delay.
2. Recenter only the label while retaining the captured restart size.
3. Own the label as scene state, relayout from `didChangeSize(_:)`, and read `self.size` when the delayed restart fires.

## Decision

Use option 3 so all game-over geometry comes from the current scene while
preserving the existing delay, transition, and active-scene restart guard.
