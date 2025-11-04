import json
import logging
import random
import sys
from pathlib import Path

import valohai

log = logging.getLogger(__file__)


def main() -> None:
    image_dir = Path(valohai.inputs(name="images").dir_path())
    if not image_dir.exists() or not any(image_dir.iterdir()):
        log.error("No images found!")
        return

    # find png images without __ in the name:
    base_images = [p for p in image_dir.glob("*__base.png")]

    for base_img in base_images:
        identity = base_img.stem.replace("__base", "")
        truth_img = image_dir / f"{identity}__truth.png"
        if not truth_img.exists():
            log.warning(f"No ground truth found for {base_img.name}")
            continue

        # find images for this identity that don't end in __base or __truth
        prediction_images = [
            p
            for p in image_dir.glob(f"{identity}__*.png")
            if not p.name.endswith("__base.png") and not p.name.endswith("__truth.png")
        ]
        if not prediction_images:
            log.warning(f"No prediction images found for {identity}")
            continue

        # keep index around
        for idx, pred_img in enumerate([*prediction_images, base_img, truth_img]):
            if pred_img.name in (base_img.name, truth_img.name):
                new_stem = pred_img.stem
                filename = pred_img.name
            else:
                # for output filename, remove everything after first __ and add random number
                random_part = f"{random.randint(0, 99999):04d}"
                new_stem = f"{identity}__{random_part}"
                filename = f"{new_stem}.png"

            metadata = {
                "vhic_group": "person/woman",
                "vhic_base": base_img.name,
                "vhic_truth": truth_img.name,
                "vhic_name": new_stem.upper(),
                "vhic_blend": "screen",
                "vhic_color": "red",
            }

            output_path = Path(valohai.outputs().path(filename))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(pred_img.read_bytes())

            metadata_path = valohai.outputs().path(f"{filename}.metadata.json")
            with open(metadata_path, "w") as fp:
                json.dump(metadata, fp)


def cli() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
