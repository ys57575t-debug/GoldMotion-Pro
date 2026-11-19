# Gold Motion Pro (Red & White Edition)

A high-performance, modded video and motion graphics editing suite based on Gold Motion.

---

## 🎨 Key Features & Improvements

### 1. Modern Red & White Default Theme + Multi-Theme Selector
- The previous golden UI styling has been replaced with a high-contrast **Crimson Red (`#FF2B44`) and Crisp White (`#FFFFFF`)** aesthetic.
- Includes built-in support for multiple color accents:
  - **Red & White** (Default)
  - **Cyber Cyan** (`#00E5FF`)
  - **Emerald Green** (`#00E676`)
  - **Royal Purple** (`#BB86FC`)
  - **Clean Monochrome** (`#E0E0E0`)

### 2. Standalone Node Video-Grade Color Grading Engine
- Dedicated **Color Grading** button accessible immediately upon tapping any image or video layer in the timeline bottom bar (independent of the Effects stack).
- **Professional Colorist Tools:**
  - **3-Way Color Wheels:** Independent Lift (Shadows), Gamma (Midtones), and Gain (Highlights) wheels with exposure controls.
  - **Tone & Dynamic Range Recovery:** Temperature, Tint, Highlights, Shadows, Whites, Blacks, Vibrance, and Saturation.
  - **8-Channel Selective HSL Qualifier:** Individual Hue, Saturation, and Luminance adjustment across 8 distinct color channels.
  - **5-Point RGB Curves:** Master, Red, Green, and Blue cubic spline curve manipulation.
  - **3D LUT Support:** Hardware-accelerated `.cube` lookup table rendering.

### 3. Clean & Native Video Reverse
- Accessible directly from the timeline layer edit action bar.
- Streamlined modal encoding dialog with zero clutter and 100% removal of the old golden HUD bubble.

### 4. Complete Watermark & Branding Eradication
- All traces of 'Pankaj' / 'PNKJ' watermarks, usernames (`okpnkj`, `fwpnkj`), social links, and update dialogs have been permanently erased.
- Custom effects sanitized and renamed to clean cinematic nomenclature (`cine_*.xml` / `cine_*.webp`).

### 5. Extreme Optimization for 4GB RAM Devices
- Texture preview allocations automatically clamped to 1080p for sub-4GB devices.
- Mediump FP16 fast shader arithmetic with zero frame drops.
- Eliminates heavy background Puter AI polling loops for silky smooth 60fps scrubbing and preview.

---

## 🚀 Automated CI/CD Build via GitHub Actions

This repository includes a GitHub Actions workflow (`.github/workflows/build_apk.yml`) that:
1. Compiles all Java color grading and theme manager classes into Android DEX bytecode.
2. Packages the complete application assets, layouts, and native libraries.
3. Automatically runs `zipalign` and signs the APK with `apksigner`.
4. Publishes release artifacts and downloadable `.apk` directly to GitHub Releases.
