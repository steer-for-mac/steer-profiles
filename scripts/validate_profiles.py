#!/usr/bin/env python3
"""Validate community-authored Steer profile JSON files.

Mirrors the importer's permissive schema: only the bundle ID and at least
one binding need to land for the profile to be useful. Everything else is
optional and inherits from the user's active default profile.
"""
import json
import pathlib
import sys


def validate(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if data.get("schemaVersion") != 1:
        errors.append(f"{path}: schemaVersion must be 1")
    profile = data.get("profile")
    if not isinstance(profile, dict):
        return errors + [f"{path}: missing profile object"]

    bundle_ids = profile.get("bundleIDs")
    if not isinstance(bundle_ids, list) or not all(isinstance(item, str) for item in bundle_ids):
        errors.append(f"{path}: profile.bundleIDs must be a string array")
    elif not bundle_ids:
        errors.append(f"{path}: profile.bundleIDs must list at least one app")
    elif path.name != f"{bundle_ids[0]}.json":
        errors.append(f"{path}: filename should match first bundle ID ({bundle_ids[0]}.json)")

    layers = profile.get("layers")
    if not isinstance(layers, list):
        errors.append(f"{path}: profile.layers must be a list")
    elif len(layers) != 6:
        errors.append(f"{path}: profile.layers must contain six layer objects (got {len(layers)})")
    else:
        binding_count = sum(
            len(layer.get("bindings", {}) or {})
            for layer in layers
            if isinstance(layer, dict)
        )
        if binding_count == 0:
            errors.append(
                f"{path}: profile must define at least one binding "
                f"(empty profiles are rejected on import)"
            )

    return errors


def main() -> int:
    paths = sorted(pathlib.Path("profiles").glob("*.json"))
    if not paths:
        print("No profiles found", file=sys.stderr)
        return 0
    errors = [error for path in paths for error in validate(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} profile files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
