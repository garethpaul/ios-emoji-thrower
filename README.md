# EmojiThrower

This legacy branch uses Firebase and TwitterKit. It does not include working
provider configuration.

Before building:

1. Download a Firebase configuration for your own iOS application and save it
   as `EmojiThrower/GoogleService-Info.plist`.
2. Copy `EmojiThrower/Config.plist.example` to
   `EmojiThrower/Config.plist` and replace both placeholders with your own
   Twitter consumer credentials.
3. Run `python3 scripts/config_security.py validate-local --root .`.

Both live files are ignored by Git. The Xcode target runs the same validator
before its Resources phase, so a missing or placeholder configuration fails
the build rather than producing a broken application bundle. Do not add the
live files or real provider values to commits.

Firebase client configuration contains public project and application
identifiers rather than a server authorization secret. Restrict the associated
API key to the expected iOS bundle ID and required APIs, and protect Firebase
data with Security Rules and App Check. Twitter consumer secrets are
credentials and must be kept private.

Removing files from the branch tip does not remove them from Git history or
revoke provider-side access. Rotate the historical Twitter credentials, review
provider activity, and review the Firebase key restrictions and data-access
rules in the provider consoles.

Run `make check` to execute the repository security contract. This branch is a
Swift 3/CocoaPods-era snapshot; the check parses the project but does not claim
that current Xcode can compile the application or its retired dependencies.
