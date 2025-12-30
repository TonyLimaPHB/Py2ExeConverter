#define AppName "Conversor Python para EXE"
#define AppExeName "ConversorPythonEXE.exe"
#define AppVersion "1.0.0"
#define AppPublisher "Toni Lima"
#define AppURL "https://example.com"

[Setup]
AppId={{A9D0F9C1-8B1A-4E9C-A111-EXE00000001}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

OutputDir=output
OutputBaseFilename=ConversorPythonEXE_Setup
Compression=lzma
SolidCompression=yes

SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#AppExeName}

WizardStyle=modern
DisableProgramGroupPage=no
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "..\dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Executar {#AppName}"; Flags: nowait postinstall skipifsilent
