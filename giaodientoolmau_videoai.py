import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
class SceneCard(QFrame):
    def __init__(self, index, active=False):
        super().__init__()
        self.index = index
        self.setObjectName("sceneCardActive" if active else "sceneCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.preview = QLabel(f"SCENE {index}")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setObjectName("previewBox")

        content = QVBoxLayout()
        content.setSpacing(5)

        title = QLabel(f"☑  CẢNH {index}")
        title.setObjectName("sceneTitle")

        prompt_label = QLabel("VIDEO PROMPT")
        prompt_label.setObjectName("blueLabel")

        self.prompt = QTextEdit()
        self.prompt.setPlainText(
            "anime style, vibrant colors, clean outlines, soft cel shading, "
            "detailed eyes, studio-quality anime frame, high-clarity character design. "
            "The character stands in a cinematic scene with expressive pose..."
        )
        self.prompt.setObjectName("promptBox")

        audio_label = QLabel("AUDIO / TTS")
        audio_label.setObjectName("blueLabel")

        audio = QLabel("I am pregnant!")
        audio.setObjectName("audioText")

        content.addWidget(title)
        content.addWidget(prompt_label)
        content.addWidget(self.prompt)
        content.addWidget(audio_label)
        content.addWidget(audio)

        layout.addWidget(self.preview)
        layout.addLayout(content, 1)

    def apply_responsive(self, scale, parent_width):
        preview_w = int(max(190, min(parent_width * 0.18, 330)))
        preview_h = int(preview_w * 0.52)

        self.preview.setFixedSize(preview_w, preview_h)
        self.prompt.setFixedHeight(int(70 * scale))
        self.setFixedHeight(int(max(155 * scale, preview_h + 35)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene_cards = []

        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_w = screen.width()
        self.screen_h = screen.height()
        self.scale = self.get_scale()

        self.setWindowTitle("AI Generate Tool - PyQt5")
        self.setMinimumSize(1100, 700)

        main = QWidget()
        self.setCentralWidget(main)

        root = QVBoxLayout(main)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self.create_topbar())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.sidebar = self.create_sidebar()
        self.content_frame = self.create_content()

        body.addWidget(self.sidebar)
        body.addWidget(self.content_frame, 1)

        root.addLayout(body, 1)

        self.setStyleSheet(self.qss())
        self.apply_responsive_sizes()

    def get_scale(self):
        return max(0.85, min(self.screen_w / 1920, self.screen_h / 1080, 1.25))

    def s(self, value):
        return int(value * self.scale)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_responsive_sizes()

    def apply_responsive_sizes(self):
        if not hasattr(self, "sidebar"):
            return

        w = max(self.width(), 1100)
        h = max(self.height(), 700)

        self.scale = max(0.85, min(w / 1920, h / 1080, 1.25))

        sidebar_w = int(max(230, min(w * 0.155, 340)))
        self.sidebar.setFixedWidth(sidebar_w)

        content_w = max(self.content_frame.width(), 800)

        for card in self.scene_cards:
            card.apply_responsive(self.scale, content_w)

    def create_topbar(self):
        top = QFrame()
        top.setObjectName("topbar")
        top.setFixedHeight(self.s(52))

        layout = QHBoxLayout(top)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        menu = QPushButton("☰")
        menu.setFixedSize(self.s(34), self.s(34))
        menu.setObjectName("iconBtn")

        title = QLabel("🌀 AI Generate Tool")
        title.setObjectName("appTitle")

        btn1 = QPushButton("Chế độ Banana Pro tạo ảnh")
        btn2 = QPushButton("Chế độ Veo3 tạo video")
        btn2.setObjectName("purpleBtn")

        layout.addWidget(menu)
        layout.addWidget(title)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addStretch()

        lang = QComboBox()
        lang.addItems(["Tiếng Việt (Vietnamese)", "English"])
        lang.setFixedWidth(self.s(190))

        version = QLabel("v1.5.9")

        new = QPushButton("● New")
        help_btn = QPushButton("?")
        help_btn.setFixedSize(self.s(34), self.s(34))

        layout.addWidget(lang)
        layout.addWidget(version)
        layout.addWidget(new)
        layout.addWidget(help_btn)

        return top

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        box = QWidget()
        box.setObjectName("sidebarBox")

        layout = QVBoxLayout(box)
        layout.setContentsMargins(10, 10, 10, 12)
        layout.setSpacing(8)

        open_btn = QPushButton("📁 Mở thư mục xuất này")
        open_btn.setObjectName("blueBtn")
        layout.addWidget(open_btn)

        output = QLabel("Output: C:\\Users\\Admin\\Desktop\\VIDEO AI")
        output.setObjectName("smallBlue")
        layout.addWidget(output)

        layout.addWidget(self.line())

        layout.addWidget(self.section_title("TÙY CHỌN KỊCH BẢN"))
        layout.addWidget(QLabel("Phong cách hình ảnh/video"))
        layout.addWidget(self.combo(["Anime Style", "Hyper Realistic", "Cinematic"]))

        layout.addWidget(QLabel("Ngôn ngữ kịch bản và giọng nói"))
        layout.addWidget(self.combo(["us English", "Vietnamese"]))

        layout.addWidget(QLabel("Tỷ lệ copy từ video gốc"))
        layout.addWidget(self.combo(["100% - Copy hoàn toàn", "50% - Copy một nửa"]))

        layout.addWidget(self.switch_row("Bật tùy chỉnh thời lượng", False))
        layout.addWidget(self.switch_row("Ảnh tham chiếu", True))
        layout.addWidget(self.switch_row("Đồng nhất giọng nhân vật", True))

        layout.addWidget(QLabel("Giọng nhân vật đồng nhất"))
        layout.addWidget(self.combo(["Achenar - Female, soft", "Male Voice"]))

        layout.addWidget(QLabel("Mô hình về ảnh tham chiếu"))
        layout.addWidget(self.combo(["🍌 Nano Banana Pro", "Gemini Flash"]))

        layout.addWidget(self.switch_row("Hạn chế vi phạm ảnh tham chiếu", True))
        layout.addWidget(self.switch_row("Sinh nhạc nền (BGM)", True))

        layout.addWidget(self.line())

        layout.addWidget(self.section_title("TÙY CHỌN VIDEO"))
        layout.addWidget(self.switch_row("Chế độ tự động xoay profile NST", False))
        layout.addWidget(QLabel("Chọn luồng chạy (NST)"))
        layout.addWidget(self.combo(["1 luồng", "2 luồng", "4 luồng", "8 luồng"]))

        layout.addStretch()

        scroll.setWidget(box)

        wrap = QVBoxLayout(sidebar)
        wrap.setContentsMargins(0, 0, 0, 0)
        wrap.addWidget(scroll)

        return sidebar

    def create_content(self):
        content = QFrame()
        content.setObjectName("content")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        self.input_link = QLineEdit()
        self.input_link.setText("https://www.youtube.com/shorts/bQic0POmBHA")
        self.input_link.setObjectName("bigInput")
        layout.addWidget(self.input_link)

        desc = QLineEdit()
        desc.setPlaceholderText("Mô tả thêm (tùy chọn)...")
        desc.setObjectName("bigInput")
        layout.addWidget(desc)

        analyze = QPushButton("🐱 PHÂN TÍCH TỪ YOUTUBE")
        analyze.setFixedHeight(self.s(42))
        analyze.setObjectName("mainPurpleBtn")
        layout.addWidget(analyze)

        actions = QHBoxLayout()
        actions.setSpacing(8)

        for text in [
            "⏳ Đang xử lý... (2/13)",
            "🎬 Ghép Video",
            "🎞 Ghép cảnh đã chọn (0)",
            "⚡ Đang chạy Combo 3...",
            "✏ Sửa tất cả lỗi",
            "➕ Thêm kịch bản",
        ]:
            btn = QPushButton(text)
            btn.setObjectName("actionBtn")
            btn.setMinimumHeight(self.s(30))
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            actions.addWidget(btn)

        actions.addStretch()
        layout.addLayout(actions)

        master = QFrame()
        master.setObjectName("masterBox")
        master.setFixedHeight(self.s(82))

        master_layout = QHBoxLayout(master)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setSpacing(10)

        img = QLabel("ẢNH THAM CHIẾU")
        img.setFixedWidth(self.s(250))
        img.setAlignment(Qt.AlignCenter)
        img.setObjectName("previewBox")

        txt = QLabel(
            "MEO ME (Adult female cat, white fur, red dress...) "
            "MEO BO (Adult male cat, orange tabby fur, strong posture...)"
        )
        txt.setWordWrap(True)
        txt.setObjectName("orangeText")

        master_layout.addWidget(img)
        master_layout.addWidget(txt, 1)
        layout.addWidget(master)

        scene_scroll = QScrollArea()
        scene_scroll.setWidgetResizable(True)
        scene_scroll.setFrameShape(QFrame.NoFrame)

        scene_box = QWidget()
        scene_box.setObjectName("sceneBox")

        scene_layout = QVBoxLayout(scene_box)
        scene_layout.setContentsMargins(0, 0, 0, 0)
        scene_layout.setSpacing(10)

        for i in range(1, 8):
            card = SceneCard(i, active=(i == 1))
            self.scene_cards.append(card)
            scene_layout.addWidget(card)

        scene_layout.addStretch()
        scene_scroll.setWidget(scene_box)

        layout.addWidget(scene_scroll, 1)

        return content

    def combo(self, items):
        cb = QComboBox()
        cb.addItems(items)
        cb.setFixedHeight(self.s(32))
        return cb

    def switch_row(self, text, checked=False):
        row = QFrame()
        row.setObjectName("switchRow")

        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 3, 8, 3)

        label = QLabel(text)
        check = QCheckBox()
        check.setChecked(checked)

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(check)

        return row

    def section_title(self, text):
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    def line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("line")
        return line

    def qss(self):
        font_size = max(11, min(int(13 * self.scale), 15))
        small_size = max(9, min(int(11 * self.scale), 13))
        title_size = max(14, min(int(18 * self.scale), 22))

        return f"""
        QMainWindow {{
            background-color: #07111f;
        }}

        QWidget#sidebarBox,
        QWidget#sceneBox {{
            background-color: transparent;
        }}

        QLabel {{
            color: #e5e7eb;
            font-size: {font_size}px;
        }}

        #topbar {{
            background-color: #050b16;
            border-bottom: 1px solid #1e293b;
        }}

        #appTitle {{
            color: #38bdf8;
            font-size: {title_size}px;
            font-weight: bold;
        }}

        #sidebar {{
            background-color: #07111f;
            border-right: 1px solid #243244;
        }}

        #content {{
            background-color: #0b1224;
        }}

        QPushButton {{
            background-color: #1e293b;
            color: white;
            border: 1px solid #334155;
            border-radius: 7px;
            padding: 6px 10px;
            font-size: {font_size}px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: #334155;
        }}

        #blueBtn {{
            background-color: #2684ff;
            border: none;
        }}

        #purpleBtn, #mainPurpleBtn {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #7c3aed,
                stop:1 #c084fc
            );
            border: none;
        }}

        #mainPurpleBtn {{
            font-size: {font_size}px;
        }}

        #actionBtn {{
            background-color: #9333ea;
            border: none;
            font-size: {small_size}px;
        }}

        #iconBtn {{
            background-color: #111827;
            border-radius: 8px;
            font-size: {title_size}px;
        }}

        QLineEdit, QTextEdit, QComboBox {{
            background-color: #111827;
            color: white;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 6px;
            font-size: {font_size}px;
        }}

        #bigInput {{
            min-height: 28px;
        }}

        #sectionTitle {{
            font-size: {font_size + 2}px;
            font-weight: bold;
            color: white;
            margin-top: 8px;
        }}

        #smallBlue {{
            color: #60a5fa;
            font-size: {small_size}px;
        }}

        #switchRow {{
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 8px;
        }}

        #masterBox {{
            background-color: rgba(15, 23, 42, 180);
            border: 1px solid #16a34a;
            border-radius: 10px;
        }}

        #sceneCard {{
            background-color: rgba(15, 23, 42, 220);
            border: 1px dashed #f59e0b;
            border-radius: 12px;
        }}

        #sceneCardActive {{
            background-color: rgba(15, 23, 42, 230);
            border: 1px solid #22c55e;
            border-radius: 12px;
        }}

        #previewBox {{
            background-color: #020617;
            color: #94a3b8;
            border-radius: 8px;
            border: 1px solid #334155;
            font-weight: bold;
        }}

        #sceneTitle {{
            color: #bfdbfe;
            font-weight: bold;
            font-size: {small_size}px;
        }}

        #blueLabel {{
            color: #38bdf8;
            font-size: {small_size}px;
            font-weight: bold;
        }}

        #promptBox {{
            background-color: transparent;
            border: none;
            color: white;
            font-style: italic;
        }}

        #audioText {{
            color: white;
            font-weight: bold;
            font-size: {small_size}px;
        }}

        #orangeText {{
            color: #f59e0b;
            font-weight: bold;
            font-size: {small_size}px;
        }}

        #line {{
            background-color: #334155;
        }}

        QScrollArea {{
            background: transparent;
            border: none;
        }}

        QScrollBar:vertical {{
            background: #0f172a;
            width: 10px;
        }}

        QScrollBar::handle:vertical {{
            background: #475569;
            border-radius: 5px;
        }}
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())