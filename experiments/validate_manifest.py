from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from experiments.models import load_manifest
from experiments.storage import file_sha256


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a pilot program manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
    except (OSError, ValueError, ValidationError) as exc:
        print(f"invalid manifest: {exc}")
        raise SystemExit(1) from exc
    print(
        json.dumps(
            {
                "valid": True,
                "manifest_sha256": file_sha256(args.manifest),
                "dataset_name": manifest.dataset_name,
                "total_records": len(manifest.programs),
                "included_records": len(manifest.included),
                "excluded_records": len(manifest.programs) - len(manifest.included),
                "selection_frozen_at": manifest.selection_frozen_at.isoformat(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
