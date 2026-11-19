#!/usr/bin/env python3
import os
import sys
import zipfile

def package_apk(app_dir, output_apk):
    print(f"Packaging {app_dir} -> {output_apk}...")
    file_count = 0
    with zipfile.ZipFile(output_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, app_dir)

                # Skip src/ directory containing .java source code
                if rel_path.startswith("src/") or rel_path.startswith("src\\"):
                    continue

                # Uncompressed files: resources.arsc and native libraries (.so)
                # Android requires these uncompressed for mmap performance and memory alignment
                if rel_path == "resources.arsc" or (rel_path.startswith("lib/") and rel_path.endswith(".so")):
                    zf.write(full_path, rel_path, compress_type=zipfile.ZIP_STORED)
                else:
                    zf.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)
                file_count += 1
                if file_count % 1000 == 0:
                    print(f"  Packed {file_count} files...")

    print(f"Packaging complete! Total files packed: {file_count}, Output size: {os.path.getsize(output_apk) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    app_dir = sys.argv[1] if len(sys.argv) > 1 else "app"
    out_apk = sys.argv[2] if len(sys.argv) > 2 else "unaligned.apk"
    package_apk(app_dir, out_apk)
