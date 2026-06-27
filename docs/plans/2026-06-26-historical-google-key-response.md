# Historical Google Key Response Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Preserve the unresolved historical Google API key response boundary and prevent the retired credential file from being committed again.

**Architecture:** The static baseline owns the repository contract. It requires the ignored credential filename, completed response evidence, and identical owner-action guidance in maintained security documents while leaving provider-side resolution outside the repository.

**Tech Stack:** Python 3 static verifier, Markdown guidance, gitignore.

status: completed

---

### Task 1: Add the failing security contract

**Files:**
- Modify: `scripts/check-baseline.py`

**Step 1: Write the failing test**

Require the response plan, the ignored `GoogleService-Info.plist` filename, and
owner-action guidance in README, SECURITY, AGENTS, and CHANGES.

**Step 2: Run test to verify it fails**

Run: `make check`
Expected: FAIL because the ignore entry and maintained guidance are missing.

### Task 2: Implement the minimal repository response

**Files:**
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `SECURITY.md`
- Modify: `CHANGES.md`
- Verify: `README.md`

**Step 1: Add the ignored retired filename**

Add `GoogleService-Info.plist` without adding a credential template because the
current local game needs no Google integration.

**Step 2: Synchronize owner-action guidance**

State that the historical alert remains open until the credential owner verifies
provider-side revocation or rotation. Do not publish the value or claim the
provider action occurred.

### Task 3: Verify and close the plan

**Files:**
- Modify: `docs/plans/2026-06-26-historical-google-key-response.md`

**Step 1: Run focused and full gates**

Run: `make check`
Expected: PASS after marking the plan completed with actual verification.

Run: `/usr/bin/make -C /tmp -f "$PWD/Makefile" check`
Expected: PASS from an external caller directory.

Run: `git diff --check`
Expected: PASS.

**Step 2: Commit**

Commit the focused security response and open a pull request for exact-head
hosted validation and review.

## Verification Completed

- Red-first `make check` failed on the missing ignored credential filename,
  maintained owner-response guidance, and completed plan evidence.
- After implementation, all four Make aliases passed the static SpriteKit gate.
- External-directory `make check` passed through the absolute Makefile path.
- Two isolated hostile mutations were rejected: removing the ignored credential
  filename and removing the security-policy response sentence.
- Python AST parsing, shell syntax, and `git diff --check` passed.
- Local `swiftc` and `xcodebuild` were unavailable; hosted macOS remains the
  native compilation authority.
- Provider-side revocation or rotation remains an owner-only blocker and was not
  claimed or used to resolve the open alert.
