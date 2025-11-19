#ifndef EDITORWINDOW_H
#define EDITORWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include <QAction>
#include <QMenu>
#include <QToolBar>
#include <QComboBox>
#include <QFontComboBox>

class EditorWindow : public QMainWindow {
    Q_OBJECT

public:
    EditorWindow(QWidget *parent = nullptr);
    ~EditorWindow();

private slots:
    // File Operations
    void fileNew();
    void fileOpen();
    void fileSave();
    void fileSaveAs();
    void filePrint();

    // Text Formatting
    void textBold();
    void textUnderline();
    void textItalic();
    void textColor();
    void textAlign(Qt::Alignment a);
    void textSize(const QString &p);
    void textFont(const QFont &f);
    
    // UI State Updates
    void currentFormatChanged(const QTextCharFormat &format);
    void cursorPositionChanged();

private:
    void setupUI();
    void createActions();
    void createMenus();
    void createToolBars();
    void mergeFormatOnWordOrSelection(const QTextCharFormat &format);

    QTextEdit *textEdit;
    QString currentFileName;

    // Actions
    QAction *actionSave;
    QAction *actionSaveAs;
    QAction *actionOpen;
    QAction *actionNew;
    QAction *actionPrint;
    
    // Edit Actions (FIX: Added these)
    QAction *actionUndo;
    QAction *actionRedo;

    QAction *actionTextBold;
    QAction *actionTextUnderline;
    QAction *actionTextItalic;
    QAction *actionTextColor;
    
    QAction *actionAlignLeft;
    QAction *actionAlignCenter;
    QAction *actionAlignRight;
    QAction *actionAlignJustify;

    // Combo Boxes for Toolbar
    QFontComboBox *comboFont;
    QComboBox *comboSize;
};

#endif // EDITORWINDOW_H
