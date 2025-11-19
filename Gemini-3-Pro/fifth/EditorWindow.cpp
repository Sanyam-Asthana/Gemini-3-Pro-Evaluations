#include "EditorWindow.h"
#include <QApplication>
#include <QFileDialog>
#include <QMessageBox>
#include <QTextStream>
#include <QColorDialog>
#include <QPrinter>
#include <QPrintDialog>
#include <QTextList>
#include <QMenuBar>  // FIX: Added missing include

EditorWindow::EditorWindow(QWidget *parent) : QMainWindow(parent) {
    setupUI();
    setMinimumSize(800, 600);
}

EditorWindow::~EditorWindow() {}

void EditorWindow::setupUI() {
    textEdit = new QTextEdit(this);
    setCentralWidget(textEdit);

    createActions();
    createMenus();
    createToolBars();

    connect(textEdit, &QTextEdit::currentCharFormatChanged, this, &EditorWindow::currentFormatChanged);
    connect(textEdit, &QTextEdit::cursorPositionChanged, this, &EditorWindow::cursorPositionChanged);
    
    setWindowTitle(tr("Untitled - C++ Rich Text Editor"));
}

void EditorWindow::createActions() {
    // File Actions
    actionNew = new QAction(QIcon::fromTheme("document-new"), tr("&New"), this);
    actionNew->setShortcut(QKeySequence::New);
    connect(actionNew, &QAction::triggered, this, &EditorWindow::fileNew);

    actionOpen = new QAction(QIcon::fromTheme("document-open"), tr("&Open..."), this);
    actionOpen->setShortcut(QKeySequence::Open);
    connect(actionOpen, &QAction::triggered, this, &EditorWindow::fileOpen);

    actionSave = new QAction(QIcon::fromTheme("document-save"), tr("&Save"), this);
    actionSave->setShortcut(QKeySequence::Save);
    connect(actionSave, &QAction::triggered, this, &EditorWindow::fileSave);

    actionSaveAs = new QAction(QIcon::fromTheme("document-save-as"), tr("Save &As..."), this);
    connect(actionSaveAs, &QAction::triggered, this, &EditorWindow::fileSaveAs);

    actionPrint = new QAction(QIcon::fromTheme("document-print"), tr("&Print..."), this);
    actionPrint->setShortcut(QKeySequence::Print);
    connect(actionPrint, &QAction::triggered, this, &EditorWindow::filePrint);

    // FIX: Edit Actions (Undo/Redo) implementation
    actionUndo = new QAction(QIcon::fromTheme("edit-undo"), tr("&Undo"), this);
    actionUndo->setShortcut(QKeySequence::Undo);
    actionUndo->setEnabled(false); // Disabled by default until an action happens
    connect(actionUndo, &QAction::triggered, textEdit, &QTextEdit::undo);
    connect(textEdit, &QTextEdit::undoAvailable, actionUndo, &QAction::setEnabled);

    actionRedo = new QAction(QIcon::fromTheme("edit-redo"), tr("&Redo"), this);
    actionRedo->setShortcut(QKeySequence::Redo);
    actionRedo->setEnabled(false);
    connect(actionRedo, &QAction::triggered, textEdit, &QTextEdit::redo);
    connect(textEdit, &QTextEdit::redoAvailable, actionRedo, &QAction::setEnabled);

    // Formatting Actions
    actionTextBold = new QAction(QIcon::fromTheme("format-text-bold"), tr("&Bold"), this);
    actionTextBold->setCheckable(true);
    actionTextBold->setShortcut(Qt::CTRL | Qt::Key_B);
    connect(actionTextBold, &QAction::triggered, this, &EditorWindow::textBold);

    actionTextItalic = new QAction(QIcon::fromTheme("format-text-italic"), tr("&Italic"), this);
    actionTextItalic->setCheckable(true);
    actionTextItalic->setShortcut(Qt::CTRL | Qt::Key_I);
    connect(actionTextItalic, &QAction::triggered, this, &EditorWindow::textItalic);

    actionTextUnderline = new QAction(QIcon::fromTheme("format-text-underline"), tr("&Underline"), this);
    actionTextUnderline->setCheckable(true);
    actionTextUnderline->setShortcut(Qt::CTRL | Qt::Key_U);
    connect(actionTextUnderline, &QAction::triggered, this, &EditorWindow::textUnderline);

    actionTextColor = new QAction(QIcon::fromTheme("format-text-color"), tr("&Color..."), this);
    connect(actionTextColor, &QAction::triggered, this, &EditorWindow::textColor);
    
    // Alignment Actions
    actionAlignLeft = new QAction(QIcon::fromTheme("format-justify-left"), tr("Left"), this);
    actionAlignLeft->setCheckable(true);
    connect(actionAlignLeft, &QAction::triggered, this, [this](){ textAlign(Qt::AlignLeft); });

    actionAlignCenter = new QAction(QIcon::fromTheme("format-justify-center"), tr("Center"), this);
    actionAlignCenter->setCheckable(true);
    connect(actionAlignCenter, &QAction::triggered, this, [this](){ textAlign(Qt::AlignCenter); });

    actionAlignRight = new QAction(QIcon::fromTheme("format-justify-right"), tr("Right"), this);
    actionAlignRight->setCheckable(true);
    connect(actionAlignRight, &QAction::triggered, this, [this](){ textAlign(Qt::AlignRight); });
    
    actionAlignJustify = new QAction(QIcon::fromTheme("format-justify-fill"), tr("Justify"), this);
    actionAlignJustify->setCheckable(true);
    connect(actionAlignJustify, &QAction::triggered, this, [this](){ textAlign(Qt::AlignJustify); });
}

