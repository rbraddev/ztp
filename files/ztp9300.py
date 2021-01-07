import re
import cli


def get_model():
    model = re.search(b"Model\sNumber\s+:\s([\-\d\w]+)\\n", cli.execute("show version"))  # noqa: W605
    model_number = re.match(b".+(\d{4})", model.groups()[0]) if model else None  # noqa: W605
    return model_number.groups()[0] if model_number else None


def get_version():
    version = re.search(b"^.*Version\s([\d\.\w]+)", cli.execute("show version"))  # noqa: W605
    return version.groups()[0] if version else None


def enable_ipxe():
    cli.configurep(["boot ipxe timeout 30"])
    cli.executep("copy running-config startup-config")
    cli.executep("reload /noverify")


def main():
    # Get model
    model = get_model()
    if model:
        print("Model is: %s" % model)
    # Check version
    version = get_version()
    if version:
        print("Version is: %s" % version)
    # Check upgrade

    # Remove iPXE

    # Request config


if __name__ == "__main__":
    main()
