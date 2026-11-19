package com.goldmotion.colorgrade;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;

/**
 * Clean Studio Theme Manager
 * Sets Red & White as default, with selectable Cyber Cyan, Emerald, Purple, and Monochrome themes.
 */
public class ThemeManager {
    private static final String PREF_NAME = "studio_theme_prefs";
    private static final String KEY_THEME = "selected_theme";

    public enum Theme {
        RED_WHITE("Red & White (Default)", "#FF2B44", "#FFFFFF", "#121212", "#1E1E1E"),
        CYBER_CYAN("Cyber Cyan", "#00E5FF", "#FFFFFF", "#0D1117", "#161B22"),
        EMERALD_NEON("Emerald Green", "#00E676", "#FFFFFF", "#101410", "#182018"),
        ROYAL_PURPLE("Royal Purple", "#BB86FC", "#FFFFFF", "#14101A", "#1F1828"),
        MONOCHROME("Clean Monochrome", "#E0E0E0", "#FFFFFF", "#0A0A0A", "#1A1A1A");

        public final String title;
        public final int primaryColor;
        public final int textColor;
        public final int backgroundColor;
        public final int cardColor;

        Theme(String title, String primary, String text, String bg, String card) {
            this.title = title;
            this.primaryColor = Color.parseColor(primary);
            this.textColor = Color.parseColor(text);
            this.backgroundColor = Color.parseColor(bg);
            this.cardColor = Color.parseColor(card);
        }
    }

    public static Theme getCurrentTheme(Context context) {
        SharedPreferences prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        String name = prefs.getString(KEY_THEME, Theme.RED_WHITE.name());
        try {
            return Theme.valueOf(name);
        } catch (Exception e) {
            return Theme.RED_WHITE;
        }
    }

    public static void setTheme(Context context, Theme theme) {
        context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
               .edit().putString(KEY_THEME, theme.name()).apply();
    }
}
