# Historical Google Key Response Design

Status: Completed

## Evidence

GitHub secret scanning reports one open historical Google API key alert. The
flagged credential file is absent from current `master`, and the alert validity
is unknown. The repository owner has not supplied provider-side revocation or
rotation evidence.

## Options

1. Resolve the alert as revoked without provider evidence.
2. Leave the existing README sentence unenforced.
3. Keep the alert open, ignore the retired credential filename, and enforce the
   owner-response boundary across maintained security guidance and verification.

## Decision

Use option 3. It improves current-tree prevention and maintainer clarity without
exposing the value or making an unsupported provider-side claim.

## Scope

No credential value, alert location, gameplay source, Xcode project setting,
network behavior, or repository history is changed.
