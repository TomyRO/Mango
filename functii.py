#!usr/bin/python
from datastuff import *

def extract_filename(file):
  return "test-filename"

def get_size(file):
  return 1024

# primit de la frontend
def upload_req(file):
  filename = extract_filename(file)
  size = get_size(file)

  start_chunk, start_offset = get_last_used_chunk_and_offset() 

  chunks, chunk_IDs = split(start_offset, get_size(file), file)
  end_offset = "bla"
  add_file_to_filelist(filename, chunk_IDs, start_offset, end)

  # store ranges
  for i in xrange(len(chunk_IDs) - 1):
  	set_chunk_offset(chunk_IDs[i], CHUNK_SIZE)
  #last chunk
  set_chunk_offset(chunk_IDs[len(chunk_IDs) - 1], size % CHUNK_SIZE)
  
  print chunks
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
  # din tabel local
  return get_file_names()

# write the file to a list of chunks
# start chunk is requested and overwritten from the last file's offset
# returns:
# 1. the list of data chunks
# 2. the list of associated chunk IDs
def split(start_offset, size, file):
  # for testing:
  chunks = ["00", "01", "02"]
  chunk_IDs = [0, 1, 2]

  # TODO check if file fits in one chunk only
  offset = "blaoffset"#get_curr_offset()
  initial_chunk, start_offset = req_chunk()

  initial_chunk = chunks[0]

  # returneaza unde a ramas in fisier
  # ret -1 daca a terminat
  file_offset = fill_initial_chunk(initial_chunk, file)

  chunks.append(initial_chunk)

  # append all other chunks 

  return chunks, chunk_IDs

# makes request to storage backend for the chunk last chunk that is
# available for writing
# also returns the offset where we can start writing in that chunk
def req_chunk():
  return "blablafiletext"
