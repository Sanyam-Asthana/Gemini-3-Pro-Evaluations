#include "mainwindow.h"
#include <QTextList>
#include <QTextCursor>
#include <QTextBlockFormat>
#include <QTextCharFormat>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Simple Rich Text Editor");
    setMinimumSize(800, 600);

    textEdit = new QTextEdit(this);
    setCentralWidget(textEdit);

    setupToolBar();
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupToolBar()
{
    QToolBar *toolBar = addToolBar("Formatting");

    // File actions
    QAction *actionSave = new QAction("Save", this);
    connect(actionSave, &QAction::triggered, this, &MainWindow::saveFile);
    toolBar->addAction(actionSave);

    QAction *actionOpen = new QAction("Open", this);
    connect(actionOpen, &QAction::triggered, this, &MainWindow::openFile);
    toolBar->addAction(actionOpen);

    toolBar->addSeparator();

    // Formatting actions
    actionBold = new QAction("Bold", this);
    actionBold->setCheckable(true);
    // Connect the toggled(bool) signal to the new slot
    connect(actionBold, &QAction::toggled, this, &MainWindow::onBoldToggled);
    toolBar->addAction(actionBold);

    actionItalic = new QAction("Italic", this);
    actionItalic->setCheckable(true);
    // Connect the toggled(bool) signal to the new slot
    connect(actionItalic, &QAction::toggled, this, &MainWindow::onItalicToggled);
    toolBar->addAction(actionItalic);

    actionUnderline = new QAction("Underline", this);
    actionUnderline->setCheckable(true);
    // Connect the toggled(bool) signal to the new slot
    connect(actionUnderline, &QAction::toggled, this, &MainWindow::onUnderlineToggled);
    toolBar->addAction(actionUnderline);

    toolBar->addSeparator();

    // Alignment actions - This part now works due to the included header
    QActionGroup *alignGroup = new QActionGroup(this);
    QAction *actionAlignLeft = alignGroup->addAction("Align Left");
    QAction *actionAlignCenter = alignGroup->addAction("Align Center");
    QAction *actionAlignRight = alignGroup->addAction("Align Right");
    QAction *actionAlignJustify = alignGroup->addAction("Justify");

    actionAlignLeft->setCheckable(true);
    actionAlignCenter->setCheckable(true);
    actionAlignRight->setCheckable(true);
    actionAlignJustify->setCheckable(true);
    actionAlignLeft->setChecked(true);

    toolBar->addActions(alignGroup->actions());
    connect(alignGroup, &QActionGroup::triggered, this, &MainWindow::textAlign);

    toolBar->addSeparator();

    // Color action
    QAction *actionColor = new QAction("Color", this);
    connect(actionColor, &QAction::triggered, this, &MainWindow::textColor);
    toolBar->addAction(actionColor);

    toolBar->addSeparator();

    // List actions
    QAction *actionListOrdered = new QAction("Ordered List", this);
    connect(actionListOrdered, &QAction::triggered, this, &MainWindow::listOrdered);
    toolBar->addAction(actionListOrdered);

    QAction *actionListUnordered = new QAction("Unordered List", this);
    connect(actionListUnordered, &QAction::triggered, this, &MainWindow::listUnordered);
    toolBar->addAction(actionListUnordered);
}

// Implement the new slots
void MainWindow::onBoldToggled(bool checked)
{
    QTextCharFormat fmt;
    fmt.setFontWeight(checked ? QFont::Bold : QFont::Normal);
    textEdit->mergeCurrentCharFormat(fmt);
}

void MainWindow::onItalicToggled(bool checked)
{
    QTextCharFormat fmt;
    fmt.setFontItalic(checked);
    textEdit->mergeCurrentCharFormat(fmt);
}

void MainWindow::onUnderlineToggled(bool checked)
{
    QTextCharFormat fmt;
    fmt.setFontUnderline(checked);
    textEdit->mergeCurrentCharFormat(fmt);
}

void MainWindow::textAlign(QAction *a)
{
    if (a->text() == "Align Left")
        textEdit->setAlignment(Qt::AlignLeft | Qt::AlignAbsolute);
    else if (a->text() == "Align Center")
        textEdit->setAlignment(Qt::AlignCenter);
    else if (a->text() == "Align Right")
        textEdit->setAlignment(Qt::AlignRight | Qt::AlignAbsolute);
    else if (a->text() == "Justify")
        textEdit->setAlignment(Qt::AlignJustify);
}

void MainWindow::textColor()
{
    QColor col = QColorDialog::getColor(textEdit->textColor(), this);
    if (!col.isValid())
        return;
    QTextCharFormat fmt;
    fmt.setForeground(col);
    textEdit->mergeCurrentCharFormat(fmt);
}

void MainWindow::listOrdered() {
    QTextCursor cursor = textEdit->textCursor();
    cursor.createList(QTextListFormat::ListDecimal);
}

void MainWindow::listUnordered() {
    QTextCursor cursor = textEdit->textCursor();
    cursor.createList(QTextListFormat::ListDisc);
}

void MainWindow::saveFile()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Save File", "", "HTML Files (*.html)");
    if (fileName.isEmpty())
        return;

    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QFile::Text))
        return;

    file.write(textEdit->toHtml().toUtf8());
    file.close();
}

void MainWindow::openFile()
{
    QString fileName = QFileDialog::getOpenFileName(this, "Open File", "", "HTML Files (*.html)");
    if (fileName.isEmpty())
        return;

    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly | QFile::Text))
        return;

    textEdit->setHtml(file.readAll());
    file.close();
}
