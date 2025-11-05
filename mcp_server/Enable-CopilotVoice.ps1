# Enable-CopilotVoice.ps1
# This script enables voice input for GitHub Copilot using Windows Speech Recognition.

# Initialize the Speech Recognition
Add-Type -AssemblyName System.Speech
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine

# Specify the commands for Copilot
$commands = @(
    "Generate a horror story",
    "Show YouTube analytics",
    "Create SSML audio",
    "Ask Copilot a general question"
)

# Setup Speech Recognition
$grammar = New-Object System.Speech.Recognition.Grammar
$grammarBuilder = New-Object System.Speech.Recognition.GrammarBuilder
$grammarBuilder.Append($commands) # Add the defined commands
$grammar = New-Object System.Speech.Recognition.Grammar($grammarBuilder)
$recognizer.LoadGrammar($grammar)

# Text-to-Speech feedback
function Speak {
    param([string]$text)
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.Speak($text)
}

# Event handling for recognized speech
$recognizer.SpeechRecognized += {
    Write-Host "Recognized command: $($_.Result.Text)"
    Speak "You said: $($_.Result.Text)"
    
    switch ($_.Result.Text) {
        "Generate a horror story" { 
            # Send command to Copilot for horror story generation
            # Copilot command execution goes here
        }
        "Show YouTube analytics" { 
            # Send command for YouTube analytics
            # Copilot command execution goes here
        }
        "Create SSML audio" { 
            # Send command to create SSML audio
            # Copilot command execution goes here
        }
        "Ask Copilot a general question" { 
            # Send command to ask a general question
            # Copilot command execution goes here
        }
    }
}

# Start listening
$recognizer.SetInputToDefaultAudioDevice()
$recognizer.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)

# Keep the script running
while ($true) {
    Start-Sleep -Seconds 1
}
