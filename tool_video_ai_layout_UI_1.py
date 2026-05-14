from PyQt5 import QtCore, QtGui, QtWidgets


class ResizeFilter(QtCore.QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            QtCore.QTimer.singleShot(0, self.ui.applyResponsiveStyle)
        return False


class Ui_Widget(object):
    def setupUi(self, Widget):
        self.Widget = Widget
        Widget.setObjectName("Widget")
        Widget.resize(1500, 900)
        Widget.setMinimumSize(1200, 720)

        self.inputs = []
        self.buttons = []
        self.sceneFrames = []
        self.sceneImages = []
        self.promptBoxes = []

        self.mainLayout = QtWidgets.QHBoxLayout(Widget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.mainLayout.addWidget(self.splitter)

        # ===================== BÊN TRÁI =====================
        self.leftScroll = QtWidgets.QScrollArea()
        self.leftScroll.setObjectName("leftScroll")
        self.leftScroll.setWidgetResizable(True)
        self.leftScroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftScroll.setMinimumWidth(330)

        self.leftFrame = QtWidgets.QFrame()
        self.leftFrame.setObjectName("leftFrame")
        self.leftScroll.setWidget(self.leftFrame)

        self.leftLayout = QtWidgets.QVBoxLayout(self.leftFrame)
        self.leftLayout.setContentsMargins(14, 14, 14, 14)
        self.leftLayout.setSpacing(10)

        self.addLeftTitle("Mô hình sinh kịch bản")
        self.comboModel = self.makeCombo(["Gemini 3.1 Flash-Lite", "Gemini 2.5 Pro", "GPT-4.1", "Claude"])
        self.leftLayout.addWidget(self.comboModel)

        self.addLeftTitle("AsyncLab API Key")
        self.inputApi = self.makeLine("Nhập AsyncLab Key...")
        self.leftLayout.addWidget(self.inputApi)

        self.addLeftTitle("Đường dẫn folder")
        self.inputFolder = self.makeLine()
        self.inputFolder.setText(r"C:\Users\Admin\Desktop\VIDEO AI")
        self.leftLayout.addWidget(self.inputFolder)

        self.btnOpenFolder = self.makeButton("📁  Mở thư mục xuất này")
        self.leftLayout.addWidget(self.btnOpenFolder)

        self.line1 = QtWidgets.QFrame()
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setObjectName("line")
        self.leftLayout.addWidget(self.line1)

        self.titleOption = QtWidgets.QLabel("TÙY CHỌN KỊCH BẢN")
        self.titleOption.setObjectName("titleOption")
        self.leftLayout.addWidget(self.titleOption)

        self.addLeftTitle("Phong cách hình ảnh/ video")
        self.comboStyle = self.makeCombo([
            "Hyper Realistic (Chân thực 100%)",
            "Anime Style",
            "Cinematic",
            "3D Cartoon",
            "Fantasy Art"
        ])
        self.leftLayout.addWidget(self.comboStyle)

        self.checkHistorical = self.makeCheck("Dùng cho nội dung lịch sử, chân dung")
        self.leftLayout.addWidget(self.checkHistorical)

        self.addLeftTitle("Ngôn ngữ kịch bản và giọng nói")
        self.comboLanguage = self.makeCombo(["US English", "Tiếng Việt", "Japanese", "Korean"])
        self.leftLayout.addWidget(self.comboLanguage)

        self.addLeftTitle("Tỷ lệ copy từ video gốc")
        self.comboCopy = self.makeCombo([
            "50% - Copy một nửa",
            "70% - Giữ phần lớn nội dung",
            "30% - Biến đổi nhiều hơn"
        ])
        self.leftLayout.addWidget(self.comboCopy)

        self.addLeftTitle("Tùy chỉnh thời lượng")
        self.checkDuration = self.makeCheck("Bật tùy chỉnh thời lượng")
        self.checkDuration.setChecked(True)
        self.leftLayout.addWidget(self.checkDuration)

        self.warningBox = QtWidgets.QLabel("⚠ Có thể gây mất chính xác so với video gốc")
        self.warningBox.setObjectName("warningBox")
        self.warningBox.setWordWrap(True)
        self.leftLayout.addWidget(self.warningBox)

        self.addLeftTitle("Thời lượng (giây)")
        self.inputTime = self.makeLine()
        self.inputTime.setText("60")
        self.leftLayout.addWidget(self.inputTime)

        self.checkRefImage = self.makeCheck("Ảnh tham chiếu")
        self.checkRefImage.setChecked(True)
        self.leftLayout.addWidget(self.checkRefImage)

        self.checkVoice = self.makeCheck("Đồng nhất giọng nhân vật")
        self.checkVoice.setChecked(True)
        self.leftLayout.addWidget(self.checkVoice)

        self.addLeftTitle("Giọng nhân vật đồng nhất")
        self.comboVoice = self.makeCombo(["Giọng nữ trẻ", "Giọng nam trầm", "Giọng kể chuyện", "Tự động"])
        self.leftLayout.addWidget(self.comboVoice)

        self.leftLayout.addStretch()

        # ===================== BÊN PHẢI =====================
        self.rightFrame = QtWidgets.QFrame()
        self.rightFrame.setObjectName("rightFrame")

        self.rightLayout = QtWidgets.QVBoxLayout(self.rightFrame)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(10)

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.tabGrok = QtWidgets.QWidget()
        self.tabVeo3 = QtWidgets.QWidget()
        self.tabSeedance = QtWidgets.QWidget()

        self.tabWidget.addTab(self.tabGrok, "Chế độ grok tạo video")
        self.tabWidget.addTab(self.tabVeo3, "Chế độ Veo3 tạo video")
        self.tabWidget.addTab(self.tabSeedance, "Chế độ Seedance 2.0 video")

        self.setupTabGrok()
        self.setupTabVeo3()
        self.setupTabSeedance()

        self.rightLayout.addWidget(self.tabWidget)

        self.splitter.addWidget(self.leftScroll)
        self.splitter.addWidget(self.rightFrame)

        # Bên trái : bên phải = 1 : 3
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.setSizes([380, 1120])

        self.applyResponsiveStyle()

        self.resizeFilter = ResizeFilter(self)
        Widget.installEventFilter(self.resizeFilter)

        QtCore.QMetaObject.connectSlotsByName(Widget)

    # ===================== HELPER =====================
    def addLeftTitle(self, text):
        label = QtWidgets.QLabel(text)
        label.setObjectName("leftLabel")
        self.leftLayout.addWidget(label)
        return label

    def makeLine(self, placeholder=""):
        line = QtWidgets.QLineEdit()
        line.setPlaceholderText(placeholder)
        line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.inputs.append(line)
        return line

    def makeCombo(self, items):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.inputs.append(combo)
        return combo

    def makeButton(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.buttons.append(btn)
        return btn

    def makeCheck(self, text):
        check = QtWidgets.QCheckBox(text)
        check.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return check

    def makeTextEdit(self, placeholder=""):
        text = QtWidgets.QTextEdit()
        text.setPlaceholderText(placeholder)
        text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.promptBoxes.append(text)
        return text

    def makeActionGrid(self, buttons, column_count=3):
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        for index, btn in enumerate(buttons):
            row = index // column_count
            col = index % column_count
            grid.addWidget(btn, row, col)

        for col in range(column_count):
            grid.setColumnStretch(col, 1)

        return grid

    # ===================== TAB GROK =====================
    def setupTabGrok(self):
        layout = QtWidgets.QVBoxLayout(self.tabGrok)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.grokUrl = self.makeLine("Nhập video hoặc nội dung cho Grok...")
        self.grokNote = self.makeLine("Mô tả thêm tùy chọn...")

        self.btnGrokAnalyze = self.makeButton("🤖 PHÂN TÍCH BẰNG GROK")
        self.btnGrokAnalyze.setObjectName("bigPurpleButton")

        self.btnGrokMerge = self.makeButton("🎬 Ghép Video")
        self.btnGrokScene = self.makeButton("🎞 Ghép cảnh đã chọn")
        self.btnGrokFix = self.makeButton("🛠 Sửa tất cả lỗi")
        self.btnGrokAdd = self.makeButton("➕ Thêm kịch bản")

        self.grokText = self.makeTextEdit("Kết quả kịch bản Grok sẽ hiển thị ở đây...")

        layout.addWidget(self.grokUrl)
        layout.addWidget(self.grokNote)
        layout.addWidget(self.btnGrokAnalyze)
        layout.addLayout(self.makeActionGrid([
            self.btnGrokMerge,
            self.btnGrokScene,
            self.btnGrokFix,
            self.btnGrokAdd
        ], 4))
        layout.addWidget(self.grokText)

    # ===================== TAB VEO3 =====================
    def setupTabVeo3(self):
        layout = QtWidgets.QVBoxLayout(self.tabVeo3)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.veoUrl = self.makeLine()
        self.veoUrl.setText("https://www.youtube.com/shorts/bQic0POmBHA")

        self.veoNote = self.makeLine("Mô tả thêm tùy chọn...")

        self.btnAnalyzeYoutube = self.makeButton("🐱 PHÂN TÍCH TỪ YOUTUBE")
        self.btnAnalyzeYoutube.setObjectName("bigPurpleButton")

        self.btnProcessing = self.makeButton("⏳ Đang xử lý... (2/13)")
        self.btnMergeVideo = self.makeButton("🎬 Ghép Video")
        self.btnMergeScene = self.makeButton("🎞 Ghép cảnh đã chọn (0)")
        self.btnCombo = self.makeButton("⚡ Đang chạy Combo 3...")
        self.btnFixAll = self.makeButton("🛠 Sửa tất cả lỗi")
        self.btnAddScript = self.makeButton("➕ Thêm kịch bản")

        self.refFrame = QtWidgets.QFrame()
        self.refFrame.setObjectName("refFrame")

        self.refLayout = QtWidgets.QHBoxLayout(self.refFrame)
        self.refLayout.setContentsMargins(14, 14, 14, 14)
        self.refLayout.setSpacing(14)

        self.refImageBox = QtWidgets.QLabel("ẢNH THAM CHIẾU")
        self.refImageBox.setObjectName("refImageBox")
        self.refImageBox.setAlignment(QtCore.Qt.AlignCenter)
        self.refImageBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.refText = QtWidgets.QLabel(
            "MEO ME (Adult female cat, white fur, red dress...)\n"
            "MEO BO (Adult male cat, orange tabby fur, strong posture...)"
        )
        self.refText.setObjectName("refText")
        self.refText.setWordWrap(True)

        self.refLayout.addWidget(self.refImageBox)
        self.refLayout.addWidget(self.refText)
        self.refLayout.setStretch(0, 1)
        self.refLayout.setStretch(1, 2)

        self.sceneScroll = QtWidgets.QScrollArea()
        self.sceneScroll.setObjectName("sceneScroll")
        self.sceneScroll.setWidgetResizable(True)
        self.sceneScroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.sceneContainer = QtWidgets.QWidget()
        self.sceneLayout = QtWidgets.QVBoxLayout(self.sceneContainer)
        self.sceneLayout.setContentsMargins(0, 0, 0, 0)
        self.sceneLayout.setSpacing(14)

        for i in range(1, 7):
            self.sceneLayout.addWidget(self.createSceneBox(i))

        self.sceneLayout.addStretch()
        self.sceneScroll.setWidget(self.sceneContainer)

        layout.addWidget(self.veoUrl)
        layout.addWidget(self.veoNote)
        layout.addWidget(self.btnAnalyzeYoutube)
        layout.addLayout(self.makeActionGrid([
            self.btnProcessing,
            self.btnMergeVideo,
            self.btnMergeScene,
            self.btnCombo,
            self.btnFixAll,
            self.btnAddScript
        ], 3))
        layout.addWidget(self.refFrame)
        layout.addWidget(self.sceneScroll, 1)

    # ===================== TAB SEEDANCE =====================
    def setupTabSeedance(self):
        layout = QtWidgets.QVBoxLayout(self.tabSeedance)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.seedUrl = self.makeLine("Nhập link video hoặc prompt cho Seedance 2.0...")
        self.seedNote = self.makeLine("Mô tả thêm tùy chọn...")

        self.btnSeedAnalyze = self.makeButton("✨ PHÂN TÍCH SEEDANCE 2.0")
        self.btnSeedAnalyze.setObjectName("bigPurpleButton")

        self.btnSeedVideo = self.makeButton("🎬 Tạo Video")
        self.btnSeedScene = self.makeButton("🎞 Tạo cảnh đã chọn")
        self.btnSeedFix = self.makeButton("🛠 Sửa tất cả lỗi")
        self.btnSeedAdd = self.makeButton("➕ Thêm kịch bản")

        self.seedText = self.makeTextEdit("Prompt Seedance 2.0 sẽ hiển thị ở đây...")

        layout.addWidget(self.seedUrl)
        layout.addWidget(self.seedNote)
        layout.addWidget(self.btnSeedAnalyze)
        layout.addLayout(self.makeActionGrid([
            self.btnSeedVideo,
            self.btnSeedScene,
            self.btnSeedFix,
            self.btnSeedAdd
        ], 4))
        layout.addWidget(self.seedText)

    # ===================== BOX CẢNH =====================
    def createSceneBox(self, index):
        frame = QtWidgets.QFrame()
        frame.setObjectName("sceneFrame")
        frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        layout = QtWidgets.QHBoxLayout(frame)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(16)

        imageBox = QtWidgets.QLabel(f"SCENE {index}")
        imageBox.setObjectName("sceneImageBox")
        imageBox.setAlignment(QtCore.Qt.AlignCenter)
        imageBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        rightBox = QtWidgets.QFrame()
        rightBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        rightLayout = QtWidgets.QVBoxLayout(rightBox)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setSpacing(8)

        title = QtWidgets.QCheckBox(f"CẢNH {index}")
        title.setChecked(True)
        title.setObjectName("sceneTitle")

        labelPrompt = QtWidgets.QLabel("VIDEO PROMPT")
        labelPrompt.setObjectName("cyanLabel")

        prompt = QtWidgets.QTextEdit()
        prompt.setText(
            "anime style, vibrant colors, clean outlines, soft cel shading, "
            "detailed eyes, studio-quality anime frame, high clarity character design. "
            "The character stands in a cinematic scene with expressive emotion."
        )
        prompt.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        labelTts = QtWidgets.QLabel("APPS / TTS")
        labelTts.setObjectName("cyanLabel")

        tts = QtWidgets.QLineEdit()
        tts.setText("I am pregnant!")
        self.inputs.append(tts)

        rightLayout.addWidget(title)
        rightLayout.addWidget(labelPrompt)
        rightLayout.addWidget(prompt)
        rightLayout.addWidget(labelTts)
        rightLayout.addWidget(tts)

        layout.addWidget(imageBox)
        layout.addWidget(rightBox)
        layout.setStretch(0, 1)
        layout.setStretch(1, 3)

        self.sceneFrames.append(frame)
        self.sceneImages.append(imageBox)
        self.promptBoxes.append(prompt)

        return frame

    # ===================== RESPONSIVE STYLE =====================
    def applyResponsiveStyle(self):
        width = max(self.Widget.width(), 1200)
        height = max(self.Widget.height(), 720)

        scale = min(width / 1500, height / 900)
        scale = max(0.95, min(scale, 1.45))

        font = int(14 * scale)
        label_font = int(13 * scale)
        title_font = int(21 * scale)
        input_height = int(42 * scale)
        button_height = int(44 * scale)
        big_button_height = int(50 * scale)
        scene_height = int(235 * scale)
        image_height = int(165 * scale)
        prompt_height = int(90 * scale)

        for item in self.inputs:
            item.setMinimumHeight(input_height)

        for btn in self.buttons:
            btn.setMinimumHeight(button_height)

        for btn in [self.btnGrokAnalyze, self.btnAnalyzeYoutube, self.btnSeedAnalyze]:
            btn.setMinimumHeight(big_button_height)

        for frame in self.sceneFrames:
            frame.setMinimumHeight(scene_height)

        for img in self.sceneImages:
            img.setMinimumHeight(image_height)

        for prompt in self.promptBoxes:
            prompt.setMinimumHeight(prompt_height)

        style = """
        QWidget {
            background-color: #080d18;
            color: #e8eefc;
            font-family: Segoe UI;
            font-size: %dpx;
        }

        QFrame#leftFrame {
            background-color: #090f1d;
            border-radius: 10px;
        }

        QScrollArea#leftScroll {
            background-color: #090f1d;
            border: 1px solid #1f2a3d;
            border-radius: 10px;
        }

        QFrame#rightFrame {
            background-color: #080d18;
        }

        QLabel#leftLabel {
            color: #cfd8e8;
            font-size: %dpx;
            font-weight: 600;
        }

        QLabel#titleOption {
            font-size: %dpx;
            font-weight: 800;
            color: white;
            padding-top: 8px;
            padding-bottom: 4px;
        }

        QLabel#warningBox {
            background-color: #241f0d;
            border: 1px solid #78621c;
            color: #ffd36a;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
        }

        QLineEdit, QTextEdit, QComboBox {
            background-color: #111827;
            border: 1px solid #2d3a50;
            border-radius: 8px;
            padding-left: 12px;
            padding-right: 12px;
            color: white;
            selection-background-color: #8b35e8;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #9b4dff;
        }

        QPushButton {
            background-color: #8b35e8;
            color: white;
            border: none;
            border-radius: 8px;
            padding-left: 12px;
            padding-right: 12px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #a855f7;
        }

        QPushButton#bigPurpleButton {
            background-color: #9b4dff;
            font-weight: 800;
        }

        QTabWidget::pane {
            border: 1px solid #263449;
            background-color: #080d18;
            border-radius: 8px;
        }

        QTabBar::tab {
            background-color: #111827;
            color: white;
            min-width: 210px;
            padding: 13px 24px;
            border: 1px solid #334155;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 800;
        }

        QTabBar::tab:selected {
            background-color: #9b4dff;
        }

        QFrame#refFrame {
            border: 1px solid #00b050;
            border-radius: 12px;
            background-color: #081120;
        }

        QLabel#refImageBox {
            border: 1px solid #334155;
            border-radius: 8px;
            color: #cbd5e1;
            font-weight: 800;
        }

        QLabel#refText {
            color: #ffb000;
            font-weight: 800;
        }

        QFrame#sceneFrame {
            border: 1px dashed #c28a00;
            border-radius: 12px;
            background-color: #07101d;
        }

        QLabel#sceneImageBox {
            background-color: #030816;
            border: 1px solid #1f2937;
            border-radius: 8px;
            color: #cbd5e1;
            font-weight: 800;
        }

        QLabel#cyanLabel {
            color: #22d3ee;
            font-weight: 800;
        }

        QCheckBox {
            spacing: 8px;
            color: #e8eefc;
        }

        QCheckBox#sceneTitle {
            font-weight: 800;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }

        QScrollBar:vertical {
            background: #0b1220;
            width: 13px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #475569;
            min-height: 40px;
            border-radius: 6px;
        }

        QSplitter::handle {
            background-color: #1f2a3d;
            width: 4px;
        }
        """ % (font, label_font, title_font)

        self.Widget.setStyleSheet(style)


if __name__ == "__main__":
    import sys

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)

    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)

    Widget.showMaximized()
    sys.exit(app.exec_())