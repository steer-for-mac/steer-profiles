#!/usr/bin/env python3
import json
import pathlib
import sys


REQUIRED_PROFILE_KEYS = {
    "id",
    "name",
    "bundleIDs",
    "layers",
    "stick",
    "touchpad",
    "gyro",
    "haptics",
    "triggers",
    "led",
    "radialMenu",
}


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

    missing = sorted(REQUIRED_PROFILE_KEYS - profile.keys())
    if missing:
        errors.append(f"{path}: profile missing keys: {', '.join(missing)}")
    bundle_ids = profile.get("bundleIDs")
    if not isinstance(bundle_ids, list) or not all(isinstance(item, str) for item in bundle_ids):
        errors.append(f"{path}: profile.bundleIDs must be a string array")
    if bundle_ids and path.name != f"{bundle_ids[0]}.json":
        errors.append(f"{path}: filename should match first bundle ID")
    layers = profile.get("layers")
    if not isinstance(layers, list) or len(layers) != 6:
        errors.append(f"{path}: profile.layers must contain six layer objects")
    return errors


def main() -> int:
    paths = sorted(pathlib.Path("profiles").glob("*.json"))
    if not paths:
        print("No profiles found", file=sys.stderr)
        return 1
    errors = [error for path in paths for error in validate(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} profile files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

