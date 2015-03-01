#!usr/bin/python
from datastuff import *
from array import array


# file is a bytes array
def upload_req(file, filename, size):
  start_chunk, start_offset = get_last_used_chunk_and_offset()

  if start_offset == CHUNK_SIZE:
    start_chunk = start_chunk + 1
    # reset the starting offset for the next chunk
    start_offset = DEFAULT

  chunks, chunk_IDs, end_offset = split(start_chunk, start_offset, size, file)

  add_file_to_filelist(filename, chunk_IDs, start_offset, end_offset)

  # store ranges
  for i in xrange(len(chunk_IDs) - 1):
  	set_chunk_offset(chunk_IDs[i], CHUNK_SIZE)

  #last chunk
  set_chunk_offset(chunk_IDs[len(chunk_IDs) - 1], size % CHUNK_SIZE)

  print chunks
  print filelist
  #return upload_storage(chunks, filename)

# primit de la frontend
def download_req(filename):
  chunks_start, chunks_end = get_chunks_offsets(fileID)
  chunk_numbers = get_chunk_numbers(fileID)

  # request la tomi pentru chunks
  chunks = [] #request la tomi

  return merge_chunks(chunks, chunks_start, chunks_end)

# trimis lui tomi
def upload_storage(chunks, filename):
  files = generate_files(chunks)
  # call la tomi cu files

# request lui tomi
def list_storage(userID):
  filelist = get_file_list()

  return filelist.keys()

# write the file to a list of chunks
# start chunk is requested and overwritten from the last file's offset
# returns:
# 1. the list of data chunks
# 2. the list of associated chunk IDs
def split(start_chunk, start_offset, size, file):
  # TODO check if file fits in one chunk only
  offset = 0
  end_offset = 0
  chunk_number = start_chunk

  chunk_list = []
  chunk_IDs = []

  if start_offset > 0:
    initial_chunk, start_offset = req_chunk(start_chunk)

    if size < CHUNK_SIZE - start_offset:
      end_offset = start_offset + size
    else:
      end_offset = CHUNK_SIZE

    initial_chunk[start_offset:] = file[0 : (CHUNK_SIZE - start_offset)]
    size = size - (CHUNK_SIZE - start_offset)
    offset = CHUNK_SIZE - start_offset
    chunk_list.append(initial_chunk)
    chunk_IDs.append(chunk_number)
    chunk_number = chunk_number + 1

  while size > 0:
    if size < CHUNK_SIZE:
      new_chunk = file[offset:]
      # TODO: check if it needs a -1 or +1
      end_offset = size
      chunk_IDs.append(chunk_number)
    else:
      new_chunk = file[offset : offset + CHUNK_SIZE]
      offset = offset + CHUNK_SIZE
      end_offset = CHUNK_SIZE
      chunk_IDs.append(chunk_number)
      chunk_number = chunk_number + 1

    size = max(0, size - CHUNK_SIZE)

    chunk_list.append(new_chunk)

  return chunk_list, chunk_IDs, end_offset

# makes request to storage backend for the chunk last chunk that is
# available for writing
# also returns the offset where we can start writing in that chunk
# TODO implementation
def req_chunk(start_chunk):
  # returns initial_chunk data, start_offset
  return array("B", "blablabla"), 9

# fills remaining empty space in a chunk with the beginning of the
# given file
# returns the offset where it finished filling the chunk.
# this offset is not CHUNK_SIZE only when the entire file fits in
# the remaining empty space in the given chunk
# TODO implementation
def fill_initial_chunk(initial_chunk, file):
  return initial_chunk, CHUNK_SIZE
