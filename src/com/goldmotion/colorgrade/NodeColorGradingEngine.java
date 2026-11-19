package com.goldmotion.colorgrade;

import java.io.Serializable;

/**
 * Node Video-Grade Advanced Color Grading Engine
 * Supports 3-Way Lift/Gamma/Gain Wheels, Spline RGB Curves, 8-Channel HSL, Tone Recovery, and 3D LUTs.
 */
public class NodeColorGradingEngine implements Serializable {

    // 1. 3-Way Color Wheels (Lift, Gamma, Gain, Offset)
    public float[] liftRgb = new float[]{0f, 0f, 0f};    // Shadows [-1.0 to 1.0]
    public float liftExposure = 0f;

    public float[] gammaRgb = new float[]{0f, 0f, 0f};   // Midtones [-1.0 to 1.0]
    public float gammaExposure = 0f;

    public float[] gainRgb = new float[]{0f, 0f, 0f};    // Highlights [-1.0 to 1.0]
    public float gainExposure = 0f;

    public float[] offsetRgb = new float[]{0f, 0f, 0f};  // Master Offset

    // 2. Tone & Recovery
    public float temperature = 0f; // -100 (Cool) to +100 (Warm)
    public float tint = 0f;        // -100 (Green) to +100 (Magenta)
    public float exposure = 0f;    // -3.0 to +3.0 EV
    public float contrast = 1.0f;  // 0.0 to 2.0
    public float highlights = 0f;  // -1.0 to 1.0
    public float shadows = 0f;     // -1.0 to 1.0
    public float whites = 0f;      // -1.0 to 1.0
    public float blacks = 0f;      // -1.0 to 1.0
    public float vibrance = 0f;    // -1.0 to 1.0 (Skin-tone preserving)
    public float saturation = 1.0f;// 0.0 to 2.0

    // 3. 8-Channel Selective HSL Qualifier (Red, Orange, Yellow, Green, Cyan, Blue, Purple, Magenta)
    public float[] channelHue = new float[8];
    public float[] channelSat = new float[8];
    public float[] channelLum = new float[8];

    // 4. Master & RGB Curves Control Points (5-point Cubic Spline)
    public float[][] masterCurve = new float[][]{{0f,0f}, {0.25f,0.25f}, {0.5f,0.5f}, {0.75f,0.75f}, {1f,1f}};
    public float[][] redCurve = new float[][]{{0f,0f}, {0.5f,0.5f}, {1f,1f}};
    public float[][] greenCurve = new float[][]{{0f,0f}, {0.5f,0.5f}, {1f,1f}};
    public float[][] blueCurve = new float[][]{{0f,0f}, {0.5f,0.5f}, {1f,1f}};

    // 5. 3D LUT (Look-Up Table)
    public String activeLutPath = null;
    public float lutIntensity = 1.0f;

    public void reset() {
        liftRgb = new float[]{0f, 0f, 0f};
        liftExposure = 0f;
        gammaRgb = new float[]{0f, 0f, 0f};
        gammaExposure = 0f;
        gainRgb = new float[]{0f, 0f, 0f};
        gainExposure = 0f;
        offsetRgb = new float[]{0f, 0f, 0f};

        temperature = 0f;
        tint = 0f;
        exposure = 0f;
        contrast = 1.0f;
        highlights = 0f;
        shadows = 0f;
        whites = 0f;
        blacks = 0f;
        vibrance = 0f;
        saturation = 1.0f;

        channelHue = new float[8];
        channelSat = new float[8];
        channelLum = new float[8];

        activeLutPath = null;
        lutIntensity = 1.0f;
    }
}
