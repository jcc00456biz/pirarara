#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from pkg.config import AppConfig
from pkg.const import __appname__, __version__
from pkg.gui.custom import (
    PirararaComboBox,
    PirararaImageViewer,
    PirararaTableWidget,
    PirararaToolButton,
    PirararaTreeWidget,
)
from pkg.gui.dialogs import (
    AboutDialog,
    OpenFileDialog,
    PluginsDialog,
    SettingDialog,
)
from pkg.gui.plugins import (
    ExternalPlugins,
    ImportFilePlugin,
    PirararaBasePlugin,
)
from pkg.translation import Translate
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class MWindow(QMainWindow):
    """
    メインウィンドウクラス。

    このクラスは、PySideを使用してメインウィンドウを作成します。
    ウィジェット、ツールバー、メニューバーなどの設定を行い、GUIの基本的な構造を構築します。

    Attributes:
        app_config (AppConfig): アプリケーション構成ファイルアクセスクラスのインスタンス。
        centralwidget (QWidget): 中央ウィジェット。
        verticalLayout (QVBoxLayout): 中央ウィジェット内の垂直レイアウト。
        toolbar (QToolBar): ツールバー。
        tool_button_define (tuple): ツールボタン定義。
        tool_buttons (list): 作成されたツールボタンのリスト。
        comboBox (PirararaComboBox): コンボボックス。
        splitter_1 (QSplitter): 上部スプリッター。
        splitter_2 (QSplitter): 下部スプリッター。
        treeWidget (PirararaTreeWidget): ツリーウィジェット。
        tableWidget (PirararaTableWidget): テーブルウィジェット。
        graphicsView (PirararaImageViewer): グラフィックスビュー。
        plainTextEdit (QPlainTextEdit): プレインテキストエディット。
        menubar (QMenuBar): メニューバー。
        statusbar (QStatusBar): ステータスバー。
    """

    def __init__(self):
        """
        MWindowのコンストラクタ。

        メインウィンドウの初期化を行い、ウィジェットやレイアウトの設定、
        シグナルとスロットの接続などを行います。
        """
        super().__init__()

        # アプリケーション構成ファイルアクセスクラス
        self.app_config = AppConfig()

        # 翻訳クラスを生成
        self.tr = Translate()

        # 画面タイトルの設定
        self.setWindowTitle(f"{__appname__} {__version__}")

        # ウインドウサイズ設定
        self.resize(1280, 640)

        self.centralwidget = QWidget(self)

        # 垂直レイアウト
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # ツールバー
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(48, 48))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        # ツールボタン定義
        self.tool_button_define = (
            (
                self.tr.tr(self.__class__.__name__, "IMPORT"),
                "import.svg",
                self.show_import_file_dialog,
            ),
            ("|", "", None),
            (
                self.tr.tr(self.__class__.__name__, "SETTING"),
                "setting.svg",
                self.show_setting_dialog,
            ),
            (
                self.tr.tr(self.__class__.__name__, "PLUGINS"),
                "plugins.svg",
                self.show_plugins_dialog,
            ),
            ("|", "", None),
            (
                self.tr.tr(self.__class__.__name__, "ABOUT"),
                "pirarara.svg",
                self.show_about_dialog,
            ),
            ("|", "", None),
            (
                self.tr.tr(self.__class__.__name__, "DEBUG"),
                "debug.svg",
                self.show_debug_dialog,
            ),
        )
        # ツールボタン
        self.tool_buttons = []
        for title, icon_file_name, slot in self.tool_button_define:
            if title == "|":
                self.toolbar.addSeparator()
                continue
            # アイコン
            icon_dir = os.path.join(os.getcwd(), "icon")
            icon_file_path = os.path.join(icon_dir, icon_file_name)
            self.tool_buttons.append(PirararaToolButton(title, icon_file_path))
            # スロット
            if slot is not None:
                self.tool_buttons[-1].clicked.connect(slot)
            # ツールバーにツールボタンを配置
            self.toolbar.addWidget(self.tool_buttons[-1])

        # コンボボックス
        self.comboBox = PirararaComboBox(self.centralwidget)
        self.verticalLayout.addWidget(self.comboBox)

        # スプリッター
        self.splitter_1 = QSplitter(self.centralwidget)
        self.splitter_1.setOrientation(Qt.Orientation.Horizontal)

        # ツリーウィジェット
        self.treeWidget = PirararaTreeWidget(self.splitter_1)
        self.splitter_1.addWidget(self.treeWidget)

        # テーブルウィジェット
        self.tableWidget = PirararaTableWidget(self.splitter_1)
        self.splitter_1.addWidget(self.tableWidget)

        # スプリッター
        self.splitter_2 = QSplitter(self.splitter_1)
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)

        # グラフィックスビュー
        self.graphicsView = PirararaImageViewer(self.splitter_2)
        self.splitter_2.addWidget(self.graphicsView)

        # プレインテキストエディット
        self.plainTextEdit = QPlainTextEdit(self.splitter_2)
        self.splitter_2.addWidget(self.plainTextEdit)

        self.splitter_1.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.splitter_1)

        self.setCentralWidget(self.centralwidget)
        # メニューバー
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 784, 33))
        self.setMenuBar(self.menubar)

        # ステータスバー
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # ウインドウ位置、サイズなどを設定
        self._setup()

        # コンボボックスのシグナルにスロットを割り当て
        self.comboBox.item_edited.connect(self.on_combo_box_editing)

        # ツリーウィジェットのシグナルにスロットを割り当て
        self.treeWidget.item_selected.connect(
            self.on_tree_widget_item_selected
        )

        # テーブルウィジェットのシグナルにスロットを割り当て
        self.tableWidget.item_selected.connect(
            self.on_table_widget_item_selected
        )
        self.tableWidget.item_changed.connect(
            self.on_table_widget_item_changed
        )

    def _setup(self):
        """
        ウィンドウの状態やスプリッターの状態を保存または復元する。

        アプリケーション構成ファイルがデフォルト値の場合は、
        現在の状態を保存し、それ以外の場合は保存された状態を復元します。
        """
        if self.app_config.isdefault:
            self.app_config.config["APP_GUI"]["main_window"] = (
                self.app_config.q_bytearray_to_str(self.saveGeometry())
            )
            self.app_config.config["APP_GUI"]["splitter1"] = (
                self.app_config.q_bytearray_to_str(self.splitter_1.saveState())
            )
            self.app_config.config["APP_GUI"]["splitter2"] = (
                self.app_config.q_bytearray_to_str(self.splitter_2.saveState())
            )
            self.app_config.write_config()
        else:
            self.restoreGeometry(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["main_window"]
                )
            )
            self.splitter_1.restoreState(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["splitter1"]
                )
            )
            self.splitter_2.restoreState(
                self.app_config.str_to_q_bytearray(
                    self.app_config.config["APP_GUI"]["splitter2"]
                )
            )

    def closeEvent(self, event):
        """
        ウィンドウを閉じる際の処理を実行する。

        ウィンドウやスプリッターの状態を構成ファイルに保存してから
        クローズイベントを呼び出します。

        Args:
            event (QCloseEvent): クローズイベント。
        """
        self.app_config.config["APP_GUI"]["main_window"] = (
            self.app_config.q_bytearray_to_str(self.saveGeometry())
        )
        self.app_config.config["APP_GUI"]["splitter1"] = (
            self.app_config.q_bytearray_to_str(self.splitter_1.saveState())
        )
        self.app_config.config["APP_GUI"]["splitter2"] = (
            self.app_config.q_bytearray_to_str(self.splitter_2.saveState())
        )
        self.app_config.write_config()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """
        キーボード入力時の処理を実行する。

        Deleteキーが押された場合、フォーカスがテーブルウィジェットにあるときは
        選択されたデータを削除します。

        Args:
            event (QKeyEvent): キープレスイベント。
        """
        if event.key() == Qt.Key_Delete and self.tableWidget.hasFocus():
            reply = QMessageBox.question(
                self,
                self.tr.tr(self.__class__.__name__, "message"),
                self.tr.tr(
                    self.__class__.__name__, "Is it okay to delete this?"
                ),
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            # 表の選択されているデータを削除
            self.tableWidget.delete_selected_items()
            # データ削除に伴い表示を更新
            self.graphicsView.clear_image()
            self.treeWidget.refresh_display()
            self.tableWidget.get_form_db("", "")

    def show_import_file_dialog(self):
        """
        ファイルインポートダイアログを表示し、選択されたファイルを処理する。
        """
        dialog = OpenFileDialog(self)
        selected_files = dialog.get_selected_file()

        if len(selected_files) != 0:
            plugin = ImportFilePlugin(selected_files)
            plugin.exec()
            self.treeWidget.refresh_display()
            self.tableWidget.get_form_db("", "")

    def show_setting_dialog(self):
        """
        Settingダイアログを表示する。
        """
        dialog = SettingDialog(self)
        dialog.exec()

    def show_plugins_dialog(self):
        """
        Pluginsダイアログを表示する。
        """
        dialog = PluginsDialog(self)
        dialog.exec()

    def show_about_dialog(self):
        """
        Aboutダイアログを表示する。
        """
        dialog = AboutDialog(self)
        dialog.exec()

    def on_combo_box_editing(self, text: str):
        """
        コンボボックスの編集時に処理を実行する。

        Args:
            text (str): コンボボックスに入力されたテキスト。
        """
        if len(text) == 0:
            self.tableWidget.get_form_db("", "")
        else:
            self.tableWidget.get_form_db("title", text)

    def on_tree_widget_item_selected(self, column_text: str, parent_text: str):
        """
        ツリーウィジェットのアイテム選択時に処理を実行する。

        Args:
            column_text (str): 選択された列のテキスト。
            parent_text (str): 親ノードのテキスト。
        """
        self.tableWidget.get_form_db(parent_text, column_text)

    def on_table_widget_item_selected(self, db_id: int):
        """
        テーブルウィジェットのアイテム選択時に処理を実行する。

        Args:
            db_id (int): 選択されたデータベースID。
        """
        self.graphicsView.show_image(db_id)

    def on_table_widget_item_changed(self):
        """
        テーブルウィジェットのアイテム変更時に処理を実行する。
        """
        self.treeWidget.refresh_display()

    def show_title_dialog(self):
        """
        Settingダイアログを表示する。
        """
        dialog = PirararaBasePlugin(1000)
        dialog.exec()

    def show_debug_dialog(self):
        ext_plugins = ExternalPlugins()
        plugin = ext_plugins.load_plugins()
        # プラグインのsetting呼び出し
        plugin.setting()
        # プラグインのdo_action呼び出し
        plugin.do_action()
