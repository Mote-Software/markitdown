# PyOxidizer configuration for building markitdown standalone binary

def make_exe():
    dist = default_python_distribution()

    # Configure packaging policy
    policy = dist.make_python_packaging_policy()

    # Include standard library modules in-memory for reliable initialization
    policy.resources_location = "in-memory"
    policy.resources_location_fallback = "filesystem-relative:lib"

    # Allow file resources which some packages need
    policy.allow_files = True
    policy.file_scanner_emit_files = True

    # Exclude unnecessary files to reduce size
    policy.include_distribution_sources = False
    policy.include_test = False

    # But include distribution resources (needed for some packages)
    policy.include_distribution_resources = True

    # Configure Python interpreter
    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "from markitdown.__main__ import main; main()"

    # Enable filesystem importer for data files
    python_config.filesystem_importer = True

    # Set proper encoding to avoid initialization errors
    python_config.filesystem_encoding = "utf-8"
    python_config.utf8_mode = True

    # Create the Python executable
    exe = dist.to_python_executable(
        name="markitdown",
        packaging_policy=policy,
        config=python_config,
    )

    # Add standard library - critical for proper initialization
    # This ensures encodings and codecs modules are available
    for resource in dist.python_resources():
        # Include all standard library modules
        if resource.is_stdlib:
            exe.add_python_resource(resource)

    # Install markitdown package and all its dependencies
    # Note: markitdown should be pre-installed in the environment
    for resource in exe.pip_install(["markitdown"]):
        exe.add_python_resource(resource)

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
