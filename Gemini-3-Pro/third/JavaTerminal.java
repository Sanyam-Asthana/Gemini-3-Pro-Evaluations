import javax.swing.*;
import javax.swing.text.DefaultCaret;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class JavaTerminal extends JFrame {
    private JTextArea textArea;
    private int lastPromptPosition; // Tracks where the user input begins
    private File currentDirectory;

    public JavaTerminal() {
        // 1. Setup the Window
        setTitle("Java Terminal Emulator");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        // 2. Initialize Directory
        currentDirectory = new File(System.getProperty("user.dir"));

        // 3. Setup Text Area
        textArea = new JTextArea();
        textArea.setBackground(Color.BLACK);
        textArea.setForeground(new Color(0, 255, 0)); // Matrix Green
        textArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
        textArea.setCaretColor(Color.WHITE);
        
        // Auto-scroll to bottom
        DefaultCaret caret = (DefaultCaret) textArea.getCaret();
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);

        // 4. Add Scroll Pane
        JScrollPane scrollPane = new JScrollPane(textArea);
        add(scrollPane);

        // 5. Handle Input
        textArea.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                // Prevent editing previous text (history)
                if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE) {
                    if (textArea.getCaretPosition() <= lastPromptPosition) {
                        e.consume(); // Ignore backspace if at prompt
                    }
                } else if (textArea.getCaretPosition() < lastPromptPosition) {
                    // Move caret to end if user tries to type in history
                    textArea.setCaretPosition(textArea.getText().length());
                }

                // Handle Enter Key
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    e.consume(); // Prevent default newline insertion immediately
                    String fullText = textArea.getText();
                    String command = fullText.substring(lastPromptPosition).trim();
                    
                    appendToArea("\n"); // Move to next line
                    
                    if (!command.isEmpty()) {
                        executeCommand(command);
                    } else {
                        printPrompt();
                    }
                }
            }
        });

        // 6. Initial Prompt
        printPrompt();
    }

    private void printPrompt() {
        String path = currentDirectory.getAbsolutePath();
        String prompt = path + "> ";
        appendToArea(prompt);
        lastPromptPosition = textArea.getText().length();
    }

    private void appendToArea(String text) {
        SwingUtilities.invokeLater(() -> {
            textArea.append(text);
            textArea.setCaretPosition(textArea.getText().length());
        });
    }

    private void executeCommand(String command) {
        // Handle "clear" or "cls"
        if (command.equalsIgnoreCase("clear") || command.equalsIgnoreCase("cls")) {
            textArea.setText("");
            printPrompt();
            return;
        }
        
        // Handle "exit"
        if (command.equalsIgnoreCase("exit")) {
            System.exit(0);
        }

        // Handle "cd" (Change Directory) - Special case
        if (command.startsWith("cd ")) {
            String targetPath = command.substring(3).trim();
            File newDir;
            
            if (targetPath.equals("..")) {
                newDir = currentDirectory.getParentFile();
                if (newDir == null) newDir = currentDirectory; // Already at root
            } else {
                // Support absolute and relative paths
                File f = new File(targetPath);
                if (f.isAbsolute()) {
                    newDir = f;
                } else {
                    newDir = new File(currentDirectory, targetPath);
                }
            }

            if (newDir.exists() && newDir.isDirectory()) {
                currentDirectory = newDir;
            } else {
                appendToArea("The system cannot find the path specified.\n");
            }
            printPrompt();
            return;
        }

        // Run standard commands in a background thread
        new Thread(() -> {
            try {
                ProcessBuilder builder = new ProcessBuilder();
                boolean isWindows = System.getProperty("os.name").toLowerCase().startsWith("windows");

                if (isWindows) {
                    builder.command("cmd.exe", "/c", command);
                } else {
                    builder.command("sh", "-c", command);
                }

                builder.directory(currentDirectory);
                builder.redirectErrorStream(true); // Merge stdout and stderr

                Process process = builder.start();

                // Read Output
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    appendToArea(line + "\n");
                }
                
                process.waitFor();

            } catch (Exception e) {
                appendToArea("Error: " + e.getMessage() + "\n");
            } finally {
                // Always print a new prompt when done
                SwingUtilities.invokeLater(this::printPrompt);
            }
        }).start();
    }

    public static void main(String[] args) {
        // Run GUI on Event Dispatch Thread
        SwingUtilities.invokeLater(() -> {
            JavaTerminal terminal = new JavaTerminal();
            terminal.setVisible(true);
        });
    }
}
