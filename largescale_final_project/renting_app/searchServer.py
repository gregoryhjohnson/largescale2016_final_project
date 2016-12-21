syntax = "proto3";

from concurrent import futures
import grpc
import sys
import os
import time 
import renting_pb2
from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import *

schema = Schema(item_id=STORED, item=TEXT, description=TEXT)
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class WhooshSearchServicer(renting_pb2.WhooshSearchServicer):

  def __init__(self):
    self = self
    #only run this once or the index files will be overwritten
    #if not os.path.exists("whoosh_index"):
      #os.mkdir("whoosh_index"):
    #ix = create_in("index, schema)
    
  def Add(self, request, context):
    ix = open_dir("whoosh_index")
    writer= ix.writer()
    writer.add_document(item_id=request.id, item=request.item, description=request.description)
    writer.commit()
    return renting_pb2.AddReply(completed="added successfully")

  def Search(self, request, context):
    parser = MultifieldParser(["item", "description"], schema=schema)
    q = parser.parse(request.query)
    ix = open_dir("whoosh_index")
    with ix.searcher() as searcher:
      results = searcher.search(q, limit=None)
      hit_ids = []
      for hit in results:
        hit_ids.append(hit["item_id"])
    return renting_pb2.SearchReply(hit_id=hit_ids)

  def Delete(self, request, context):
    ix = open_dir("whoosh_index")
    w = ix.writer()
    w.delete_by_term('item_id', str(request.id))
    w.commit()
    return renting_pb2.DeleteReply(completed="deleted successfully") 
    
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  renting_pb2.add_WhooshSearchServicer_to_server(WhooshSearchServicer(), server)
  server.add_insecure_port('[::]:35000')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
