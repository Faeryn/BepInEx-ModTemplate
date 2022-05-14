# BepInEx ModTemplate

This script generates a BepInEx mod. The folder structure conforms to my [ModPacker](https://github.com/Faeryn/BepInEx-ModPacker) requirements, so it can be used to install or publish the mod.  
WARNING: This script is in a very early/PoC stage and may break in unexpected ways. Use at your own risk!

## Notes: 
* No SideLoader support (yet), you will have to do that manually after generating the project.
* Right now it only supports Outward. I'm planning to add more games later.
* The main Outward assembly reference points to `..\lib\Assembly-CSharp.dll`. The reason for this is that this way it's easier for Rider IDE's built-in decompiler. 
This also means you will either have to copy the `Assembly-CSharp.dll` from the game's folder, or remove this reference and use the one in the NuGet package. I will make this an option in a later release.

## Usage
1. Run the script with one argument, the folder where you keep your mod projects (for example `modgen.py C:\Workspace\ `).
2. Answer the questions. A few hints:
   * The questions have sensible defaults shown in (parentheses) after the question.
   * If you don't know what it is, you do not want to create a patcher project.
   * It's a good idea to accept generated mod GUID.
3. You may have to force refresh NuGet packages and/or manually reimport BepInEx.
