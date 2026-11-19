#version 300 es
precision mediump float;

in vec2 vTexCoord;
out vec4 fragColor;

uniform sampler2D uTexture;
uniform vec3 uLift;       // Shadows adjustment [-1.0 to 1.0]
uniform vec3 uGamma;      // Midtones adjustment [-1.0 to 1.0]
uniform vec3 uGain;       // Highlights adjustment [-1.0 to 1.0]
uniform float uTemp;      // Color Temperature [-1.0 to 1.0]
uniform float uTint;      // Green-Magenta Tint [-1.0 to 1.0]
uniform float uExposure;  // Exposure in EV
uniform float uContrast;  // Contrast factor
uniform float uVibrance;  // Smart skin-tone vibrance
uniform float uSaturation;// Saturation factor

float getLuma(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

void main() {
    vec4 color = texture(uTexture, vTexCoord);
    vec3 rgb = color.rgb;

    // 1. Exposure EV
    rgb *= pow(2.0, uExposure);

    // 2. White Balance (Temperature & Tint)
    rgb.r += uTemp * 0.12;
    rgb.b -= uTemp * 0.12;
    rgb.g += uTint * 0.10;

    // 3. 3-Way Color Wheels (Lift, Gamma, Gain)
    float luma = getLuma(rgb);
    vec3 lift = uLift * (1.0 - luma);
    vec3 gain = (uGain - 1.0) * luma;
    rgb = max(vec3(0.0), rgb + lift + gain);
    rgb = pow(max(vec3(0.0), rgb), 1.0 / max(vec3(0.1), (1.0 + uGamma)));

    // 4. Contrast factor
    rgb = (rgb - 0.5) * uContrast + 0.5;

    // 5. Smart Vibrance
    float maxCol = max(rgb.r, max(rgb.g, rgb.b));
    float minCol = min(rgb.r, min(rgb.g, rgb.b));
    float sat = (maxCol - minCol) / max(maxCol, 0.001);
    float vibFactor = (1.0 - sat) * uVibrance;
    rgb = mix(vec3(luma), rgb, 1.0 + vibFactor);

    // 6. Global Saturation
    rgb = mix(vec3(getLuma(rgb)), rgb, uSaturation);

    fragColor = vec4(clamp(rgb, 0.0, 1.0), color.a);
}
