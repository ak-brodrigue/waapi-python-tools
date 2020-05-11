 param (
    [Parameter(Mandatory=$true)][string]$path,
    [Parameter(Mandatory=$true)][string]$text
 )

Add-Type -AssemblyName System.Speech; 
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$synth.SetOutputToWaveFile($path);
$synth.Speak($text);
$synth.Dispose();