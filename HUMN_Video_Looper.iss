; HUMNLooper Installer Script
; Created for HUMN.audio 2025
; Generates a Start Menu shortcut, uninstaller, and proper copyright.
; No custom wizard images (uses Windows default)

[Setup]
AppName=HUMN Video Looper
AppVersion=1.0
AppPublisher=HUMN.audio
AppPublisherURL=https://humn.audio
AppSupportURL=https://humn.audio
AppUpdatesURL=https://humn.audio
DefaultDirName={autopf}\HUMN Video Looper
DefaultGroupName=HUMN Video Looper
OutputDir=dist\installer
OutputBaseFilename=HUMNLooperInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
UninstallDisplayIcon={app}\HUMNLooper.exe
SetupIconFile=humn_icon.ico
LicenseFile=LICENSE.txt
WizardSmallImageFile=
WizardImageFile=
AppCopyright=Made with ♥ by HUMN.audio 2025
SignTool=signtool sign /fd SHA256 /a /n "HUMN.audio, Inc." /tr http://timestamp.digicert.com /td SHA256 $f

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\HUMNLooper.exe";           DestDir: "{app}"; Flags: ignoreversion
Source: "humn_logo.png";                 DestDir: "{app}"; Flags: ignoreversion
Source: "README.md";                    DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt";                   DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\HUMN Video Looper"; Filename: "{app}\HUMNLooper.exe"; IconFilename: "{app}\humn_icon.ico"
Name: "{autodesktop}\HUMN Video Looper"; Filename: "{app}\HUMNLooper.exe"; IconFilename: "{app}\humn_icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\HUMNLooper.exe"; Description: "Launch HUMN Video Looper"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
// No code section needed for your setup

[Messages]
WelcomeLabel1=Welcome to the HUMN Video Looper Setup Wizard
FinishedLabel=Setup has finished installing HUMN Video Looper on your computer.
ClickFinish=Click Finish to exit Setup.

[INI]
Filename: "{app}\README.txt"; Section: "README"; Key: "Info"; String: "See https://humn.audio"

