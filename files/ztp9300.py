import re
import urllib2
import json
import cli

API_SERVER = "10.0.0.1"


def get_model():
    model = re.search(b"Model\sNumber\s+:\s([\-\d\w]+)\\n", cli.execute("show version"))  # noqa: W605
    model_number = re.match(b".+(\d{4})", model.groups()[0]) if model else None  # noqa: W605
    return model_number.groups()[0] if model_number else None


def get_version():
    version = re.search(b"^.*Version\s([\d\.\w]+)", cli.execute("show version"))  # noqa: W605
    return version.groups()[0] if version else None


def enable_ipxe():
    print("*** Enabling iPXE to upgrade software ***\n")
    cli.configurep(["boot ipxe timeout 30"])
    cli.executep("copy running-config startup-config")
    cli.executep("reload /noverify")


def disable_ipxe():
    print("*** Disabling iPXE ***\n")
    cli.configurep(["no boot ipxe timeout 30"])
    cli.executep("copy running-config startup-config")


def check_required(model, version):
    try:
        response = urllib2.urlopen("http://%s/api/provisioning/version/%s" % (API_SERVER, model))
        data = json.loads(response.read().decode("utf-8"))
    except urllib2.HTTPError as e:
        print(e.reason)
        return None
    except urllib2.URLError as e:
        print(e.reason)
        return None
    else:
        return data if version != data["version"] else None


def main():
    # Get model
    model = get_model()
    if model:
        print("\nModel is: %s" % model)
    # Check version
    version = get_version()
    if version:
        print("\nVersion is: %s" % version)
    # Check upgrade
    upgrade_required = check_required(model, version)
    if upgrade_required:
        print("Current software version: %s" % version)
        print("Required software version: %s" % upgrade_required["version"])
        enable_ipxe()
    # Remove iPXE
    else:
        print("Software upgrade not required")
        disable_ipxe()
    # Request config


if __name__ == "__main__":
    main()
