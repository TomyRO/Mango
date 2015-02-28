#!usr/bin/python

DEFAULT = 0

# contine:
#   - chunk number de forma 00, 01, etc
#   - offset pana la care a fost scris
chunk_index = {}

# contine:
#   - fileId
#   - lista de chunkuri in care este stocat
#   - start offset din primul chunk
#   - end offset din ultimul chunk
filelist = {}

def add_file_to_filelist(fileID, chunks, start, end):
  filelist[fileID] = {'chunks': chunks, 'start': start, 'end': end}

def get_file_chunks(fileID):
  return filelist[fileID]['chunks']

def get_file_start_offest(fileID):
  return filelist[fileID]['start']

def get_file_end_offset(fileID):
  return filelist[fileID]['end']

def populate_chunk_index(chunk_numbers):
  for i in range(chunk_numbers):
    chunk_index[i] = DEFAULT

def set_chunk_offsite(chunk_number, offset):
    chunk_index[chunk_number] = offset
