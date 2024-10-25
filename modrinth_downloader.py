#!/usr/bin/python3

#
# By Thijzert
#

import requests
import platform
import os
import json
import shutil
import sys
import argparse
import pathlib

# The project downloader. Returns True if the mod and its dependencies have successfully been downloaded.
# minecraftLoader: loader/platform to look for
# minecraftVersions: list of versions to look for
# projectID: id of project that should be downloaded, can be name or Modrinth identifier
# optionalDependencies: whether optional dependencies should be downloaded
# skipDependencies: whether dependencies should be downloaded
# outputDir: output directory, made if non-existent
# replaceFiles: whether files should be replaced
def downloadProject(minecraftLoader, minecraftVersions, projectID, optionalDependencies = False, skipDependencies = False, outputDir = ".", replaceFiles = False):
    if not os.path.isdir(outputDir):
        if os.path.isfile(outputDir):
            print(f"Output directory is a file: {outputDir}")
            exit(1)
        else:
            pathlib.Path(outputDir).mkdir(parents=True, exist_ok=True)

    minecraftVersionsSearch = str(minecraftVersions).replace("'", '"')
    searchURL = f'https://api.modrinth.com/v2/project/{projectID}/version?loaders=["{minecraftLoader}"]&game_versions={minecraftVersionsSearch}'
    r = requests.get(searchURL)
    statusCode = r.status_code
    if statusCode == 404:
        print(f"Project {projectID} doesn't exist, skipping")
        return False
    elif statusCode != 200:
        print(f"Error code {statusCode} while processing {projectID}, skipping")
    projectDetails = r.json()
    if len(projectDetails) == 0:
        print(f"No {projectID} version found for {minecraftLoader} or Minecraft versions {minecraftVersions}, skipping")
        return False
    
    projectID = projectDetails[0]["project_id"]

    projectName = projectDetails[0]["name"]
    projectVersion = projectDetails[0]["version_number"]
    jarURL = projectDetails[0]["files"][0]["url"]
    filename = projectDetails[0]["files"][0]["filename"]
    filepath = os.path.join(outputDir, filename)
    if os.path.exists(filepath) and replaceFiles == False:
        print(f"File {filepath} already exists, skipping {projectID} ({projectName}) version {projectVersion}")
        if optionalDependencies:
            return False
    else:
        print(f"Downloading {projectID} ({projectName}) version {projectVersion} to {filepath}")
        open(filepath, "wb").write(requests.get(jarURL).content)

    successful = True
    if skipDependencies == False:
        projectDependencies = projectDetails[0]["dependencies"]
        if projectDependencies:
            for x in range(len(projectDependencies)):
                if projectDependencies[x]["dependency_type"] == "required" or (projectDependencies[x]["dependency_type"] == "optional" and optionalDependencies):
                    if downloadProject(minecraftLoader, minecraftVersions, projectDependencies[x]["project_id"], optionalDependencies, skipDependencies, outputDir, replaceFiles) == False:
                        successful = False

    return successful


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Download Minecraft Java mods, resource packs, data packs, modpacks, shaders, plugins etc. and their dependencies from Modrinth")
    argparser.add_argument("-d", "--directory", "--destination", default=".", help="Directory the files will be placed in")
    argparser.add_argument("-r", "--replace", action="store_true", help="Replace files when they already exist")
    argparser.add_argument("-o", "--optional", "--optional-dependencies", action="store_true", help="Also download all optional dependencies of a project")
    argparser.add_argument("-s", "--skip", "--skip-dependencies", action="store_true", help="Skip downloading dependencies of projects")
    argparser.add_argument("-l", "--loader", "--platform", required=True, choices=["fabric", "forge", "neoforge", "quilt", "liteloader", "modloader", "rift", "minecraft", "datapack", "canvas", "iris", "optifine", "vanilla", "bikkit", "folia", "spigot", "paper", "purpur", "sponge", "bungeecord", "velocity", "waterfall"], help="The loader/platform you want your projects to support")
    argparser.add_argument("-v", "--versions", required=True, nargs="+", help="The Minecraft versions to look for for your projects")
    argparser.add_argument("-p", "--projects", required=True, nargs="+", help="Projects to download. This can be the name (fabric-api) or project identifier (P7dR8mSH).")
    args = argparser.parse_args()

    for i in range(len(args.projects)):
        downloadProject(args.loader, args.versions, args.projects[i], optionalDependencies = args.optional, skipDependencies = args.skip, outputDir = os.path.abspath(args.directory.strip()), replaceFiles = args.replace)
        
    print("done")
