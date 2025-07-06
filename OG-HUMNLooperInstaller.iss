[Setup]
AppName=HUMN Video Looper
AppVersion=1.0
DefaultDirName={pf}\HUMN Video Looper
DefaultGroupName=HUMN Video Looper
OutputBaseFilename=HUMNLooperInstaller
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Files]
Source: "dist\\HUMNLooper\\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
Source: "dist\HUMNLooper\HUMNLooper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\HUMN Video Looper"; Filename: "{app}\HUMNLooper.exe"
Name: "{commondesktop}\HUMN Video Looper"; Filename: "{app}\HUMNLooper.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; Flags: unchecked

[Run]
Filename: "{app}\HUMNLooper.exe"; Description: "Launch HUMN Video Looper"; Flags: nowait postinstall skipifsilent