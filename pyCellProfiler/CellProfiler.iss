; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E6064576-236D-4C12-ACBD-BC8B606F9329}
AppName=CellProfiler
AppVerName=CellProfiler 2.0 r9051
AppPublisher=Broad Institute
AppPublisherURL=http://www.cellprofiler.org
AppSupportURL=http://www.cellprofiler.org
AppUpdatesURL=http://www.cellprofiler.org
DefaultDirName={pf}\CellProfiler
DefaultGroupName=CellProfiler
OutputDir=C:\cellprofiler\trunk\CellProfiler\pyCellProfiler\output
OutputBaseFilename=CellProfilerSetup
SetupIconFile=C:\cellprofiler\trunk\CellProfiler\pyCellProfiler\CellProfilerIcon.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\cellprofiler\trunk\CellProfiler\pyCellProfiler\dist\CellProfiler.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\cellprofiler\trunk\CellProfiler\pyCellProfiler\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\CellProfiler"; Filename: "{app}\CellProfiler.exe"
Name: "{group}\{cm:ProgramOnTheWeb,CellProfiler}"; Filename: "http://www.cellprofiler.org"
Name: "{group}\{cm:UninstallProgram,CellProfiler}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CellProfiler"; Filename: "{app}\CellProfiler.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CellProfiler.exe"; Description: "{cm:LaunchProgram,CellProfiler}"; Flags: nowait postinstall skipifsilent

