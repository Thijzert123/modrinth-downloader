# Modrinth Downloader
This simple Python 3 application downloads given Minecraft Java mods and their dependencies from [Modrinth](https://modrinth.com). Things such as Minecraft version and mod loader can be configured individually.<br><br>
*Note: mods, resource packs, data packs, modpacks, shaders and plugins will from now on be reffered to as __projects__.*

## Setup
* Check if you have Python 3 installed on your system by running <code>python3 --version</code>. If Python is installed, you should see something along the lines of <code>Python 3.x.x</code> Note that the Python version should be at least 3.6.x in order for this program to work correctly.
<br>If, however you get an error message indicating that the command is not found, you should install now. If you are using Windows, go to https://www.python.org/downloads/latest, and download and run the installer. If you are using Linux, run the correct command for your Linux distribution:
```bash
# Debian-based (Ubuntu, Mint etc.)
apt install -y python3
# Arch Linux
pacman -S python313
```

* Clone the git repository and change directory:
```bash
git clone https://github.com/Thijzert123/modrinth-downloader.git && cd modrinth-downloader
```

* You now should be able to run the program:
```bash
python3 modrinth_downloader.py
```

## Usage
### Basic usage
To download Sodium Extra and their dependencies for a Minecraft 1.21 instance with Fabric, run:
```bash
python3 modrinth_downloader.py --version 1.21 --loader fabric --projects sodium-extra
```
This is going to download Sodium Extra and Sodium, because that is a required dependency.
#### Explanation:
* <code>--version</code> specifies what Minecraft version the mod is for. If more than one version is provided, the newest available will be downloaded, as long as it's one of these versions. <code>-v</code> can also be used instead.
* <code>--loader</code> specifies what loader the project is made for. For resource packs, use <code>minecraft</code>. For data packs, use <code>datapack</code>. <code>-l</code> or <code>--platform</code> can also be used instead.
* <code>--projects</code> specifies what projects should be downloaded. You can use the project name (such as <code>fabric-api</code>. This can be found in the searchbar when looking at a project) or project identifier (<code>P7dR8mSH</code>). These projects *must* meet the previous requirements (version and mod loader), otherwise the project entry will be skipped. <code>-p</code> can also be used instead.

### Advanced usage
* <code>-d</code>, <code>--directory</code> or <code>--destination</code> can be used to specify the output directory. If it doesn't exist, it will be created. However, if the specified output directory is a file, an error message is provided and the program stops.
* If the arguments <code>-r</code> or <code>--replace</code> are passed, the files will be replaced when they already exist. This is almost never useful, because it usually results in downloading the same file multiple times.
* When <code>-o</code>, <code>--optional</code> or <code>--optional-dependencies</code> are used, all the optional dependencies of projects will be downloaded. To avoid recursion problems, when a file exists it won't still download the dependencies.
* When <code>-s</code>, <code>--skip</code> or <code>--skip-dependencies</code> are used, no dependencies will ever be downloaded.

### Examples
Download Mod Menu and their dependencies for Fabric, Minecraft version 1.20.5:
```bash
python3 modrinth_downloader.py -v 1.20.5 -l fabric -p modmenu
```
Download Complementary Shaders Reimagined for Iris, Minecraft version 1.21.1:
```bash
python3 modrinth_downloader.py --version 1.20.5 --platform iris --project complementary-reimagined
```
Download Simple Voice Chat for Bungeecord, Minecraft version 1.17, but replace files when they already exist:
```bash
python3 modrinth_downloader.py -v 1.17 -l bungeecord -p simple-voice-chat -r
```
Download Reese's Sodium Options for NeoForge, Minecraft version 1.21.1, and download all optional dependencies:
```bash
python3 modrinth_downloader.py -v 1.21.1 -l neoforge -p reeses-sodium-options -o
```
Download Fresh Animations for Minecraft version 1.20.4 to <code>~/Downloads</code> and replace files if they already exist:
```bash
python3 modrinth_downloader.py -v 1.20.4 -l minecraft -p fresh-animations -d ~/Downloads -r
```

### Help info
You can also see the options and possible values you can pass by running <code>python3 modrinth_downloader.py --help</code>:
```
$ python3 modrinth_downloader.py --help
usage: modrinth_downloader.py [-h] [-d DIRECTORY] [-r] [-o] [-s] -l
                              {fabric,forge,neoforge,quilt,liteloader,modloader,rift,minecraft,datapack,canvas,iris,optifine,vanilla,bikkit,folia,spigot,paper,purpur,sponge,bungeecord,velocity,waterfall} -v
                              VERSIONS [VERSIONS ...] -p PROJECTS [PROJECTS ...]

Download Minecraft Java mods, resource packs, data packs, modpacks, shaders, plugins etc. and their dependencies from Modrinth

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY, --destination DIRECTORY
                        Directory the files will be placed in
  -r, --replace         Replace files when they already exist
  -o, --optional, --optional-dependencies
                        Also download all optional dependencies of a project
  -s, --skip, --skip-dependencies
                        Skip downloading dependencies of projects
  -l {fabric,forge,neoforge,quilt,liteloader,modloader,rift,minecraft,datapack,canvas,iris,optifine,vanilla,bikkit,folia,spigot,paper,purpur,sponge,bungeecord,velocity,waterfall}, --loader {fabric,forge,neoforge,quilt,liteloader,modloader,rift,minecraft,datapack,canvas,iris,optifine,vanilla,bikkit,folia,spigot,paper,purpur,sponge,bungeecord,velocity,waterfall}, --platform {fabric,forge,neoforge,quilt,liteloader,modloader,rift,minecraft,datapack,canvas,iris,optifine,vanilla,bikkit,folia,spigot,paper,purpur,sponge,bungeecord,velocity,waterfall}
                        The loader/platform you want your projects to support
  -v VERSIONS [VERSIONS ...], --versions VERSIONS [VERSIONS ...]
                        The Minecraft versions to look for for your projects
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
                        Projects to download. This can be the name (fabric-api) or project identifier (P7dR8mSH).
```

## Issues
If you have found a bug or want a new or changed feature, feel free to open an issue.