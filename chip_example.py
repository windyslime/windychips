import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from qfluentwidgets import FluentIcon as fIcon, isDarkTheme, setTheme, Theme

from chip import WindyChip


class ChipExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chip控件示例")
        self.resize(800, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加标题
        title = QLabel("Chip控件示例")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # 添加说明
        description = QLabel("Chip控件用于显示图标和文本，带有删除按钮，可作为标签供用户选择。使用方式和QPushButton完全相同。")
        description.setWordWrap(True)
        main_layout.addWidget(description)
        
        # 基本用法示例
        main_layout.addWidget(QLabel("基本用法："))
        basic_layout = QHBoxLayout()
        basic_layout.setSpacing(10)
        
        # 创建基本Chip
        basic_chip = WindyChip(text="基本标签")
        basic_chip.deleteClicked.connect(lambda: self.on_delete_clicked("基本标签"))
        basic_chip.clicked.connect(lambda: self.on_chip_clicked("基本标签"))
        basic_layout.addWidget(basic_chip)
        
        main_layout.addLayout(basic_layout)
        
        # 带图标的Chip示例
        main_layout.addWidget(QLabel("带图标的Chip："))
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(10)
        
        # 创建带图标的Chip
        icon_chip1 = WindyChip(text="设置")
        icon_chip1.setIcon(fIcon.SETTING.icon())
        icon_chip1.deleteClicked.connect(lambda: self.on_delete_clicked("设置"))
        
        icon_chip2 = WindyChip(text="编辑")
        icon_chip2.setIcon(fIcon.EDIT.icon())
        icon_chip2.deleteClicked.connect(lambda: self.on_delete_clicked("编辑"))
        
        icon_chip3 = WindyChip(text="信息")
        icon_chip3.setIcon(fIcon.INFO.icon())
        icon_chip3.deleteClicked.connect(lambda: self.on_delete_clicked("信息"))
        
        icon_layout.addWidget(icon_chip1)
        icon_layout.addWidget(icon_chip2)
        icon_layout.addWidget(icon_chip3)
        icon_layout.addStretch(1)
        
        main_layout.addLayout(icon_layout)
        
        # 状态示例
        main_layout.addWidget(QLabel("不同状态的Chip："))
        state_layout = QHBoxLayout()
        state_layout.setSpacing(10)
        
        # 创建不同状态的Chip
        normal_chip = WindyChip(text="普通状态")
        normal_chip.deleteClicked.connect(lambda: self.on_delete_clicked("普通状态"))
        
        checked_chip = WindyChip(text="选中状态")
        checked_chip.setChecked(True)
        checked_chip.deleteClicked.connect(lambda: self.on_delete_clicked("选中状态"))
        
        disabled_chip = WindyChip(text="禁用状态")
        disabled_chip.setEnabled(False)
        
        state_layout.addWidget(normal_chip)
        state_layout.addWidget(checked_chip)
        state_layout.addWidget(disabled_chip)
        state_layout.addStretch(1)
        
        main_layout.addLayout(state_layout)
        
        # 主题切换按钮
        theme_layout = QHBoxLayout()
        theme_chip = WindyChip(text="切换主题")
        theme_chip.setIcon(fIcon.PALETTE.icon() if not isDarkTheme() else fIcon.SUNNY.icon())
        theme_chip.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(theme_chip)
        theme_layout.addStretch(1)
        
        main_layout.addLayout(theme_layout)
        main_layout.addStretch(1)
        
        # 应用当前主题
        self.apply_current_theme()
    
    def on_delete_clicked(self, text):
        print(f"删除按钮被点击: {text}")
    
    def on_chip_clicked(self, text):
        print(f"Chip被点击: {text}")
    
    def toggle_theme(self):
        # 切换主题
        new_theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        setTheme(new_theme)
        self.apply_current_theme()
    
    def apply_current_theme(self):
        # 应用当前主题到所有Chip
        for chip in self.findChildren(WindyChip):
            if isDarkTheme():
                chip.apply_dark_theme()
            else:
                chip.updateStyle()
        
        # 更新主题切换按钮图标
        theme_chip = None
        for chip in self.findChildren(WindyChip):
            if chip.text() == "切换主题":
                theme_chip = chip
                break
        
        if theme_chip:
            theme_chip.setIcon(fIcon.PALETTE.icon() if not isDarkTheme() else fIcon.SUNNY.icon())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChipExample()
    window.show()
    sys.exit(app.exec())