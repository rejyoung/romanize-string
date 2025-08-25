import subprocess, sys, os
from pathlib import Path


def create_data_dirs(base_dir: Path):
    # define all desired directories relative to base_dir
    dirs = [
        base_dir / "data" / "raw",
        base_dir / "data" / "intermediate",
        base_dir / "data" / "processed" / "split",
        base_dir / "data" / "processed" / "vectorized",
        base_dir / "data" / "processed" / "augmented",
        base_dir / "model_assets" / "models",
        base_dir / "model_assets" / "vectorizers",
        base_dir / "model_assets" / "tell_lists"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Ensured folder exists: {d}")

    parent_dir = base_dir.parent
    model_assets = parent_dir / "model_assets"
    model_assets.mkdir(exist_ok=True)
    print(f"Ensured folder exists: {model_assets}")

    return model_assets


def train_model(model_dir: Path):
    datasets = [
        "family",
        "perso_arabic",
        "cyrillic",
        "indic",
        "ja_zh",
        "eastern_slavic",
        "southern_slavic",
        "turkic",
    ]

    python_root = Path(__file__).resolve().parent.parent  # .../python
    env = os.environ.copy()
    env["PYTHONPATH"] = str(python_root)

    for script in [
        "create_datasets.py",
        "prepare_datasets.py",
        "vectorize_training_data.py",
        "split_data.py",
        "train_model.py",
        "run_test_data.py",
    ]:
        if script == "create_datasets.py":
            subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).parent / "training_steps" / script),
                ],
                check=True,
                cwd=str(python_root),
                env=env,
            )
        else:
            for d in datasets:
                subprocess.run(
                    [
                        sys.executable,
                        str(Path(__file__).parent / "training_steps" / script),
                        d,
                        *(
                            [model_dir]
                            if script
                            in [
                                "train_data.py",
                                "vectorize_training_data.py",
                                "run_test_data.py",
                            ]
                            else []
                        ),
                    ],
                    check=True,
                    cwd=str(python_root),
                    env=env,
                )


if __name__ == "__main__":
    # parent folder of this script
    script_parent = Path(__file__).resolve().parent
    model_dir = create_data_dirs(script_parent)
    train_model(model_dir)
