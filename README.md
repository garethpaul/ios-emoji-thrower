# EmojiThrower

This branch uses Firebase for application configuration. Before building,
download a Firebase configuration for your own restricted iOS application and
place it at `EmojiThrower/GoogleService-Info.plist`.

The configuration file is intentionally ignored by Git and must not be
committed. Restrict the associated API key to the expected iOS bundle ID and
the minimum APIs required by the application.
