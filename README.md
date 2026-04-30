# Steer Profiles

Community-curated controller profiles for popular Mac apps.

This repo is empty for now — early seeds were stubs that imported as no-op profiles. Real bindings will land here as the [Steer](https://github.com/steer-for-mac/steer) beta widens; in the meantime, contributions are welcome.

## Import a Profile

In Steer: **Settings → Profiles → Import from URL** (link icon in the bottom toolbar). Paste the GitHub link to any `.json` file under `profiles/` — Steer rewrites `github.com/.../blob/...` URLs to fetch the raw file.

## Contribute

Profiles are sparse: include only the fields you intend to override. Steer fills in everything else from the active default. A minimum-useful profile is just a bundle ID and one or more bindings:

```json
{
  "schemaVersion": 1,
  "profile": {
    "name": "Safari",
    "bundleIDs": ["com.apple.Safari"],
    "layers": [
      {
        "bindings": {
          "circle": { "tap": { "primary": { "key": "w", "modifiers": ["cmd"] } } }
        }
      },
      {}, {}, {}, {}, {}
    ]
  }
}
```

The six `layers` slots map to Solo, L1, R1, L1+R1, L2-hold, R2-hold. Empty `{}` entries inherit Default.

Steer rejects profiles with zero bindings on import — the validation workflow does the same on PR.

### Workflow

1. Fork this repo.
2. Add one `.json` file per app under `profiles/`. Filename should match the first bundle ID (`com.apple.Safari.json`).
3. `python3 scripts/validate_profiles.py` to check locally.
4. Open a pull request.

### Tips

- Look at how other apps map controllers for inspiration: [NSEvent/xbox-controller-mapper](https://github.com/NSEvent/xbox-controller-mapper), AntiMicroX, JoyToKey configs. Translate the action shapes; don't copy raw mappings.
- Keep bindings to actions that make sense without a controller (Cmd+W, Cmd+T, scrolling) — exotic chords age poorly.
- The importer ignores unknown top-level keys, so feel free to add metadata fields the validator doesn't yet understand.
