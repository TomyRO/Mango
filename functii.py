#!usr/bin/python
import datastuff


# primit de la frontend
def upload_req(file):
  filename = extract_filename(file)
  size = get_size(file)

  start_slice, start = get_curr_offset()
  end = start + size

  chunks, chunk_IDs = split(start, get_size(file), file)
  add_file_to_filelist(filename, chunk_IDs, start, end)

  return upload_storage(chunks, filename)

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
def split(start_offset, size, file):
  chunks = []

  # check if file fits in one chunk only
  offset = get_curr_offset()
  initial_chunk = req_chunk(offset)

  # returneaza unde a ramas in fisier
  # ret -1 daca a terminat
  file_offset = fill_initial_chunk(initial_chunk, file)

  chunks.append(initial_chunk)

  # append all other chunks 

  return chunks

