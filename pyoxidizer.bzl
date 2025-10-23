# PyOxidizer configuration for building markitdown standalone binary

def make_exe():
    dist = default_python_distribution()

    # Use a custom build script to control what resources are included
    policy = dist.make_python_packaging_policy()

    # Include all necessary file resources
    policy.resources_location_fallback = "filesystem-relative:lib"
    policy.allow_files = True
    policy.file_scanner_emit_files = True
    policy.include_distribution_sources = False
    policy.include_distribution_resources = False
    policy.include_test = False

    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "from markitdown.__main__ import main; main()"
    python_config.filesystem_importer = True

    # Create the Python executable with the markitdown package
    exe = dist.to_python_executable(
        name="markitdown",
        packaging_policy=policy,
        config=python_config,
    )

    # Add markitdown package from the submodule
    exe.add_python_resources(exe.pip_install([
        "./markitdown/packages/markitdown[all]"
    ]))

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)

resolve_targets()
