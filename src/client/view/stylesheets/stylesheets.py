scroll_bar_vertical_stylesheet = """
    QScrollArea {
        background: none;
        border: none;
    }
    QScrollBar:vertical {
        background: transparent;
        width: 12px;
        margin-left: 5px;
    }
    QScrollBar::handle:vertical {
        background: #171717;
        min-height: 25px;
        border-radius: 2.5px;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: transparent;
        height: 20px;
        border-bottom-left-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
        margin-left: 5px;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: #2A2C2F;
        height: 20px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
        subcontrol-position: top;
        subcontrol-origin: margin;
        margin-left: 5px;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        background: #2A2C2F;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: #2A2C2F;
    }
"""
