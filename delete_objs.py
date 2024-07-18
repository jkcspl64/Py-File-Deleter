#!/usr/bin/env python3

import os
import pathlib

from typing import Self


def normalize_fp(fp: pathlib.Path):
  if fp.is_absolute():
    return fp
  elif fp.is_symlink():
    return pathlib.Path( os.path.abspath(str(fp)) )
  else:
    return fp.resolve()


class DeleteEntry:
  def __init__(self):
    self.src: pathlib.Path = None
    self.exists_before_deletion = False
    self.done = False
    self.successful = False
    self.detail = str(None)
  
  def __as_string(self, file_type):
    file_exists = "EXISTS" if self.exists_before_deletion else "MISSING"
    success_txt = ""
    if not self.done:
      success_txt = "PENDING"
    elif self.successful:
      success_txt = "OK"
    else:
      success_txt = "ERROR"
    
    return f"Delete|{file_type}|{file_exists}|{str(self.src)}|{success_txt}|{self.detail}"
  
  def __str__(self):
    return self.__as_string("ENTRY")
  
  @staticmethod
  def build(src: pathlib.Path):
    resp = DeleteEntry()
    return DeleteEntry._finish_build(resp, src)
  
  @staticmethod
  def _finish_build(resp: Self, src: pathlib.Path):
    resp.src = normalize_fp(src)
    resp.exists_before_deletion = resp.src.exists()
    return resp


class DeleteFileEntry(DeleteEntry):
  def __init__(self):
    super().__init__()
  
  def __str__(self):
    return self._DeleteEntry__as_string("FILE")
  
  @staticmethod
  def build(src: pathlib.Path):
    resp = DeleteFileEntry()
    return DeleteEntry._finish_build(resp, src)
  
  def delete(self):
    try:
      self.src.unlink()
      self.successful = True
      self.detail = "OK"
    except (IOError, OSError) as e:
      self.detail = str(e)
    finally:
      self.done = True


class DeleteFolderEntry(DeleteEntry):
  def __init__(self):
    super().__init__()
  
  def __str__(self):
    return self._DeleteEntry__as_string("FOLDER")
  
  @staticmethod
  def build(src: pathlib.Path):
    resp = DeleteFolderEntry()
    return DeleteEntry._finish_build(resp, src)
  
  def delete(self):
    try:
      self.src.rmdir()
      self.successful = True
      self.detail = "OK"
    except (IOError, OSError) as e:
      self.detail = str(e)
    finally:
      self.done = True
