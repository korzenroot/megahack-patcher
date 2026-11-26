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
            file = original_zipfile.read(name)
            if name == "absolllute.megahack.dll":
                print(f"\n- Patching Mega Hack {version} -")
                data = bytearray(file)
                # xref "LICENSE" 55 56 57 48 81 EC 80 01 00 00 48 8D AC 24 80 00 00 00 48 C7 85 F8 00 00 00 FE FF FF FF 48 89 D6
                patch(data, rb"\x55\x41\x56\x56\x57\x53\x48\x83\xEC\x70\x48\x8D\x6C\x24\x70\x48\xC7\x45\xF8\xFE\xFF\xFF\xFF\x48\x83\x39\x00", b"\xB8\x01\x00\x00\x00\xC3")
                # caller 56 57 53 48 83 EC 40 48 89 CE 48 8B 05 ? ? ? ? 48 31 E0 48 89 44 24 38 0F 57 C0
                patch(data, rb"\xE8....\x48\x83\x7F\x18\x10\x72", b"\xB8\x00\x00\x00\x00")
                patch(data, rb"\x56\x57\x48\x83\xEC\x48\x48\x83\x79\x10\x40", b"\xB8\x01\x00\x00\x00\xC3")
                patch(data, rb"\x55\x41\x57\x41\x56\x56\x57\x53\x48\x81\xEC\x48\x01\x00\x00\x48\x8D\xAC\x24\x80\x00\x00\x00\x48\xC7\x85\xC0\x00\x00\x00\xFE\xFF\xFF\xFF\x48\x89\xD7", b"\xC3")
                file = bytes(data)
            patched_zipfile.writestr(name, file)

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
