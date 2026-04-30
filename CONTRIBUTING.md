# Contributing Profiles

Profiles use Steer's `.steerprofile` JSON document format: a `SteerProfileDocument` wrapper with a `profile` payload matching Steer's `Profile` `Codable` definition.

File names should match the app bundle ID, for example:

```text
profiles/com.apple.Safari.json
profiles/com.figma.Desktop.json
```

Keep profiles focused on one app, include the target bundle ID in `profile.bundleIDs`, and prefer clear bindings over personal workflow quirks. A typical pull request adds or updates one profile file and explains which app version and controller were used while testing.

