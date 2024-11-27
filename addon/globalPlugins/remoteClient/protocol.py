from enum import Enum

class RemoteMessageType(Enum):
    # Connection and Protocol Messages
    protocol_version = "protocol_version"
    join = "join"
    channel_joined = "channel_joined"
    client_joined = "client_joined"
    client_left = "client_left"
    
    # Control Messages
    key = "key"
    speak = "speak"
    cancel = "cancel"
    pause_speech = "pause_speech"
    tone = "tone"
    wave = "wave"
    send_SAS = "send_SAS"  # Send Secure Attention Sequence
    
    # Display and Braille Messages
    display = "display"
    braille_input = "braille_input"
    set_braille_info = "set_braille_info"
    set_display_size = "set_display_size"
    
    # Clipboard Operations
    set_clipboard_text = "set_clipboard_text"
    
    # System Messages
    ping = "ping"
    error = "error"
    