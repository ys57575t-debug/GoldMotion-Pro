#!/usr/bin/env python3
import os
import sys
import struct
import zlib
import time

STORED_EXTENSIONS = {
    '.arsc',
    '.png', '.jpg', '.jpeg', '.gif', '.webp',
    '.mp4', '.m4a', '.mp3', '.ogg', '.wav', '.webm',
    '.tflite',
    '.so'
}

def should_store(rel_path):
    ext = os.path.splitext(rel_path)[1].lower()
    if rel_path == "resources.arsc" or ext in STORED_EXTENSIONS:
        return True
    return False

def build_aligned_apk(app_dir, output_apk):
    print(f"Building aligned APK: {app_dir} -> {output_apk}")
    
    files_to_pack = []
    for root, dirs, files in os.walk(app_dir):
        for f in sorted(files):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, app_dir).replace('\\', '/')
            if rel_path.startswith("src/") or rel_path.startswith(".git"):
                continue
            # Also skip any existing signature files in META-INF (apksigner will re-sign)
            if rel_path.startswith("META-INF/") and (rel_path.endswith(".SF") or rel_path.endswith(".RSA") or rel_path.endswith(".DSA") or rel_path.endswith(".MF")):
                continue
            files_to_pack.append((full_path, rel_path))

    # To ensure Android loads classes in optimal order, sort so AndroidManifest.xml and classes*.dex come first
    def sort_key(item):
        p = item[1]
        if p == "AndroidManifest.xml":
            return (0, p)
        if p.startswith("classes") and p.endswith(".dex"):
            num = p.replace("classes", "").replace(".dex", "")
            n = int(num) if num else 1
            return (1, n)
        if p == "resources.arsc":
            return (2, p)
        return (3, p)

    files_to_pack.sort(key=sort_key)
    print(f"Total files to pack: {len(files_to_pack)}")

    # Use fixed timestamp for reproducibility (2026-01-01 00:00:00)
    dos_time = 0x5c00
    dos_date = 0x5c01

    cd_entries = []
    
    with open(output_apk, 'wb') as out:
        for idx, (full_p, rel_p) in enumerate(files_to_pack):
            with open(full_p, 'rb') as fp:
                data = fp.read()
            
            uncomp_size = len(data)
            crc = zlib.crc32(data) & 0xffffffff
            
            is_stored = should_store(rel_p)
            fname_bytes = rel_p.encode('utf-8')
            fname_len = len(fname_bytes)
            
            if is_stored:
                method = 0
                comp_data = data
                comp_size = uncomp_size
                align = 4096 if rel_p.endswith('.so') else 4
            else:
                method = 8
                # compress with deflate (wbits=-15 for raw deflate)
                compressor = zlib.compressobj(6, zlib.DEFLATED, -15)
                comp_data = compressor.compress(data) + compressor.flush()
                comp_size = len(comp_data)
                align = 1

            # Current write position
            header_offset = out.tell()
            
            # Calculate padding needed for data alignment
            # Local header = 30 + fname_len + extra_len
            min_header_size = 30 + fname_len
            data_offset = header_offset + min_header_size
            if align > 1:
                padding = (align - (data_offset % align)) % align
            else:
                padding = 0
            
            extra = b'\x00' * padding
            extra_len = len(extra)
            
            # Write local header
            # Signature: PK\x03\x04
            flags = 0
            version_needed = 20
            local_hdr = struct.pack(
                '<4sHHHHHIIIHH',
                b'PK\x03\x04',
                version_needed,
                flags,
                method,
                dos_time,
                dos_date,
                crc,
                comp_size,
                uncomp_size,
                fname_len,
                extra_len
            )
            out.write(local_hdr)
            out.write(fname_bytes)
            if extra_len > 0:
                out.write(extra)
            
            # Verify data alignment
            actual_data_offset = out.tell()
            if align > 1:
                assert actual_data_offset % align == 0, f"Alignment failed for {rel_p}: offset {actual_data_offset} not divisible by {align}"
            
            # Write data
            out.write(comp_data)
            
            # Record central directory entry info
            cd_entries.append((
                version_needed, flags, method, dos_time, dos_date,
                crc, comp_size, uncomp_size, fname_bytes, header_offset
            ))
            
            if (idx + 1) % 1000 == 0:
                print(f"  Processed {idx + 1} / {len(files_to_pack)} files...")

        # Central directory
        cd_start_offset = out.tell()
        for entry in cd_entries:
            v_needed, flags, method, dtime, ddate, crc, c_sz, u_sz, f_bytes, h_off = entry
            fn_len = len(f_bytes)
            cd_hdr = struct.pack(
                '<4sHHHHHHIIIHHHHHII',
                b'PK\x01\x02',
                0x0314, # version made by (UNIX, zip 2.0)
                v_needed,
                flags,
                method,
                dtime,
                ddate,
                crc,
                c_sz,
                u_sz,
                fn_len,
                0, # extra_len in CD
                0, # comment_len
                0, # disk number start
                0, # internal file attrs
                0x81a40000 if not f_bytes.endswith(b'/') else 0x41ed0000, # external file attrs
                h_off
            )
            out.write(cd_hdr)
            out.write(f_bytes)
            
        cd_end_offset = out.tell()
        cd_total_size = cd_end_offset - cd_start_offset
        
        # End of Central Directory record
        eocd = struct.pack(
            '<4sHHHHIIH',
            b'PK\x05\x06',
            0, # disk num
            0, # disk num with start
            len(cd_entries),
            len(cd_entries),
            cd_total_size,
            cd_start_offset,
            0 # comment len
        )
        out.write(eocd)

    print(f"Aligned APK successfully created at {output_apk} (size: {os.path.getsize(output_apk) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    app_dir = sys.argv[1] if len(sys.argv) > 1 else "app"
    out_apk = sys.argv[2] if len(sys.argv) > 2 else "aligned_uncompressed.apk"
    build_aligned_apk(app_dir, out_apk)
