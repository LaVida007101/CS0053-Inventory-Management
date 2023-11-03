package lib;

public class PrintFormat {
    public static final int SCREEN_WIDTH = 80;
    public static final String TITLE = "Inventory Management System";
    
    public static String centerTitle(String title, int SCREEN_WIDTH) {
        int textLength = title.length();
        if (SCREEN_WIDTH <= textLength) {
            return title;
        }

        int padding = (SCREEN_WIDTH - textLength) / 2;
        String centeredTitle = " ".repeat(padding) + title;
        centeredTitle += " ".repeat(SCREEN_WIDTH - padding - textLength);

        return centeredTitle + "\n";
    }

    public static String centerText(String text, int SCREEN_WIDTH) {
        int textLength = text.length();

        if (SCREEN_WIDTH <= textLength) {
            return text;
        }

        int padding = (SCREEN_WIDTH - textLength) / 2;
        String centeredText = " ".repeat(padding) + text;
        centeredText += " ".repeat(SCREEN_WIDTH - padding - textLength);

        return centerTitle(text, SCREEN_WIDTH) + centeredText;
    }

    public static String centerNote(String note, int SCREEN_WIDTH) {
        int textLength = note.length();
        if (SCREEN_WIDTH <= textLength) {
            return note;
        }

        int padding = (SCREEN_WIDTH - textLength) / 2;
        String centeredNote = " ".repeat(padding) + note;
        centeredNote += " ".repeat(SCREEN_WIDTH - padding - textLength);

        return centeredNote;
    }

    public static String lines(int SCREEN_WIDTH) {
        String line = "=".repeat(SCREEN_WIDTH);
        return line + "\n";
    }

    public static String dash(int SCREEN_WIDTH) {
        String dash = "-".repeat(SCREEN_WIDTH);
        return dash + "\n";
    }
}
