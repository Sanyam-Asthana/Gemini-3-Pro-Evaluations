#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include <QToolBar>
#include <QAction>
#include <QActionGroup> // <-- ADD THIS INCLUDE
#include <QMenu>
#include <QMenuBar>
#include <QFontComboBox>
#include <QComboBox>
#include <QColorDialog>
#include <QFileDialog>
#include <QFile>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // Renamed slots to be more descriptive and accept the bool parameter
    void onBoldToggled(bool checked);
    void onItalicToggled(bool checked);
    void onUnderlineToggled(bool checked);
    void textAlign(QAction *a);
    void textColor();
    void listOrdered();
    void listUnordered();
    void saveFile();
    void openFile();

private:
    void setupToolBar();
    QTextEdit *textEdit;

    // Member variables for actions to connect them properly
    QAction *actionBold;
    QAction *actionItalic;
    QAction *actionUnderline;
};
#endif // MAINWINDOW_H
