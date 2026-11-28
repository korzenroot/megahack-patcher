#!/usr/bin/python3
import re
import urllib.request
import json
import zipfile
import io
import sys
from pathlib import Path
import shutil

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
            if name == "absolllute.megahack.dll":
                print("\n- Patching absolllute.megahack.dll -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\x55\x41\x56\x56\x57\x53\x48\x83\xEC\x70\x48\x8D\x6C\x24\x70\x48\xC7\x45\xF8\xFE\xFF\xFF\xFF\x48\x83\x39\x00", b"\xB8\x01\x00\x00\x00\xC3")
                patch(patched_bytes, rb"\x56\x57\x48\x83\xEC\x48\x48\x83\x79\x10\x40", b"\xB8\x01\x00\x00\x00\xC3")
                patch(patched_bytes, rb"\x55\x41\x57\x41\x56\x56\x57\x53\x48\x81\xEC\x48\x01\x00\x00\x48\x8D\xAC\x24\x80\x00\x00\x00\x48\xC7\x85\xC0\x00\x00\x00\xFE\xFF\xFF\xFF\x48\x89\xD7", b"\xC3")
                original_bytes = bytes(patched_bytes)
            if name == "absolllute.megahack.dylib":
                print("\n- Patching absolllute.megahack.dylib -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\xFF\x83\x01\xD1\xF6\x57\x03\xA9\xF4\x4F\x04\xA9\xFD\x7B\x05\xA9\xFD\x43\x01\x91\x08\x00\x40\xF9", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                patch(patched_bytes, rb"\x08\x5C\x40\x39\x09\x1D\x00\x13\x0A\x04\x40\xF9\x3F\x01\x00\x71\x48\xB1\x88\x9A\x1F\x01\x01\xF1\x21\x04\x00\x54", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                patch(patched_bytes, rb"\xFC\x6F\xBA\xA9\xFA\x67\x01\xA9\xF8\x5F\x02\xA9\xF6\x57\x03\xA9\xF4\x4F\x04\xA9\xFD\x7B\x05\xA9\xFD\x43\x01\x91\xFF\x83\x08\xD1\xF4\x03\x01\xAA", b"\xC0\x03\x5F\xD6")
                patch(patched_bytes, rb"\x55\x48\x89\xE5\x41\x57\x41\x56\x41\x54\x53\x48\x83\xEC\x30\x48\x83\x3F\x00", b"\xB8\x01\x00\x00\x00\xC3")
                patch(patched_bytes, rb"\x55\x48\x89\xE5\x53\x48\x83\xEC\x18\x48\x89\xFB\x0F\xB6\x07", b"\xB8\x01\x00\x00\x00\xC3")
                patch(patched_bytes, rb"\x55\x48\x89\xE5\x41\x57\x41\x56\x41\x55\x41\x54\x53\x48\x81\xEC....\x49\x89\xF6\x49\x89\xFF\x48\x8B\x05", b"\xC3")
                original_bytes = bytes(patched_bytes)
            if name == "absolllute.megahack.android32.so":
                print("\n- Patching absolllute.megahack.android32.so -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\xF0\xB5\x03\xAF\x4D\xF8\x04\x8D\x88\xB0\x04\x46\x83\x48", b"\x01\x20\x70\x47")
                patch(patched_bytes, rb"\xF0\xB5\x03\xAF\x4D\xF8\x04\x8D\x84\xB0\x04\x46\x24\x48", b"\x01\x20\x70\x47")
                patch(patched_bytes, rb"\xF0\xB5\x03\xAF\x2D\xE9\x00\x0F\x81\xB0\x2D\xED\x04\x8B\xEE\xB0", b"\x70\x47")
                original_bytes = bytes(patched_bytes)
            if name == "absolllute.megahack.android64.so":
                print("\n- Patching absolllute.megahack.android64.so -")
                patched_bytes = bytearray(original_bytes)
                patch(patched_bytes, rb"\xFF\xC3\x01\xD1\xFD\x7B\x03\xA9\xF7\x23\x00\xF9\xF6\x57\x05\xA9\xF4\x4F\x06\xA9\xFD\xC3\x00\x91\x57\xD0\x3B\xD5\xE8\x16\x40\xF9\xA8\x83\x1F\xF8\x08\x00\x40\xF9", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                patch(patched_bytes, rb"\xFF\x43\x01\xD1\xFD\x7B\x02\xA9\xF5\x1B\x00\xF9\xF4\x4F\x04\xA9\xFD\x83\x00\x91\x54\xD0\x3B\xD5\x88\x16\x40\xF9\xA8\x83\x1F\xF8\x08\x00\x40\x39", b"\x20\x00\x80\x52\xC0\x03\x5F\xD6")
                patch(patched_bytes, rb"\xFD\x7B\xBA\xA9\xFC\x6F\x01\xA9\xFA\x67\x02\xA9\xF8\x5F\x03\xA9\xF6\x57\x04\xA9\xF4\x4F\x05\xA9\xFD\x03\x00\x91\xFF\xC3\x08\xD1\x59\xD0\x3B\xD5", b"\xC0\x03\x5F\xD6")
                original_bytes = bytes(patched_bytes)
            patched_zipfile.writestr(name, original_bytes)

    print("\n- Creating license -")
    #json.dumps({"data": base64.b64encode(json.dumps({"id": "", "guid2": "0E841FA5BFE5CE8FC91EB11ADD1DCEF694045BEEAFCF521BF4341D3997C1C219"}).encode()).decode(), "sig": "", "token": ""})
    with open("license", "wb") as license_file:
        license_file.write(b'{"data":"eyJpZCI6ICIiLCAiZ3VpZDIiOiAiMEU4NDFGQTVCRkU1Q0U4RkM5MUVCMTFBREQxRENFRjY5NDA0NUJFRUFGQ0Y1MjFCRjQzNDFEMzk5N0MxQzIxOSJ9","sig":"","token":""}')
        print("Created license")

    print(f"\n- Installing patched Mega Hack {version} -")
    for geometrydash_exe_path in Path.home().rglob("GeometryDash.exe"):
        geode_mods_path = geometrydash_exe_path.parent / "geode/mods"
        geode_mods_path.mkdir(parents=True, exist_ok=True)
        shutil.copy("absolllute.megahack.geode", geode_mods_path)
        print(f"Copied patched Mega Hack {version} to {geode_mods_path}")

    for appdata_local_geometrydash_path in Path.home().rglob("AppData/Local/GeometryDash"):
        absolllute_megahack_path = appdata_local_geometrydash_path.parent / "absolllute.megahack"
        absolllute_megahack_path.mkdir(parents=True, exist_ok=True)
        shutil.copy("license", absolllute_megahack_path)
        print(f"Copied license to {absolllute_megahack_path}")