void EditorWindow::createMenus() {
    QMenu *fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(actionNew);
    fileMenu->addAction(actionOpen);
    fileMenu->addAction(actionSave);
    fileMenu->addAction(actionSaveAs);
    fileMenu->addSeparator();
    fileMenu->addAction(actionPrint);

    QMenu *editMenu = menuBar()->addMenu(tr("&Edit"));
    // FIX: Use our custom actions instead of non-existent QTextEdit methods
    editMenu->addAction(actionUndo);
    editMenu->addAction(actionRedo);

    QMenu *formatMenu = menuBar()->addMenu(tr("F&ormat"));
    formatMenu->addAction(actionTextBold);
    formatMenu->addAction(actionTextItalic);
    formatMenu->addAction(actionTextUnderline);
    formatMenu->addAction(actionTextColor);
}

void EditorWindow::createToolBars() {
    QToolBar *fileToolBar = addToolBar(tr("File"));
    fileToolBar->addAction(actionNew);
    fileToolBar->addAction(actionOpen);
    fileToolBar->addAction(actionSave);
    fileToolBar->addAction(actionPrint);

    QToolBar *fmtToolBar = addToolBar(tr("Format"));
    fmtToolBar->addAction(actionUndo); // FIX: Added Undo/Redo to toolbar
    fmtToolBar->addAction(actionRedo);
    fmtToolBar->addSeparator();
    fmtToolBar->addAction(actionTextBold);
    fmtToolBar->addAction(actionTextItalic);
    fmtToolBar->addAction(actionTextUnderline);
    fmtToolBar->addAction(actionTextColor);
    fmtToolBar->addSeparator();
    fmtToolBar->addAction(actionAlignLeft);
    fmtToolBar->addAction(actionAlignCenter);
    fmtToolBar->addAction(actionAlignRight);
    fmtToolBar->addAction(actionAlignJustify);

    // Font Combo Box
    comboFont = new QFontComboBox(fileToolBar);
    connect(comboFont, &QComboBox::textActivated, this, [this](){ textFont(comboFont->currentFont()); });
    fmtToolBar->addWidget(comboFont);

    // Size Combo Box
    comboSize = new QComboBox(fileToolBar);
    comboSize->setEditable(true);
    const QList<int> standardSizes = QFontDatabase::standardSizes();
    for (int size : standardSizes)
        comboSize->addItem(QString::number(size));
    comboSize->setCurrentIndex(standardSizes.indexOf(QApplication::font().pointSize()));
    connect(comboSize, &QComboBox::textActivated, this, &EditorWindow::textSize);
    fmtToolBar->addWidget(comboSize);
}

// ==================== Logic Implementation ====================

void EditorWindow::fileNew() {
    textEdit->clear();
    currentFileName.clear();
    setWindowTitle(tr("Untitled - C++ Rich Text Editor"));
}

