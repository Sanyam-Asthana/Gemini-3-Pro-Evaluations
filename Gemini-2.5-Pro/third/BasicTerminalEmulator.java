import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class BasicTerminalEmulator extends JFrame {

    private JTextArea outputArea;
    private JTextField inputField;
    private List<String> history = new ArrayList<>();
    private int historyIndex = 0;
    private File currentDirectory;

    public BasicTerminalEmulator() {
        setTitle("Java Terminal Emulator");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // Set the initial working directory to the user's home directory
        currentDirectory = new File(System.getProperty("user.home"));

        // Output Area
        outputArea = new JTextArea();
        outputArea.setEditable(false);
        outputArea.setBackground(Color.BLACK);
        outputArea.setForeground(Color.WHITE);
        outputArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
        JScrollPane scrollPane = new JScrollPane(outputArea);
        add(scrollPane, BorderLayout.CENTER);

        // Input Field
        inputField = new JTextField();
        inputField.setBackground(Color.BLACK);
        inputField.setForeground(Color.WHITE);
        inputField.setFont(new Font("Monospaced", Font.PLAIN, 14));
        inputField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String command = inputField.getText();
                if (!command.trim().isEmpty()) {
                    history.add(command);
                    historyIndex = history.size();
                    executeCommand(command);
                    inputField.setText("");
                }
            }
        });

        // Command History Navigation
        inputField.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                if (evt.getKeyCode() == java.awt.event.KeyEvent.VK_UP) {
                    if (historyIndex > 0) {
                        historyIndex--;
                        inputField.setText(history.get(historyIndex));
                    }
                } else if (evt.getKeyCode() == java.awt.event.KeyEvent.VK_DOWN) {
                    if (historyIndex < history.size() - 1) {
                        historyIndex++;
                        inputField.setText(history.get(historyIndex));
                    } else if (historyIndex == history.size() - 1) {
                        historyIndex++;
                        inputField.setText("");
                    }
                }
            }
        });

        add(inputField, BorderLayout.SOUTH);

        setVisible(true);
        inputField.requestFocusInWindow();
    }

    private void executeCommand(String command) {
        outputArea.append("$ " + command + "\n");
        try {
            ProcessBuilder processBuilder = new ProcessBuilder();
            boolean isWindows = System.getProperty("os.name").toLowerCase().startsWith("windows");

            // Handle 'cd' command separately as it's a shell built-in
            if (command.trim().startsWith("cd ")) {
                String newDir = command.trim().substring(3).trim();
                File newDirectory = new File(currentDirectory, newDir).getCanonicalFile();
                if (newDirectory.exists() && newDirectory.isDirectory()) {
                    currentDirectory = newDirectory;
                } else {
                    outputArea.append("cd: no such file or directory: " + newDir + "\n");
                }
                return;
            }

            if (isWindows) {
                processBuilder.command("cmd.exe", "/c", command);
            } else {
                processBuilder.command("sh", "-c", command);
            }

            processBuilder.directory(currentDirectory);
            Process process = processBuilder.start();

            // Capture and display the output
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                outputArea.append(line + "\n");
            }

            // Capture and display any errors
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = errorReader.readLine()) != null) {
                outputArea.append("ERROR: " + line + "\n");
            }

            process.waitFor();

        } catch (IOException | InterruptedException ex) {
            outputArea.append("Error executing command: " + ex.getMessage() + "\n");
        }
        // Ensure the JTextArea scrolls to the bottom
        outputArea.setCaretPosition(outputArea.getDocument().getLength());
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new BasicTerminalEmulator();
            }
        });
    }
}
