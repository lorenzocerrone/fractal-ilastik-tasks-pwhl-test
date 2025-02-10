import argparse
import shutil
from pathlib import Path
from subprocess import run
from typing import Literal

import toml


def argparser():
    parser = argparse.ArgumentParser(description="Build a pwhl file")

    parser.add_argument(
        "--mode",
        "-m",
        default="wheel",
        choices=["wheel", "pypi", "conda"],
        help=(
            "The mode to run the script in. "
            "-'wheel' will build a pwhl file that contains a wheel file. \n"
            "-'pypi' will build a pwhl file that contains pypi dependencies. \n"
        ),
    )
    parser.add_argument(
        "--dist-dir",
        "-d",
        default="dist",
        help="The directory to build and store the pwhl file",
    )

    return parser.parse_args()


def setup_dirs(dist: str | Path = "dist"):
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(exist_ok=True)


def hatch_build(dist: str | Path = "dist"):
    # This step shoul be generic and should be
    # able to build using any build tool
    out = run(["hatch", "build", dist], capture_output=True)
    if out.returncode != 0:
        raise Exception(out.stderr.decode())


def get_wheel_file(dist: str | Path) -> Path:
    # get the wheel file path
    wheel_file = list(dist.glob("*.whl"))
    if len(wheel_file) == 0:
        raise Exception("No wheel file found")

    if len(wheel_file) > 1:
        raise Exception("Multiple wheel files found, only one expected")

    wheel_file = wheel_file[0]
    print(f"wheel file: {wheel_file}")
    return wheel_file


def derive_pyproject(wheel_path: Path, pweel_dir: Path) -> None:
    # read the pyproject.toml file
    with open("pyproject.toml", "r") as f:
        data = toml.load(f)

    if "tool" not in data:
        raise Exception("No tool section found in pyproject.toml")

    if "pixi" not in data["tool"]:
        raise Exception("No pixi section found in pyproject.toml")

    if "pypi-dependencies" not in data["tool"]["pixi"]:
        raise Exception("No pypi-dependencies section found in pyproject.toml")

    keys = data["tool"]["pixi"]["pypi-dependencies"].keys()

    if len(keys) == 0:
        raise Exception("No wheel dependencies found")

    if len(keys) > 1:
        raise Exception("Multiple wheel dependencies found, only one expected")

    key = next(iter(keys))

    data["tool"]["pixi"]["pypi-dependencies"][key] = {"path": str(wheel_path.name)}

    pwhl_pyproject = pweel_dir / "pyproject.toml"
    with open(pwhl_pyproject, "w") as f:
        toml.dump(data, f)


def compress_pwhl(new_dir: Path):
    new_pwhl = new_dir.with_suffix(".pwhl")
    shutil.make_archive(new_pwhl, "zip", new_dir)


def build_pwhl(dist: str | Path = "dist", mode: Literal["wheel", "pypi"] = "wheel"):
    """Build a pwhl file

    This function builds a pwhl that can be used to build a standalone python environment
    using the pixi tool.

    The pwhl file is a zip file with the extension .pwhl.zip that contains:
    - A pyproject.toml file that specifies all conda and pipy dependencies and optionally
        a path to a wheel file in the pypi-dependencies section.
    - Optionally a wheel file that is specified in the pypi-dependencies section of the pyproject.toml file.

    """
    if mode == "pypi":
        raise NotImplementedError("pypi mode not implemented")

    dist = Path(dist)
    setup_dirs(dist)

    hatch_build(dist)

    wheel_path = get_wheel_file(dist)

    pweel_dir = dist / wheel_path.stem
    pweel_dir.mkdir(exist_ok=True)

    # copy the wheel file to the pweel directory
    shutil.copy(wheel_path, pweel_dir)

    derive_pyproject(wheel_path, pweel_dir)

    compress_pwhl(pweel_dir)

    print("pweel build complete")


if __name__ == "__main__":
    args = argparser()
    build_pwhl()
