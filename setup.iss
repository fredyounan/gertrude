; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define GertrudeVersion GetFileVersion("gertrude.exe")

[Setup]
AppName=Gertrude
AppVerName=Gertrude {#GertrudeVersion}
AppVersion={#GertrudeVersion}
AppPublisher=Bertrand Songis
AppPublisherURL=http://gertrude.creches.free.fr
AppSupportURL=http://gertrude.creches.free.fr
AppUpdatesURL=http://gertrude.creches.free.fr
VersionInfoVersion={#GertrudeVersion}
VersionInfoCompany=Bertrand Songis
VersionInfoProductName=Gertrude
AppCopyright=Copyright � 2005-2009 - Bertrand Songis

DefaultDirName={pf}\Gertrude
DefaultGroupName=Gertrude

OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

WizardImageBackColor=clWhite
SetupIconFile=bitmaps\setup_gertrude.ico
WizardImageFile=bitmaps\setup_gertrude.bmp
WizardSmallImageFile=bitmaps\setup_gertrude_mini.bmp
UninstallDisplayIcon={app}\gertrude.exe

[Messages]
BeveledLabel=Gertrude - v{#GertrudeVersion}

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[InstallDelete]
Type: files; Name: "{app}\*.py"
Type: files; Name: "{app}\*.pyc"
Type: files; Name: "{app}\*.log"

[Files]
Source: "dist\*";                 DestDir: "{app}";                 Flags: ignoreversion
Source: "dist\bitmaps\*";         DestDir: "{app}\bitmaps";         Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\templates_dist\*";  DestDir: "{app}\templates_dist";  Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\doc\*";             DestDir: "{app}\doc";             Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Gertrude";       Filename: "{app}\gertrude.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\Gertrude"; Filename: "{app}\gertrude.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\gertrude.exe"; Description: "{cm:LaunchProgram,Gertrude}"; Flags: nowait postinstall skipifsilent








