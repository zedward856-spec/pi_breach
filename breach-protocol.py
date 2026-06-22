import gi
import random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

HEX_CODES = ["1C", "55", "BD", "E9", "FF", "7A", "42"]

class BreachProtocol(Gtk.Window):
    def __init__(self):
        super().__init__(title="Breach Protocol")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(40)
        self.fullscreen()
        self.connect("key-press-event", self.on_key_press)
        
        self.apply_css()
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        self.vbox.set_name("MainFrame")
        self.add(self.vbox)
        
        center_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        center_vbox.set_halign(Gtk.Align.CENTER)
        center_vbox.set_valign(Gtk.Align.CENTER)
        self.vbox.pack_start(center_vbox, True, True, 0)
        
        # Main Layout (Left and Right columns)
        main_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=25)
        main_hbox.set_halign(Gtk.Align.CENTER)
        main_hbox.set_valign(Gtk.Align.START)
        center_vbox.pack_start(main_hbox, False, False, 0)

        # LEFT COLUMN
        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10) # 10px gap between progress bar and code matrix
        left_col.set_halign(Gtk.Align.START)
        left_col.set_valign(Gtk.Align.START)
        main_hbox.pack_start(left_col, False, False, 0)

        # Timer
        timer_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        timer_container.set_halign(Gtk.Align.START)
        
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        top_bar.set_name("TopBar") # CSS gives this 10px padding-bottom, matching the gap above exactly!
        top_bar.set_halign(Gtk.Align.START)
        top_bar.set_size_request(466, -1)
        
        time_label = Gtk.Label(label="BREACH TIME REMAINING")
        time_label.set_name("TimeLabel")
        time_label.set_halign(Gtk.Align.START)
        
        self.timer_val = Gtk.Label(label="00:30:00")
        self.timer_val.set_name("TimerVal")
        
        top_bar.pack_start(time_label, False, False, 0)
        top_bar.pack_end(self.timer_val, False, False, 0)
        
        timer_container.pack_start(top_bar, False, False, 0)
        
        self.time_bar_container = Gtk.Box()
        self.time_bar_container.set_name("TimeBarContainer")
        self.time_bar_container.set_size_request(466, -1)
        
        self.time_bar = Gtk.ProgressBar()
        self.time_bar.set_name("TimeBar")
        self.time_bar.set_fraction(1.0)
        
        self.time_bar_container.pack_start(self.time_bar, True, True, 0)
        timer_container.pack_start(self.time_bar_container, False, False, 0)
        
        left_col.pack_start(timer_container, False, False, 0)

        # Left Panel (Code Matrix)
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        left_panel.set_name("LeftPanel")
        left_panel.set_halign(Gtk.Align.START)
        left_panel.set_valign(Gtk.Align.START)
        
        matrix_header = Gtk.Label(label="CODE MATRIX")
        matrix_header.set_name("MatrixHeader")
        matrix_header.set_halign(Gtk.Align.FILL)
        matrix_header.set_xalign(0.0)
        left_panel.pack_start(matrix_header, False, True, 0)
        
        self.grid_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid_container.set_name("GridContainer")
        self.grid_container.set_halign(Gtk.Align.CENTER)
        self.grid_container.set_valign(Gtk.Align.CENTER)
        left_panel.pack_start(self.grid_container, False, False, 0)
        
        left_col.pack_start(left_panel, False, False, 0)


        # RIGHT COLUMN
        right_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        right_col.set_valign(Gtk.Align.START)
        right_col.set_halign(Gtk.Align.START)
        right_col.set_margin_top(25)
        main_hbox.pack_start(right_col, False, False, 0)

        # Target Sequence
        target_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        target_container.set_valign(Gtk.Align.START)
        target_container.set_halign(Gtk.Align.START)
        
        target_header = Gtk.Label(label="SEQUENCE REQUIRED TO UPLOAD")
        target_header.set_name("TimeLabel")
        target_header.set_halign(Gtk.Align.START)
        
        self.target_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.target_box.set_name("TargetSequence")
        self.target_box.set_halign(Gtk.Align.START)
        self.target_box.set_size_request(460, 75)
        
        target_container.pack_start(target_header, False, False, 0)
        target_container.pack_start(self.target_box, False, False, 0)
        
        right_col.pack_start(target_container, False, False, 0)

        # Buffer and Controls
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        right_panel.set_valign(Gtk.Align.START)
        right_panel.set_halign(Gtk.Align.START)
        
        # BUFFER HEADER & BAR GROUP
        buffer_header_group = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        self.buffer_info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.buffer_info_box.set_size_request(460, -1)
        
        buffer_header = Gtk.Label(label="BUFFER")
        buffer_header.set_name("BufferHeader")
        buffer_header.set_halign(Gtk.Align.START)
        
        self.buffer_count_lbl = Gtk.Label(label="0/0")
        self.buffer_count_lbl.set_name("BufferCountLbl")
        
        self.buffer_info_box.pack_start(buffer_header, True, True, 0)
        self.buffer_info_box.pack_end(self.buffer_count_lbl, False, False, 0)
        
        buffer_header_group.pack_start(self.buffer_info_box, False, False, 0)
        
        self.buffer_bar_line = Gtk.Box()
        self.buffer_bar_line.set_name("BufferBarLine")
        self.buffer_bar_line.set_valign(Gtk.Align.CENTER)
        self.buffer_bar_line.set_size_request(460, 2)
        
        buffer_header_group.pack_start(self.buffer_bar_line, False, False, 0)
        
        self.buffer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.buffer_box.set_halign(Gtk.Align.START)
        self.buffer_box.set_size_request(460, 75)
        buffer_header_group.pack_start(self.buffer_box, False, False, 0)
        
        right_panel.pack_start(buffer_header_group, False, False, 0)
        
        # STATUS LABEL
        self.status_label = Gtk.Label(label="")
        self.status_label.set_name("StatusLabel")
        self.status_label.set_halign(Gtk.Align.CENTER)
        self.status_label.set_margin_top(15)
        right_panel.pack_start(self.status_label, False, False, 0)
        
        # FAILURE BAR
        self.failure_bar = Gtk.Box()
        self.failure_bar.set_name("FailureBar")
        self.failure_bar.set_margin_top(10)
        self.failure_bar.set_halign(Gtk.Align.FILL)
        right_panel.pack_start(self.failure_bar, False, False, 0)
        
        # BUTTONS
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        button_box.set_margin_top(20)
        button_box.set_halign(Gtk.Align.START)
        
        self.restart_btn = Gtk.Button(label="Reset")
        self.restart_btn.set_name("ActionBtn")
        self.restart_btn.connect("clicked", self.on_restart)
        
        self.shutdown_btn = Gtk.Button(label="Shutdown")
        self.shutdown_btn.set_name("ShutdownBtn")
        self.shutdown_btn.connect("clicked", lambda w: self.destroy())
        
        button_box.pack_start(self.restart_btn, False, False, 0)
        button_box.pack_start(self.shutdown_btn, False, False, 0)
        
        right_panel.pack_start(button_box, False, False, 0)
        
        right_col.pack_start(right_panel, False, False, 0)
        
        self.timer_id = None
        
        self.init_game_state()
        self.set_focus(None)
        
    def init_game_state(self, keep_difficulty=False):
        if not keep_difficulty:
            old_size = getattr(self, 'grid_size', None)
            sizes = [3, 4, 5]
            if old_size in sizes and len(sizes) > 1:
                sizes.remove(old_size)
            self.grid_size = random.choice(sizes)
            
            if self.grid_size == 3:
                self.max_time = 15.0
            elif self.grid_size == 4:
                self.max_time = 20.0
            else:
                self.max_time = 25.0
                
            self.target_size = random.randint(4, 6)
            self.buffer_size = self.target_size
        
        self.matrix = [[random.choice(HEX_CODES) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.buffer = []
        self.is_row_active = True
        self.active_index = 0
        self.game_over = False
        self.focus_r = 0
        self.focus_c = 0
        self.mouse_r = 0
        self.mouse_c = 0
        self.input_mode = "keyboard"
        
        self.target_seq = []
        r, c = 0, random.randint(0, self.grid_size-1)
        self.target_seq.append(self.matrix[r][c])
        visited = set([(r, c)])
        
        is_row = False
        for _ in range(self.target_size - 1):
            if is_row:
                avail = [cc for cc in range(self.grid_size) if (r, cc) not in visited]
                if not avail: break
                c = random.choice(avail)
            else:
                avail = [rr for rr in range(self.grid_size) if (rr, c) not in visited]
                if not avail: break
                r = random.choice(avail)
            
            visited.add((r, c))
            self.target_seq.append(self.matrix[r][c])
            is_row = not is_row
            
        for child in self.target_box.get_children():
            self.target_box.remove(child)
        self.target_labels = []
        for hex_code in self.target_seq:
            ev_box = Gtk.EventBox()
            ev_box.set_visible_window(False)
            ev_box.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
            ev_box.connect("enter-notify-event", self.on_target_hover_enter, hex_code)
            ev_box.connect("leave-notify-event", self.on_target_hover_leave, hex_code)
            
            lbl = Gtk.Label(label=hex_code)
            lbl.get_style_context().add_class("target-slot")
            lbl.set_size_request(75, 75)
            lbl.set_yalign(0.5)
            lbl.set_halign(Gtk.Align.CENTER)
            
            ev_box.add(lbl)
            self.target_box.pack_start(ev_box, False, False, 0)
            self.target_labels.append(lbl)
        self.target_box.show_all()
            
        self.rebuild_matrix_ui()
        self.status_label.set_text("")
        self.status_label.get_style_context().remove_class("success")
        self.status_label.get_style_context().remove_class("failed")
        self.failure_bar.get_style_context().remove_class("animate-bar")
        self.restart_btn.set_can_focus(False)
        self.shutdown_btn.set_can_focus(False)
        
        self.timer_started = False
        self.time_left = self.max_time
        self.timer_val.set_text(f"00:{int(self.max_time):02d}:00")
        if hasattr(self, 'time_bar'):
            self.time_bar.set_fraction(1.0)
        if self.timer_id:
            GLib.source_remove(self.timer_id)
        self.timer_id = GLib.timeout_add(10, self.update_timer)
        
        # Force GTK to spawn fresh buffer labels to prevent CSS animation caching bugs
        for child in self.buffer_box.get_children():
            self.buffer_box.remove(child)
        self.buffer_labels = []
        
        self.update_ui()
        self.update_focus_ui()
        
    def update_timer(self):
        if self.game_over:
            return False
        if not self.timer_started:
            return True
            
        self.time_left -= 0.01
        fraction = self.time_left / self.max_time
        if fraction < 0: fraction = 0
        self.time_bar.set_fraction(fraction)
        
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            self.status_label.set_text("Hack Failed")
            self.status_label.get_style_context().add_class("failed")
            self.restart_btn.set_can_focus(True)
            self.shutdown_btn.set_can_focus(True)
            self.restart_btn.grab_focus()
            self.trigger_failure_animation()
            self.update_ui()
            return False
        
        secs = int(self.time_left)
        millis = int((self.time_left - secs) * 100)
        self.timer_val.set_text(f"00:{secs:02d}:{millis:02d}")
        return True
        
    def rebuild_matrix_ui(self):
        for child in self.grid_container.get_children():
            self.grid_container.remove(child)
            
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(0)
        self.grid.set_row_spacing(0)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        
        self.buttons = []
        btn_size = 88
        
        for r in range(5):
            row_btns = []
            for c in range(5):
                btn = Gtk.Button(label="  ")
                btn.set_name("MatrixBtn")
                btn.set_size_request(btn_size, btn_size)
                
                if r < self.grid_size and c < self.grid_size:
                    btn.connect("clicked", self.on_btn_clicked, r, c)
                    btn.connect("enter-notify-event", self.on_btn_enter, r, c)
                else:
                    btn.set_sensitive(False)
                    btn.get_style_context().add_class("empty")
                    
                self.grid.attach(btn, c, r, 1, 1)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        self.grid_container.pack_start(self.grid, False, False, 0)
        self.grid_container.show_all()

    def apply_css(self):
        css = b"""
        window {
            background-color: #0e1115;
            color: #f7f7f7;
        }
        label {
            font-family: 'Noto Sans Mono', monospace;
        }
        #TopBar {
            padding-bottom: 10px;
        }
        #TimeBarContainer {
            border: 2px solid #dcf41b;
            padding: 0px;
            border-radius: 2px;
            background-color: rgba(220, 244, 27, 0.05);
        }
        progressbar#TimeBar {
            min-height: 10px;
        }
        progressbar#TimeBar trough {
            background-color: transparent;
            min-height: 10px;
            border: none;
            border-radius: 0px;
            padding: 0px;
            box-shadow: none;
            background-image: none;
        }
        progressbar#TimeBar progress {
            background-color: #dcf41b;
            border-radius: 0px;
            min-height: 10px;
            border: none;
            box-shadow: none;
            background-image: none;
            transition: all 10ms linear;
        }
        #TimeLabel, #TimerVal {
            color: #dcf41b;
            font-size: 24px;
            font-weight: bold;
        }
        #TimerVal {
            border: 2px solid #dcf41b;
            padding: 5px 15px;
            border-radius: 2px;
            background-color: rgba(220, 244, 27, 0.05);
        }
        #MatrixHeader {
            background-image: linear-gradient(135deg, transparent 8px, #dcf41b 8px);
            background-color: transparent;
            color: #000000;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 20px;
        }
        #StatusLabel {
            font-size: 24px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
        }
        #StatusLabel.success {
            color: #dcf41b;
        }
        #StatusLabel.failed {
            color: #ff003c;
        }
        #FailureBar {
            background-image: linear-gradient(to right, #ff003c, #ff003c);
            background-repeat: no-repeat;
            background-position: center bottom;
            min-height: 20px;
            background-size: 0% 20px;
        }
        #FailureBar.animate-bar {
            animation-name: grow-bar;
            animation-timing-function: linear;
            animation-fill-mode: forwards;
        }
        @keyframes grow-bar {
            0% { background-size: 0% 20px; }
            100% { background-size: 100% 20px; }
        }
        #LeftPanel {
            background-color: #12151a;
            border: 1px solid #293140;
        }
        #GridContainer {
            padding: 12px;
        }
        #TargetHeader, #BufferHeader {
            color: #dcf41b;
            font-size: 20px;
            font-weight: bold;
        }
        #BufferBarLine {
            background-color: #dcf41b;
        }
        #BufferCountLbl {
            color: #dcf41b;
            font-size: 20px;
            font-family: 'Noto Sans Mono', monospace;
            font-weight: bold;
        }
        #TargetSequence {
            margin-top: 10px;
            background-color: transparent;
        }
        .buffer-slot {
            background-color: transparent;
            color: rgba(220, 244, 27, 0.4);
            font-size: 28px;
            font-family: 'Noto Sans Mono', monospace;
            font-weight: bold;
            border: 2px dashed rgba(220, 244, 27, 0.4);
            padding: 0px;
            transition: all 200ms ease-in-out;
        }
        .target-slot {
            background-color: transparent;
            color: #ffffff;
            font-size: 28px;
            font-family: 'Noto Sans Mono', monospace;
            font-weight: bold;
            border: 2px solid #2a313d;
            padding: 0px;
        }
        .target-slot.matched {
            color: #42f554;
            border-color: #42f554;
            text-shadow: 0 0 5px rgba(66, 245, 84, 0.4);
            box-shadow: inset 0 0 10px rgba(66, 245, 84, 0.1);
        }
        .target-slot.hovered-target {
            border-color: #38bec9;
            box-shadow: 0 0 10px rgba(56, 190, 201, 0.6), inset 0 0 5px rgba(56, 190, 201, 0.4);
            color: #38bec9;
            font-weight: 900;
            text-shadow: 1px 0 0 #38bec9, 0 1px 0 #38bec9;
        }
        @keyframes fill-cyan-anim {
            0% {
                background-position: 100% 100%;
            }
            100% {
                background-position: 0% 0%;
            }
        }
        .buffer-slot.filled {
            border: 2px solid #dcf41b;
            color: #dcf41b;
            background-color: #1e2430;
            background-image: linear-gradient(150deg, transparent 30%, #38bec9 30%, #38bec9 70%, transparent 70%);
            background-repeat: no-repeat;
            background-size: 300% 300%;
            background-position: 0% 0%;
            animation-name: fill-cyan-anim;
            animation-duration: 0.7s;
            animation-timing-function: ease-in-out;
        }
        @keyframes rise-red {
            0% { background-position: 0px 150px; }
            100% { background-position: 0px -130px; }
        }
        .buffer-slot.filled.failed-buffer,
        .buffer-slot.failed-buffer {
            background-image: linear-gradient(to bottom, rgba(255,0,60,1), rgba(255,0,60,0));
            background-color: #1e2430;
            background-size: 100% 120px;
            background-repeat: no-repeat;
            background-position: 0px 150px;
            animation-name: rise-red;
            animation-duration: 0.5s;
            animation-timing-function: ease-out;
        }
        @keyframes rise-green {
            0% { background-position: 0px 150px; }
            100% { background-position: 0px -130px; }
        }
        .buffer-slot.filled.success-buffer,
        .buffer-slot.success-buffer {
            background-image: linear-gradient(to bottom, rgba(66,245,84,1), rgba(66,245,84,0));
            background-color: #1e2430;
            background-size: 100% 120px;
            background-repeat: no-repeat;
            background-position: 0px 150px;
            animation-name: rise-green;
            animation-duration: 0.5s;
            animation-timing-function: ease-out;
        }
        .failed-delay-0 { animation-delay: 0.0s; }
        .failed-delay-1 { animation-delay: 0.1s; }
        .failed-delay-2 { animation-delay: 0.2s; }
        .failed-delay-3 { animation-delay: 0.3s; }
        .failed-delay-4 { animation-delay: 0.4s; }
        .failed-delay-5 { animation-delay: 0.5s; }
        .failed-delay-6 { animation-delay: 0.6s; }
        .failed-delay-7 { animation-delay: 0.7s; }
        .failed-delay-8 { animation-delay: 0.8s; }
        .failed-delay-9 { animation-delay: 0.9s; }
        @keyframes blink-text {
            0% { color: #dcf41b; text-shadow: 1px 0 0 #dcf41b, -1px 0 0 #dcf41b; }
            49% { color: #dcf41b; text-shadow: 1px 0 0 #dcf41b, -1px 0 0 #dcf41b; }
            50% { color: transparent; text-shadow: 1px 0 0 transparent, -1px 0 0 transparent; }
            99% { color: transparent; text-shadow: 1px 0 0 transparent, -1px 0 0 transparent; }
            100% { color: #dcf41b; text-shadow: 1px 0 0 #dcf41b, -1px 0 0 #dcf41b; }
        }
        .buffer-slot.current-slot {
            border: 2px solid #38bec9;
            background-color: #1e2430;
            animation: blink-text 1.2s infinite;
        }
        #MatrixBtn, #MatrixBtn label {
            background-color: transparent;
            color: #dcf41b;
            font-size: 32px;
            font-family: 'Noto Sans Mono', monospace;
            font-weight: bold;
            border: 2px solid transparent;
            box-shadow: inset 0 0 0 1px transparent, inset 0 0 0 3px transparent;
            border-radius: 0px;
            transition: all 150ms ease-in-out;
        }
        #MatrixBtn.crosshair {
            background-color: rgba(220, 244, 27, 0.08);
        }
        #MatrixBtn.active-line {
            background-color: #2c3547;
            color: #dcf41b;
        }
        #MatrixBtn.active-line.crosshair {
            background-color: #3a465c;
        }
        #MatrixBtn:disabled, #MatrixBtn label:disabled {
            color: #dcf41b;
            opacity: 1.0;
        }
        #MatrixBtn.empty, #MatrixBtn.empty label:disabled {
            color: rgba(220, 244, 27, 0.4);
            opacity: 1.0;
        }
        #MatrixBtn.highlight-match {
            border-color: #dcf41b;
            box-shadow: 0 0 10px #dcf41b, inset 0 0 5px #dcf41b;
        }
        #MatrixBtn:hover, 
        #MatrixBtn.keyboard-focus,
        #MatrixBtn.active-line:hover,
        #MatrixBtn.active-line.keyboard-focus,
        #MatrixBtn.crosshair:hover,
        #MatrixBtn.crosshair.keyboard-focus,
        #MatrixBtn.active-line.crosshair:hover,
        #MatrixBtn.active-line.crosshair.keyboard-focus {
            background-color: #0e1115;
            color: #38bec9;
            border-color: #38bec9;
            box-shadow: inset 0 0 0 1px #0e1115, inset 0 0 0 3px #38bec9;
        }
        #MatrixBtn:hover label, 
        #MatrixBtn.keyboard-focus label,
        #MatrixBtn.active-line:hover label,
        #MatrixBtn.active-line.keyboard-focus label,
        #MatrixBtn.crosshair:hover label,
        #MatrixBtn.crosshair.keyboard-focus label,
        #MatrixBtn.active-line.crosshair:hover label,
        #MatrixBtn.active-line.keyboard-focus label {
            color: #38bec9;
            font-weight: 900;
            text-shadow: 1px 0 0 #38bec9, 0 1px 0 #38bec9;
        }
        #ActionBtn {
            background-color: transparent;
            background-image: 
                linear-gradient(-45deg, transparent 10px, #0e1115 10px),
                linear-gradient(-45deg, transparent 12px, #38bec9 12px);
            background-clip: padding-box, border-box;
            background-origin: padding-box, border-box;
            color: #38bec9;
            font-family: 'Noto Sans Mono', monospace;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid transparent;
            border-radius: 0px;
            padding: 10px 40px;
            outline: none;
        }
        #ActionBtn:hover, #ActionBtn:focus, #ActionBtn:active {
            background-image: 
                linear-gradient(-45deg, transparent 10px, #38bec9 10px),
                linear-gradient(-45deg, transparent 12px, #38bec9 12px);
            color: #000000;
        }
        #ShutdownBtn {
            background-color: transparent;
            background-image: 
                linear-gradient(-45deg, transparent 10px, #0e1115 10px),
                linear-gradient(-45deg, transparent 12px, #ff003c 12px);
            background-clip: padding-box, border-box;
            background-origin: padding-box, border-box;
            color: #ff003c;
            font-family: 'Noto Sans Mono', monospace;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid transparent;
            border-radius: 0px;
            padding: 10px 40px;
            outline: none;
        }
        #ShutdownBtn:hover, #ShutdownBtn:focus, #ShutdownBtn:active {
            background-image: 
                linear-gradient(-45deg, transparent 10px, #ff003c 10px),
                linear-gradient(-45deg, transparent 12px, #ff003c 12px);
            color: #ffffff;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_ui(self):
        match_len = 0
        if self.game_over and self.status_label.get_text() == "Hack Successful":
            match_len = len(self.target_seq)
        else:
            for i in range(1, len(self.target_seq) + 1):
                if i <= len(self.buffer):
                    if self.buffer[-i:] == self.target_seq[:i]:
                        match_len = i
                        
        if hasattr(self, 'target_labels'):
            for i, lbl in enumerate(self.target_labels):
                ctx = lbl.get_style_context()
                if i < match_len:
                    if not ctx.has_class("matched"):
                        ctx.add_class("matched")
                else:
                    if ctx.has_class("matched"):
                        ctx.remove_class("matched")

        if hasattr(self, 'buffer_count_lbl'):
            self.buffer_count_lbl.set_text(f"{len(self.buffer)}/{self.buffer_size}")

        if len(self.buffer_box.get_children()) != self.buffer_size:
            for child in self.buffer_box.get_children():
                self.buffer_box.remove(child)
            self.buffer_labels = []
            for i in range(self.buffer_size):
                lbl = Gtk.Label()
                lbl.get_style_context().add_class("buffer-slot")
                lbl.set_size_request(75, 75)
                self.buffer_box.pack_start(lbl, False, False, 0)
                self.buffer_labels.append(lbl)
            self.buffer_box.show_all()

        for i in range(self.buffer_size):
            lbl = self.buffer_labels[i]
            ctx = lbl.get_style_context()
            
            if not self.game_over:
                if ctx.has_class("failed-buffer"):
                    ctx.remove_class("failed-buffer")
                if ctx.has_class("success-buffer"):
                    ctx.remove_class("success-buffer")
                for j in range(10):
                    if ctx.has_class(f"failed-delay-{j}"):
                        ctx.remove_class(f"failed-delay-{j}")
            
            if i < len(self.buffer):
                lbl.set_text(self.buffer[i])
                lbl.set_yalign(0.5)
                if not ctx.has_class("filled"):
                    ctx.add_class("filled")
                if ctx.has_class("current-slot"):
                    ctx.remove_class("current-slot")
            elif i == len(self.buffer) and not self.game_over:
                lbl.set_text("___")
                lbl.set_yalign(0.93)
                if not ctx.has_class("current-slot"):
                    ctx.add_class("current-slot")
                if ctx.has_class("filled"):
                    ctx.remove_class("filled")
            else:
                lbl.set_text("  ")
                lbl.set_yalign(0.5)
                if ctx.has_class("filled"):
                    ctx.remove_class("filled")
                if ctx.has_class("current-slot"):
                    ctx.remove_class("current-slot")
                
        
        for r in range(5):
            for c in range(5):
                btn = self.buttons[r][c]
                context = btn.get_style_context()
                
                if context.has_class("active-line"):
                    context.remove_class("active-line")
                if context.has_class("empty"):
                    context.remove_class("empty")
                    
                is_active_line = False
                if not self.game_over:
                    if self.is_row_active and r == self.active_index:
                        is_active_line = True
                    elif not self.is_row_active and c == self.active_index:
                        is_active_line = True
                        
                if is_active_line:
                    context.add_class("active-line")
                
                if r >= self.grid_size or c >= self.grid_size:
                    btn.set_label("  ")
                    context.add_class("empty")
                    btn.set_sensitive(False)
                else:
                    if self.matrix[r][c] is None:
                        btn.set_label("[]")
                        context.add_class("empty")
                        btn.set_sensitive(False)
                    else:
                        btn.set_label(self.matrix[r][c])
                        btn.set_sensitive(is_active_line)
                            
        self.update_focus_ui()
        
    def update_focus_ui(self):
        active_r, active_c = None, None
        mode = getattr(self, 'input_mode', None)
        if mode == "keyboard":
            active_r, active_c = getattr(self, 'focus_r', None), getattr(self, 'focus_c', None)
        elif mode == "mouse":
            active_r, active_c = getattr(self, 'mouse_r', None), getattr(self, 'mouse_c', None)
            
        for r in range(5):
            for c in range(5):
                ctx = self.buttons[r][c].get_style_context()
                if ctx.has_class("keyboard-focus"):
                    ctx.remove_class("keyboard-focus")
                if ctx.has_class("crosshair"):
                    ctx.remove_class("crosshair")
                    
                if active_r is not None and active_c is not None and not self.game_over:
                    if r == active_r or c == active_c:
                        ctx.add_class("crosshair")
                        
                    if r == active_r and c == active_c:
                        is_valid = True
                        if self.matrix[r][c] is None: is_valid = False
                        if self.is_row_active and r != self.active_index: is_valid = False
                        if not self.is_row_active and c != self.active_index: is_valid = False
                        
                        if is_valid:
                            ctx.add_class("keyboard-focus")
                        
    def check_win_condition(self):
        target_len = len(self.target_seq)
        buffer_len = len(self.buffer)
        
        if self.buffer == self.target_seq:
            self.game_over = True
            self.status_label.set_text("Hack Successful")
            self.status_label.get_style_context().add_class("success")
            self.restart_btn.set_can_focus(True)
            self.shutdown_btn.set_can_focus(True)
            self.restart_btn.grab_focus()
            self.trigger_success_animation()
            return
            
        # Check if buffer is a strict prefix of the target sequence
        is_prefix = True
        for i in range(buffer_len):
            if i >= target_len or self.buffer[i] != self.target_seq[i]:
                is_prefix = False
                break
                
        if not is_prefix or buffer_len >= self.buffer_size:
            self.game_over = True
            self.status_label.set_text("Hack Failed")
            self.status_label.get_style_context().add_class("failed")
            self.restart_btn.set_can_focus(True)
            self.shutdown_btn.set_can_focus(True)
            self.restart_btn.grab_focus()
            self.trigger_failure_animation()
            return

    def trigger_success_animation(self):
        for i, lbl in enumerate(self.buffer_labels):
            ctx = lbl.get_style_context()
            ctx.add_class("success-buffer")
            ctx.add_class(f"failed-delay-{i}")

    def trigger_failure_animation(self):
        for i, lbl in enumerate(self.buffer_labels):
            ctx = lbl.get_style_context()
            ctx.add_class("failed-buffer")
            ctx.add_class(f"failed-delay-{i}")
            
        max_delay = (len(self.buffer_labels) - 1) * 0.1
        total_time_s = max_delay + 0.5
        
        # Dynamically sync the progress bar duration to the exact cascade time
        provider = Gtk.CssProvider()
        css = f"#FailureBar.animate-bar {{ animation-duration: {total_time_s}s; }}"
        provider.load_from_data(css.encode('utf-8'))
        self.failure_bar.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        self.failure_bar.get_style_context().add_class("animate-bar")

    def on_btn_enter(self, widget, event, r, c):
        if self.game_over: return False
        self.input_mode = "mouse"
        self.mouse_r = r
        self.mouse_c = c
        self.update_focus_ui()
        return False

    def on_btn_clicked(self, widget, r, c, is_keyboard=False):
        if self.game_over: return
        
        if not is_keyboard:
            self.input_mode = "mouse"
            
        if self.is_row_active and r != self.active_index: return
        if not self.is_row_active and c != self.active_index: return
        if self.matrix[r][c] is None: return
        
        self.timer_started = True
        
        val = self.matrix[r][c]
        self.buffer.append(val)
        self.matrix[r][c] = None 
        
        old_r, old_c = r, c
        self.is_row_active = not self.is_row_active
        self.active_index = r if self.is_row_active else c
        
        if self.is_row_active:
            left_valid = [c_idx for c_idx in range(old_c - 1, -1, -1) if self.matrix[self.active_index][c_idx] is not None]
            right_valid = [c_idx for c_idx in range(old_c + 1, self.grid_size) if self.matrix[self.active_index][c_idx] is not None]
            
            if left_valid and right_valid:
                dist_l = old_c - left_valid[0]
                dist_r = right_valid[0] - old_c
                if dist_l < dist_r:
                    self.focus_r, self.focus_c = self.active_index, left_valid[0]
                elif dist_r < dist_l:
                    self.focus_r, self.focus_c = self.active_index, right_valid[0]
                else:
                    if len(right_valid) >= len(left_valid):
                        self.focus_r, self.focus_c = self.active_index, right_valid[0]
                    else:
                        self.focus_r, self.focus_c = self.active_index, left_valid[0]
            elif right_valid:
                self.focus_r, self.focus_c = self.active_index, right_valid[0]
            elif left_valid:
                self.focus_r, self.focus_c = self.active_index, left_valid[0]
            else:
                self.focus_r, self.focus_c = self.active_index, old_c
        else:
            up_valid = [r_idx for r_idx in range(old_r - 1, -1, -1) if self.matrix[r_idx][self.active_index] is not None]
            down_valid = [r_idx for r_idx in range(old_r + 1, self.grid_size) if self.matrix[r_idx][self.active_index] is not None]
            
            if up_valid and down_valid:
                dist_u = old_r - up_valid[0]
                dist_d = down_valid[0] - old_r
                if dist_u < dist_d:
                    self.focus_r, self.focus_c = up_valid[0], self.active_index
                elif dist_d < dist_u:
                    self.focus_r, self.focus_c = down_valid[0], self.active_index
                else:
                    if len(down_valid) >= len(up_valid):
                        self.focus_r, self.focus_c = down_valid[0], self.active_index
                    else:
                        self.focus_r, self.focus_c = up_valid[0], self.active_index
            elif down_valid:
                self.focus_r, self.focus_c = down_valid[0], self.active_index
            elif up_valid:
                self.focus_r, self.focus_c = up_valid[0], self.active_index
            else:
                self.focus_r, self.focus_c = old_r, self.active_index
                    
        self.check_win_condition()
        self.update_ui()

    def on_key_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.destroy()
            return True
            
        if self.game_over:
            return False
            
        if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            self.input_mode = "keyboard"
            if self.focus_r is not None:
                self.on_btn_clicked(self.buttons[self.focus_r][self.focus_c], self.focus_r, self.focus_c, is_keyboard=True)
            return True
            
        if keyval in (Gdk.KEY_Up, Gdk.KEY_Down, Gdk.KEY_Left, Gdk.KEY_Right):
            self.input_mode = "keyboard"
            if self.focus_r is None:
                self.focus_r = self.active_index if self.is_row_active else 0
                self.focus_c = 0 if self.is_row_active else self.active_index
            
            if self.is_row_active:
                if keyval == Gdk.KEY_Left:
                    for new_c in range(self.focus_c - 1, -1, -1):
                        if self.matrix[self.focus_r][new_c] is not None:
                            self.focus_c = new_c
                            break
                elif keyval == Gdk.KEY_Right:
                    for new_c in range(self.focus_c + 1, self.grid_size):
                        if self.matrix[self.focus_r][new_c] is not None:
                            self.focus_c = new_c
                            break
            else:
                if keyval == Gdk.KEY_Up:
                    for new_r in range(self.focus_r - 1, -1, -1):
                        if self.matrix[new_r][self.focus_c] is not None:
                            self.focus_r = new_r
                            break
                elif keyval == Gdk.KEY_Down:
                    for new_r in range(self.focus_r + 1, self.grid_size):
                        if self.matrix[new_r][self.focus_c] is not None:
                            self.focus_r = new_r
                            break
                
            self.update_focus_ui()
            return True
        return False

    def on_target_hover_enter(self, widget, event, hex_code):
        if self.game_over: return False
        lbl = widget.get_child()
        if lbl:
            lbl.get_style_context().add_class("hovered-target")
        for r in range(5):
            for c in range(5):
                if r < self.grid_size and c < self.grid_size:
                    if self.matrix[r][c] == hex_code:
                        self.buttons[r][c].get_style_context().add_class("highlight-match")
        return False

    def on_target_hover_leave(self, widget, event, hex_code):
        lbl = widget.get_child()
        if lbl:
            lbl.get_style_context().remove_class("hovered-target")
        for r in range(5):
            for c in range(5):
                if r < self.grid_size and c < self.grid_size:
                    if self.matrix[r][c] == hex_code:
                        self.buttons[r][c].get_style_context().remove_class("highlight-match")
        return False

    def on_restart(self, widget):
        keep = False
        if getattr(self, 'game_over', False) and self.status_label.get_text() == "Hack Failed":
            keep = True
        self.init_game_state(keep_difficulty=keep)
        self.set_focus(None)

win = BreachProtocol()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
