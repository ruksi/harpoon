# Harpoon

> just a bit of whaling on the Pacific Ocean 🐋

A debug repository for [Valohai](https://valohai.com/), nothing to see here.

## TL;DR

```bash
mise install
```

Then, you can run the various tools locally; results will be on `.valohai` dir.

```bash
# batman - Datum Alias Testing
uv run batman

# genesis - Datasets and Dataset Versions
uv run genesis

# mech - Execution Metadata
uv run mech --beep-count 5 --boop-count 5

# prism - Image Comparison
# NB: needs images in .valohai/inputs
uv run prism

# prophet - Models and Model Versions
uv run prophet --model-uri [FILL-ME]

# ship - Deployment Testing
uv run ship ahoy  # prints AHOY every 3 seconds
uv run ship flaky # prints AHOY? every 3 seconds with 10% chance of crashing
```

There are various other debugging flows in `valohai.yaml` too

## Debugging Valohai CLI

```bash
uv pip install -e /path/to/local/valohai-cli
# how `vh` points to the local copy
```
