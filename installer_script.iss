[Setup]
AppName=XFollowingViews
AppVersion=1.0
DefaultDirName={pf}\XFollowingViews
DefaultGroupName=XFollowingViews
UninstallDisplayIcon={app}\XFollowingViews.exe
OutputDir=.
OutputBaseFilename=XFollowingViews_Installer
SetupIconFile=xfollowingviews.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\XFollowingViews.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "chromedriver.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XFollowingViews"; Filename: "{app}\XFollowingViews.exe"
Name: "{commondesktop}\XFollowingViews"; Filename: "{app}\XFollowingViews.exe"; Tasks: desktopicon
Name: "{group}\Uninstall XFollowingViews"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"
