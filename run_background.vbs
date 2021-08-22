Set WshShell = CreateObject("WScript.shell")
WshShell.Run chr(34) & "run.bat" & chr(34), 0
Set WshShell = Nothing