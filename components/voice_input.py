import streamlit as st


def inject_voice_listener() -> None:
    """
    Injects a JS message listener into the Streamlit page.
    Catches SET_VOICE_TOPIC postMessage and fills the topic input box.
    Call this once at the top of your app after set_page_config.
    """
    st.markdown("""
    <script>
    window.addEventListener("message", function(event) {
        if (event.data && event.data.type === "SET_VOICE_TOPIC") {
            var text   = event.data.value;
            var inputs = document.querySelectorAll('input[type="text"]');
            for (var i = 0; i < inputs.length; i++) {
                var ph = inputs[i].placeholder || "";
                if (ph.toLowerCase().includes("quantum") ||
                    ph.toLowerCase().includes("e.g")     ||
                    ph.toLowerCase().includes("topic")) {
                    var setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, "value"
                    ).set;
                    setter.call(inputs[i], text);
                    inputs[i].dispatchEvent(new Event("input",  { bubbles: true }));
                    inputs[i].dispatchEvent(new Event("change", { bubbles: true }));
                    break;
                }
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)


def render_voice_input() -> None:
    """
    Renders a mic button using the browser's Web Speech API.
    Uses st.iframe (replaces deprecated st.components.v1.html).
    Works on Chrome and Edge only.
    """

    voice_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: transparent;
            font-family: 'Segoe UI', sans-serif;
        }

        .wrapper {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 0;
        }

        .mic-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            border: 2px solid #232838;
            background: #111318;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.2s;
            outline: none;
        }
        .mic-btn:hover {
            border-color: #4fffb0;
            background: rgba(79,255,176,0.1);
        }
        .mic-btn.listening {
            border-color: #f87171;
            background: rgba(248,113,113,0.15);
            animation: pulse 1s infinite;
        }
        .mic-btn.success {
            border-color: #4fffb0;
            background: rgba(79,255,176,0.12);
        }

        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0   rgba(248,113,113,0.6); }
            70%  { box-shadow: 0 0 0 8px rgba(248,113,113,0);   }
            100% { box-shadow: 0 0 0 0   rgba(248,113,113,0);   }
        }

        .status {
            flex: 1;
            background: #111318;
            border: 1.5px solid #232838;
            border-radius: 10px;
            padding: 8px 14px;
            font-size: 13px;
            color: #6b7280;
            min-height: 40px;
            display: flex;
            align-items: center;
            transition: all 0.3s;
        }
        .status.listening { border-color: #f87171; color: #f87171; }
        .status.success   { border-color: #4fffb0; color: #e8eaf0; font-weight: 500; }
        .status.error     { border-color: #f87171; color: #f87171; }

        .use-btn {
            padding: 8px 16px;
            border-radius: 8px;
            border: none;
            background: linear-gradient(135deg, #4fffb0, #38bdf8);
            color: #0a0b0f;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            display: none;
            white-space: nowrap;
            transition: opacity 0.2s;
        }
        .use-btn:hover { opacity: 0.85; }
        .use-btn.show  { display: block; }

        .hint {
            font-size: 11px;
            color: #4b5563;
            margin-top: 5px;
            letter-spacing: 0.03em;
        }
    </style>
    </head>
    <body>

    <div class="wrapper">
        <button class="mic-btn" id="micBtn" onclick="toggleMic()">🎤</button>
        <div class="status"     id="statusBox">Click 🎤 to speak your research topic</div>
        <button class="use-btn" id="useBtn"   onclick="useTranscript()">Use ➤</button>
    </div>
    <div class="hint" id="hint">Chrome / Edge only · speak clearly after clicking the mic</div>

    <script>
    var recognition = null;
    var isListening = false;
    var finalText   = "";
    var interimText = "";

    var micBtn    = document.getElementById("micBtn");
    var statusBox = document.getElementById("statusBox");
    var useBtn    = document.getElementById("useBtn");
    var hint      = document.getElementById("hint");

    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SR) {
        statusBox.textContent = "⚠️ Not supported — use Chrome or Edge";
        statusBox.className   = "status error";
        micBtn.disabled       = true;
        micBtn.style.opacity  = "0.35";
        micBtn.style.cursor   = "not-allowed";
    } else {
        recognition = new SR();
        recognition.lang            = "en-US";
        recognition.continuous      = true;
        recognition.interimResults  = true;
        recognition.maxAlternatives = 3;

        recognition.onstart = function() {
            isListening = true;
            finalText   = "";
            interimText = "";
            micBtn.className      = "mic-btn listening";
            micBtn.textContent    = "⏹️";
            statusBox.className   = "status listening";
            statusBox.textContent = "🔴  Listening… speak now";
            useBtn.className      = "use-btn";
            hint.textContent      = "Speak clearly · click ⏹️ when done";
        };

        recognition.onresult = function(event) {
            finalText   = "";
            interimText = "";
            for (var i = 0; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalText += event.results[i][0].transcript + " ";
                } else {
                    interimText += event.results[i][0].transcript;
                }
            }
            var display = (finalText + interimText).trim();
            if (display) { statusBox.textContent = display; }
        };

        recognition.onend = function() {
            isListening = false;
            micBtn.textContent = "🎤";
            var result = finalText.trim() || interimText.trim();
            if (result) {
                finalText             = result;
                micBtn.className      = "mic-btn success";
                statusBox.className   = "status success";
                statusBox.textContent = "✅  " + result;
                useBtn.className      = "use-btn show";
                hint.textContent      = "Click 'Use ➤' to fill the search box";
            } else {
                micBtn.className      = "mic-btn";
                statusBox.className   = "status";
                statusBox.textContent = "Didn't catch that — try again";
                hint.textContent      = "Chrome / Edge only · speak clearly after clicking the mic";
            }
        };

        recognition.onerror = function(event) {
            isListening = false;
            micBtn.className   = "mic-btn";
            micBtn.textContent = "🎤";
            var msgs = {
                "not-allowed"   : "❌ Mic permission denied — allow mic in browser settings",
                "no-speech"     : "No speech heard — please try again",
                "network"       : "Network error — check your connection",
                "aborted"       : "Stopped",
                "audio-capture" : "No microphone found"
            };
            statusBox.className   = "status error";
            statusBox.textContent = msgs[event.error] || ("Error: " + event.error);
            hint.textContent      = "Click 🎤 to try again";
        };
    }

    function toggleMic() {
        if (!SR) return;
        if (isListening) {
            recognition.stop();
        } else {
            finalText   = "";
            interimText = "";
            micBtn.className = "mic-btn";
            useBtn.className = "use-btn";
            try {
                recognition.start();
            } catch(e) {
                recognition.stop();
                setTimeout(function(){ recognition.start(); }, 300);
            }
        }
    }

    function useTranscript() {
        if (!finalText.trim()) return;
        var text = finalText.trim();

        // postMessage to parent Streamlit window
        try {
            window.parent.postMessage({
                isStreamlitMessage : true,
                type               : "SET_VOICE_TOPIC",
                value              : text
            }, "*");
        } catch(e) {}

        // Also try direct DOM injection
        try {
            var inputs = window.parent.document.querySelectorAll('input[type="text"]');
            for (var i = 0; i < inputs.length; i++) {
                var ph = inputs[i].placeholder || "";
                if (ph.toLowerCase().includes("quantum") ||
                    ph.toLowerCase().includes("e.g")     ||
                    ph.toLowerCase().includes("topic")) {
                    var setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, "value"
                    ).set;
                    setter.call(inputs[i], text);
                    inputs[i].dispatchEvent(new Event("input",  { bubbles: true }));
                    inputs[i].dispatchEvent(new Event("change", { bubbles: true }));
                    break;
                }
            }
        } catch(e) {}

        statusBox.textContent = "⚡ Filled: " + text;
        useBtn.className      = "use-btn";
        micBtn.className      = "mic-btn";

        setTimeout(function() {
            statusBox.className   = "status";
            statusBox.textContent = "Click 🎤 to speak your research topic";
            hint.textContent      = "Chrome / Edge only · speak clearly after clicking the mic";
            finalText = "";
        }, 2000);
    }
    </script>
    </body>
    </html>
    """

    # ── Use st.iframe instead of deprecated components.html ───────────
    st.iframe(voice_html, height=75)