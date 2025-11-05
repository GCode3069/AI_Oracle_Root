'UseWindowsSpeechRecognition.ps1

# Enable Windows Speech Recognition
# This script allows voice control of the Oracle MCP Server
# Commands available: "generate horror story", "analyze YouTube videos", "create audio script"

Add-Type -AssemblyName System.Speech

# Set up speech recognition
$speechRecognitionEngine = New-Object System.Speech.Recognition.SpeechRecognitionEngine

# Load commands
$commands = New-Object System.Speech.Recognition.Choices
$commands.Add('generate horror story')
$commands.Add('analyze YouTube videos')
$commands.Add('create audio script')

$grammar = New-Object System.Speech.Recognition.Grammar($commands)
$speechRecognitionEngine.LoadGrammar($grammar)

# Set up text-to-speech
$speechSynthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Define what happens when a recognized command is heard
$speechRecognitionEngine.SpeechRecognized += { [void]$speechSynthesizer.Speak($_.Result.Text)
  switch ($_.Result.Text) {
    'generate horror story' {
      # Call your function to generate a horror story
      Generate-HorrorStory
    }
    'analyze YouTube videos' {
      # Call your function to analyze YouTube videos
      Analyze-YouTubeVideos
    }
    'create audio script' {
      # Call your function to create an audio script
      Create-AudioScript
    }
  }
}

# Start recognition
$speechRecognitionEngine.SetInputToDefaultAudioDevice()
$speechRecognitionEngine.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)

# Keep the script running
while ($true) { Start-Sleep -Seconds 1 }