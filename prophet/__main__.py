import json
import logging

log = logging.getLogger(__file__)


def main():
    log.info("Creating the model file")
    model_path = "/valohai/outputs/model.txt"
    with open(model_path, "w") as fp:
        fp.write("This is my model.")
    log.info(f"Model file created: {model_path}")

    log.info("Creating the model file metadata")
    metadata = {"valohai.model-versions": [{
        "model_uri": "model://unicorns/",
        "model_version_tags": ["red", "blue", "green", "yellow", "pink"],
        "model_release_note": "100% freshly squeezed unicorn juice 🍋🦄",
    }]}
    metadata_path = f"{model_path}.metadata.json"
    with open(metadata_path, "w") as fp:
        json.dump(metadata, fp)
    log.info(f"Model metadata file created: {metadata_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
