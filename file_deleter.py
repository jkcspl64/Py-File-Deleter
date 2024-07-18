#!/usr/bin/env python3

import sys
import pathlib
import argparse

from typing import List
from delete_objs import normalize_fp, DeleteFileEntry, DeleteFolderEntry


def parse_args():
  parser = argparse.ArgumentParser()
  
  del_mode_sp = parser.add_subparsers(
    title="Deletion mode", description="The following are valid deletion modes:",
    dest="del_mode"
  )
  
  file_del = del_mode_sp.add_parser("files", help="Delete a list of files")
  file_del.add_argument("file_list", help="The list of files to be deleted (mandatory)")
  
  folder_del = del_mode_sp.add_parser("folder", help="Delete files from a specified folder")
  folder_del.add_argument("folder", help="The folder where the to-be deleted files are (mandatory)")
  folder_del.add_argument(
    "-w", "--wildcard",
    help="A wildcard specifying which files to delete (default: ALL)",
    default="ALL"
  )
  folder_del.add_argument(
    "-X", "--delete-folder",
    help="A flag to determine if the input folder will also be deleted (default: false)",
    action="store_true", default=False
  )
  
  return parser.parse_args()


def get_files_from_txt(txt_file):
  fp = pathlib.Path(txt_file)
  
  if not fp.exists() or not fp.is_file():
    print("The input file doesn't exist or is not a file!", file=sys.stderr)
    exit(-1)
  
  result: List[DeleteFileEntry] = []
  
  with open(str(fp), "r", encoding="utf-8") as fhand:
    result = [DeleteFileEntry.build(pathlib.Path(line.strip())) for line in fhand]
  
  return result


def get_files_from_folder(folder: str, wildcard):
  ffp = DeleteFolderEntry.build( pathlib.Path(folder) )
  
  if not ffp.src.exists() or not ffp.src.is_dir():
    print("The input folder doesn't exist or is not a folder!", file=sys.stderr)
    exit(-1)
    
  result: List[DeleteFileEntry] = []
  wcd = "*" if wildcard == "ALL" else wildcard
  files = ffp.src.glob(wcd)
  
  for file in files:
    result.append( DeleteFileEntry.build(file if file.is_absolute else file.resolve()) )
  
  return (ffp, result)
  

def main():
  args = parse_args()
  
  files: List[DeleteFileEntry] = []
  folder: DeleteFolderEntry = None
  
  if args.del_mode.lower() == "files":
    # File list deletion mode
    files = get_files_from_txt(args.file_list)
  elif args.del_mode.lower() == "folder":
    # Folder deletion mode
    folder, files = get_files_from_folder(args.folder, args.wildcard)
  
  for file in files:
    file.delete()
    print(file)
  
  if folder and args.delete_folder:
    folder.delete()
    print(folder)


if __name__ == "__main__":
  main()
