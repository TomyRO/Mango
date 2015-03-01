#!usr/bin/python
from datastuff import *
from array import array
import testdata as t

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

  return upload_storage(chunks, chunk_IDs)

# primit de la frontend
def download_req(filename):
  chunk_start = get_file_start_offest(filename)
  chunk_end = get_file_end_offset(filename)
  
  chunk_numbers = get_file_chunks(filename) # list of chunk numbers

  # print chunk_start, ' ', chunk_end, ' ', chunk_numbers

  # request la tomi pentru chunks
  chunks = download_storage(chunk_numbers, True)
  
  final_file = []
  if len(chunk_numbers) == 1:
    final_file = chunks[0][chunk_start : chunk_end]
  else:
    final_file = chunks[0][chunk_start:]
    for i in xrange(1, len(chunks_numbers) - 1):
      final_file = final_file + chunks[i]
    final_file = final_file + chunks[len(chunks_numbers) - 1][:chunk_end]

  return final_file

def download_storage(chunk_numbers, testing):
  #request la tomi
  chunks = []
  
  #TODO remove when not testing
  if testing:
    for i in xrange(len(chunk_numbers)):
      chunks.append(t.test_CHUNKS[chunk_numbers[i]]) 

  return chunks

# trimis lui tomi
def upload_storage(chunks, chunk_IDs):
  #files = generate_files(chunks)
  # call la tomi cu files
  #print "CHUNKS", chunks, chunk_IDs
  return chunks, chunk_IDs

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

    initial_chunk[start_offset:end_offset] = file[0 : (CHUNK_SIZE - start_offset)]
    size = size - (CHUNK_SIZE - start_offset)
    offset = CHUNK_SIZE - start_offset
    chunk_list.append(initial_chunk)
    chunk_IDs.append(chunk_number)
    chunk_number = chunk_number + 1

  while size > 0:
    if size < CHUNK_SIZE:
      new_chunk = array("B", CHUNK_SIZE * '0')
      new_chunk[0 : size] = file[offset:]
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
  # return array("B", "g"), 1
  return t.test_CHUNKS[start_chunk], chunk_index[start_chunk]
