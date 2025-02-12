# Test task for Pixi-based fractal task collection

Scope of this test is to prototype a pixi-based task collection for fractal tasks.
The goal is to create reproducible environments that require a mix of pypi, conda and wheel packages.

## Requirements to run the test

* pixi

## Build a .pwhl.zip file

A `.pwhl.zip` file is a zip file that contains the modified pyproject.toml file (maybe the lock) and the wheel file for the task package.
The `pytproject.toml` in a pixi project typically has the source code specified in the `[tool.pixi.pypi-dependencies]` section.

```toml
[tool.pixi.pypi-dependencies]
ilastik-tasks = { path = ".", editable = true }
```

and the modified `pyproject.toml` file will have the wheel file in the `[tool.pixi.pypi-dependencies]` section.

```toml
[tool.pixi.pypi-dependencies]
ilastik-tasks = { path = "ilastik-tasks-0.1.0-py3-none-any.whl" }
```

```bash
pixi run -e dev python build_pwhl.py
```

## Create a pixi environment

```bash
bash 1_2_3_create_pixi_env.sh
```

Variables in the script:

* `PACKAGE_ENV_DIR`: The directory where the environment will be created
* `PWHL_PATH`: The path to the .pwhl.zip file
* `ENV_EXTRA`: The extra to install in the environment (if any like dev, test, task-core). If none are required, set it to `default`.

## Run the a test to check if the python env is created correctly

```bash
bash run_pixi_env_python.sh
```

Running any python script in the environment:

```bash
pixi run --manifest-path ./pwhl_env/pyproject.toml -e dev python script.py
```

## Reinstall the environment

* Remove the environment

```bash
rm -rf pwhl_env/.pixi  
```

* Reinstall the environment from frozen pixi.lock

```bash
bash 6_reinstall_pixi_env.sh
```
