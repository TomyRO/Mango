# functii.py test
from functii import *
from array import array

import testdata as t
import datastuff as d

# upload request test
file1 = array("B", "abcdefg")
fn1 = "file1"

file2 = array("B", "hij")
fn2 = "file2"

file3 = array("B", "klmnopqrstuv")
fn3 = "file3"

def append_or_overwrite_to_storage(ids, chks, store):
  for i in xrange(len(ids)):
    chunkIndex = ids[i]
    store[ids[i]] = chks[i]
  return store

chunks, chunkIDs = upload_req(file1, fn1, len(file1))
t.test_CHUNKS = append_or_overwrite_to_storage(chunkIDs, chunks, t.test_CHUNKS)
print t.test_CHUNKS

chunks, chunkIDs = upload_req(file2, fn2, len(file2))
t.test_CHUNKS = append_or_overwrite_to_storage(chunkIDs, chunks, t.test_CHUNKS)
print t.test_CHUNKS

chunks, chunkIDs = upload_req(file3, fn3, len(file3))
t.test_CHUNKS = append_or_overwrite_to_storage(chunkIDs, chunks, t.test_CHUNKS)
print t.test_CHUNKS

###################
# Download test
# True for testing
dld1 = download_req("file1", True)
print dld1
dld2 = download_req("file2", True)
print dld2
dld3 = download_req("file3", True)
print dld3