void EditorWindow::fileOpen() {
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"), "", tr("HTML Files (*.html *.htm);;Text Files (*.txt)"));
    if (fileName.isEmpty()) return;

    QFile file(fileName);
    if (!file.open(QFile::ReadOnly | QFile::Text)) {
        QMessageBox::warning(this, tr("Error"), tr("Cannot open file: ") + file.errorString());
        return;
    }

    QTextStream in(&file);
    QString content = in.readAll();
    
    // If HTML, parse it, otherwise set plain text
    if (Qt::mightBeRichText(content))
        textEdit->setHtml(content);
    else
        textEdit->setPlainText(content);

    currentFileName = fileName;
    setWindowTitle(currentFileName);
}

void EditorWindow::fileSave() {
    if (currentFileName.isEmpty()) {
        fileSaveAs();
    } else {
        QFile file(currentFileName);
        if (!file.open(QFile::WriteOnly | QFile::Text)) {
            QMessageBox::warning(this, tr("Error"), tr("Cannot save file: ") + file.errorString());
            return;
        }
        QTextStream out(&file);
        out << textEdit->toHtml(); // Save as HTML to preserve formatting
        setWindowTitle(currentFileName);
    }
}

void EditorWindow::fileSaveAs() {
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"), "", tr("HTML Files (*.html *.htm)"));
    if (fileName.isEmpty()) return;
    currentFileName = fileName;
    fileSave();
}

void EditorWindow::filePrint() {
    QPrinter printer(QPrinter::HighResolution);
    QPrintDialog *dlg = new QPrintDialog(&printer, this);
    if (dlg->exec() == QDialog::Accepted) {
        textEdit->print(&printer);
    }
    delete dlg;
}

void EditorWindow::textBold() {
    QTextCharFormat fmt;
    fmt.setFontWeight(actionTextBold->isChecked() ? QFont::Bold : QFont::Normal);
    mergeFormatOnWordOrSelection(fmt);
}

void EditorWindow::textUnderline() {
    QTextCharFormat fmt;
    fmt.setFontUnderline(actionTextUnderline->isChecked());
    mergeFormatOnWordOrSelection(fmt);
}

void EditorWindow::textItalic() {
    QTextCharFormat fmt;
    fmt.setFontItalic(actionTextItalic->isChecked());
    mergeFormatOnWordOrSelection(fmt);
}

void EditorWindow::textColor() {
    QColor col = QColorDialog::getColor(textEdit->textColor(), this);
    if (!col.isValid()) return;
    QTextCharFormat fmt;
    fmt.setForeground(col);
    mergeFormatOnWordOrSelection(fmt);
}

void EditorWindow::textAlign(Qt::Alignment a) {
    textEdit->setAlignment(a);
}

void EditorWindow::textFont(const QFont &f) {
    QTextCharFormat fmt;
    fmt.setFont(f);
    mergeFormatOnWordOrSelection(fmt);
}

void EditorWindow::textSize(const QString &p) {
    qreal pointSize = p.toFloat();
    if (p.toFloat() > 0) {
        QTextCharFormat fmt;
        fmt.setFontPointSize(pointSize);
        mergeFormatOnWordOrSelection(fmt);
    }
}

void EditorWindow::mergeFormatOnWordOrSelection(const QTextCharFormat &format) {
    QTextCursor cursor = textEdit->textCursor();
    if (!cursor.hasSelection())
        cursor.select(QTextCursor::WordUnderCursor);
    cursor.mergeCharFormat(format);
    textEdit->mergeCurrentCharFormat(format);
}

// Update toolbar buttons based on where the cursor is (e.g. toggle bold button if text is bold)
void EditorWindow::currentFormatChanged(const QTextCharFormat &format) {
    actionTextBold->setChecked(format.font().bold());
    actionTextItalic->setChecked(format.font().italic());
    actionTextUnderline->setChecked(format.font().underline());
}

void EditorWindow::cursorPositionChanged() {
    if (textEdit->alignment() & Qt::AlignLeft) actionAlignLeft->setChecked(true);
    else if (textEdit->alignment() & Qt::AlignHCenter) actionAlignCenter->setChecked(true);
    else if (textEdit->alignment() & Qt::AlignRight) actionAlignRight->setChecked(true);
    else if (textEdit->alignment() & Qt::AlignJustify) actionAlignJustify->setChecked(true);
}
