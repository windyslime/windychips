from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QIcon, QPainter, QColor, QPen, QFont, QCursor
from PyQt6.QtWidgets import QPushButton, QApplication, QHBoxLayout, QLabel, QToolButton


class WindyChip(QPushButton):
    """
    Chip控件，用于显示图标和文本，带有删除按钮，可作为标签供用户选择。
    使用方式和QPushButton完全相同。
    """
    # 定义删除按钮点击信号
    deleteClicked = pyqtSignal()

    def __init__(self, parent=None, text="", icon=None):
        super().__init__(parent)
        self.setText(text)
        if icon:
            self.setIcon(icon)

        # 设置基本属性
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setCheckable(True)
        self.setFixedHeight(32)  # 固定高度

        # 创建布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 0, 8, 0)
        self.layout.setSpacing(8)

        # 创建文本标签
        self.textLabel = QLabel(text, self)
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 创建删除按钮
        self.deleteButton = QToolButton(self)
        self.deleteButton.setFixedSize(16, 16)
        self.deleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.deleteButton.clicked.connect(self.onDeleteButtonClicked)
        
        # 设置删除按钮图标（使用Unicode字符作为关闭图标）
        self.deleteButton.setText("✕")
        self.deleteButton.setStyleSheet("""
            QToolButton {
                border: none;
                background-color: transparent;
                color: #888888;
                font-size: 12px;
            }
            QToolButton:hover {
                color: #444444;
            }
        """)

        # 添加组件到布局
        if icon:
            self.layout.addSpacing(4)  # 图标左侧间距
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.deleteButton)

        # 应用QSS样式
        self.updateStyle()

    def setText(self, text):
        super().setText(text)
        if hasattr(self, 'textLabel'):
            self.textLabel.setText(text)

    def text(self):
        return super().text()

    def setIcon(self, icon):
        super().setIcon(icon)
        self.update()

    def onDeleteButtonClicked(self):
        self.deleteClicked.emit()

    def updateStyle(self):
        # 根据是否选中设置不同的样式
        self.setStyleSheet("""
        WindyChip {
            border: 1px solid #d1d1d1;
            border-radius: 16px;
            background-color: #f5f5f5;
            padding: 4px 8px;
            color: #333333;
        }
        
        Chip:hover {
            background-color: #e5e5e5;
        }
        
        Chip:checked {
            background-color: #e0f2fe;
            border-color: #0078d4;
            color: #0078d4;
        }
        
        Chip:disabled {
            background-color: #f0f0f0;
            border-color: #e0e0e0;
            color: #a0a0a0;
        }
        """)

    def paintEvent(self, event):
        # 自定义绘制，确保图标和文本正确显示
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景
        if self.isChecked():
            painter.setBrush(QColor("#e0f2fe"))
            painter.setPen(QPen(QColor("#0078d4"), 1))
        elif self.underMouse():
            painter.setBrush(QColor("#e5e5e5"))
            painter.setPen(QPen(QColor("#d1d1d1"), 1))
        else:
            painter.setBrush(QColor("#f5f5f5"))
            painter.setPen(QPen(QColor("#d1d1d1"), 1))
            
        if self.isEnabled() is False:
            painter.setBrush(QColor("#f0f0f0"))
            painter.setPen(QPen(QColor("#e0e0e0"), 1))
            
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 16, 16)
        
        # 如果有图标，绘制图标
        if not self.icon().isNull():
            iconSize = QSize(16, 16)
            iconRect = QRect(12, (self.height() - iconSize.height()) // 2, 
                             iconSize.width(), iconSize.height())
            self.icon().paint(painter, iconRect)
            # 为文本标签添加左边距，避免与图标重叠
            self.textLabel.setContentsMargins(24, 0, 0, 0)

    def sizeHint(self):
        # 根据内容调整大小
        width = self.textLabel.sizeHint().width() + self.deleteButton.width() + 40  # 增加间距
        if not self.icon().isNull():
            width += 28  # 为图标增加更多空间
        return QSize(width, 32)


    def apply_dark_theme(self):
        self.setStyleSheet("""
        WindyChip {
            border: 1px solid #555555;
            border-radius: 16px;
            background-color: #333333;
            padding: 4px 8px;
            color: #ffffff;
        }
        
        Chip:hover {
            background-color: #444444;
            border-color: #666666;
        }
        
        Chip:checked {
            background-color: #0078d4;
            border-color: #2b9fff;
            color: #ffffff;
        }
        
        Chip:disabled {
            background-color: #2a2a2a;
            border-color: #404040;
            color: #808080;
        }
        """)
        
        self.deleteButton.setStyleSheet("""
            QToolButton {
                border: none;
                background-color: transparent;
                color: #aaaaaa;
                font-size: 12px;
            }
            QToolButton:hover {
                color: #ffffff;
            }
        """)


# 示例代码，用于测试
if __name__ == "__main__":
    import sys
    from PyQt6.QtGui import QIcon
    
    app = QApplication(sys.argv)
    
    # 创建一个窗口显示Chip控件
    from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
    
    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    
    # 创建一个水平布局放置多个Chip
    h_layout = QHBoxLayout()
    
    # 创建几个Chip控件
    chip1 = Chip(text="标签1")
    chip2 = Chip(text="带图标的标签")
    chip2.setIcon(QIcon.fromTheme("document-new"))  # 使用系统图标
    chip3 = Chip(text="选中的标签")
    chip3.setChecked(True)
    chip4 = Chip(text="禁用的标签")
    chip4.setEnabled(False)
    
    # 连接删除信号
    chip1.deleteClicked.connect(lambda: print("删除标签1"))
    chip2.deleteClicked.connect(lambda: print("删除带图标的标签"))
    chip3.deleteClicked.connect(lambda: print("删除选中的标签"))
    
    # 添加到布局
    h_layout.addWidget(chip1)
    h_layout.addWidget(chip2)
    h_layout.addWidget(chip3)
    h_layout.addWidget(chip4)
    h_layout.addStretch(1)  # 添加弹性空间
    
    layout.addLayout(h_layout)
    layout.addStretch(1)  # 添加弹性空间
    
    # 显示窗口
    window.setWindowTitle("Chip控件示例")
    window.resize(600, 200)
    window.show()
    
    sys.exit(app.exec())