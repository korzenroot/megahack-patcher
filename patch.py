#!/usr/bin/python3
import re
import sys
import urllib.request
import json
import zipfile
import io

if __name__ == "__main__":
    def patch(data: bytearray, signature: bytes, patch: bytes):
        match = re.search(signature, data, re.DOTALL)
        if not match:
            print(f"Failed to find {signature.hex().upper()}")
            sys.exit(1)
        start = match.start()
        data[start:start + len(patch)] = patch
        print(f"0x{start:X} patched with {patch.hex().upper()}")

    with urllib.request.urlopen(urllib.request.Request("https://absolllute.com/api/mega_hack/v9/install.json", headers={"User-Agent": ""})) as install_json:
        versions = [bundle["version"] for package in json.load(install_json)["packages"] for bundle in package["bundles"] if bundle.get("geode")]
    if len(sys.argv) > 1:
        if sys.argv[1] in versions:
            version = sys.argv[1]
        else:
            print(versions)
            sys.exit(1)
    else:
        version = versions[0]
    print(f"- Downloading Mega Hack {version} -")
    with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(urllib.request.Request(f"https://absolllute.com/api/mega_hack/v9/files/{version}/absolllute.megahack.geode", headers={"User-Agent": ""})).read())) as original_zipfile, zipfile.ZipFile("absolllute.megahack.geode", "w") as patched_zipfile:
        print(f"Downloaded Mega Hack {version}")
        for name in original_zipfile.namelist():
            original_bytes = original_zipfile.read(name)
            if name == "mod.json":
                print("\n- Patching mod.json -")
                mod_json = json.loads(original_bytes)
                mod_json.get("dependencies", {}).pop("absolllute.installer")
                original_bytes = json.dumps(mod_json).encode()
                print("absolllute.installer dependency patched")
            # xref "LICENSE"
            elif name == "absolllute.megahack.dll":
                print("\n- Patching absolllute.megahack.dll -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\x55\x41\x57\x41\x56\x56\x57\x53\x48\x83\xEC\x48\x48\x8D\x6C\x24\x40\x48\xC7\x45\x00\xFE\xFF\xFF\xFF\xB0\x01", b"\xB8\x01\x00\x00\x00\xC3")
                original_bytes = bytes(patched_bytes)
            elif name == "absolllute.megahack.dylib":
                print("\n- Patching absolllute.megahack.dylib -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\x55\x48\x89\xE5\x41\x57\x41\x56\x41\x55\x41\x54\x53\x48\x83\xEC\x18\x41\xB7\x01", b"\xB8\x01\x00\x00\x00\xC3")
                patch(patched_bytes, rb"\xFF\x83\x01\xD1\xF8\x5F\x02\xA9\xF6\x57\x03\xA9\xF4\x4F\x04\xA9\xFD\x7B\x05\xA9\xFD\x43\x01\x91\x08\x00\x40\x39\x08\x01\x00\x36", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                original_bytes = bytes(patched_bytes)
            elif name == "absolllute.megahack.android32.so":
                print("\n- Patching absolllute.megahack.android32.so -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\xF0\xB5\x03\xAF\x4D\xF8\x04\xBD\x84\xB0\x04\x46\x21\x48\x78\x44", b"\x01\x20\x70\x47")
                original_bytes = bytes(patched_bytes)
            elif name == "absolllute.megahack.android64.so":
                print("\n- Patching absolllute.megahack.android64.so -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\xFF\x43\x01\xD1\xFD\x7B\x02\xA9\xF5\x1B\x00\xF9\xF4\x4F\x04\xA9\xFD\x83\x00\x91\x55\xD0\x3B\xD5\xA8\x16\x40\xF9\xA8\x83\x1F\xF8\x08\x00\x40\x39", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                original_bytes = bytes(patched_bytes)
            patched_zipfile.writestr(name, original_bytes)
