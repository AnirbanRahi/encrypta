active_button = """
border: 2px solid black;
background-color: black;
color: white;
font-weight: bold;
padding: 6px;
"""

inactive_button = """
border: 2px solid black;
background-color: white;
color: black;
font-weight: bold;
padding: 6px;
"""
line_style = """
background-color: white;
color: black;
font-weight: normal;
min-height: 30px;   
min-width: 300px;
border: 1px solid #a4a4a4;
border-left: none;
border-right: none;
border-top: none;
padding-left: 3px;
"""

enc_dec_button = """
QPushButton {
    border: 1.5px solid black;
    background-color: white;
    color: black;
    font-size: 20px;
    font-weight: bold;
    min-height: 30px;
}

QPushButton:hover {
    background-color: #b5b5b5;
}

QPushButton:pressed {
    background-color: #8f8f8f;
}
"""

icons = """
QPushButton {
    border: 1px solid #a4a4a4;
    background-color: white;
    color: black;
    border-left: none;
    border-right: none;
    border-top: none;
    
}

QPushButton:hover {
    background-color: #b5b5b5;
    border: 1px solid #b5b5b5;
    border-radius: 2px;
    
}

QPushButton:pressed {
    background-color: #8f8f8f;
    border: 1px solid #8f8f8f;
    border-radius: 2px;
}
"""