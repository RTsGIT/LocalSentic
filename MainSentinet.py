import cPickle as pickle
import networkx as nx
import senticnet
import SenticParser
import nltk
import os
import sys
import psycopg2

path=os.getenv("JAVA_HOME")
java_path = path+"/bin/java.exe" # replace this
os.environ['JAVAHOME'] = java_path

#this contains set of words 
# TODO : know what these words are
G = nx.read_gpickle( "test.gpickle" )


def performSentiNetAnalysis(con,record):
   # sentence = raw_input("Enter your search sentence ===>> " ).lower()
   cur = con.cursor()
   bigrams = []
   sentence = record[2] 
   words = sentence.split()

   list_concepts = []
   conc = []

   to_add = ""


   # for every word which is not in G, to_add is set to ""
   for word in words:
      if ( word in G ):
         conc.append(word)
         to_add = to_add+ word+" "

      else:
         if( to_add != "" ):
          list_concepts.append(to_add[:-1])
         to_add = ""     


   if( to_add != "" ):
      list_concepts.append(to_add[:-1])

   # print 'list_concepts',list_concepts

   parserList = SenticParser.getOutputConcepts(sentence)
   # print 'parserList',parserList 

   list_concept = list( set(list_concepts) |  set(parserList) ) 
   # print 'step1',list_concept

   list_concept = filter(bool, list_concept)
   # print 'step2',list_concept

   list_concept = set(list(list_concepts))
   # print 'step3',list_concept

   sn = senticnet.Senticnet()

   to_search = []


   for phrase in list_concepts:
      concepts = phrase.split()
      to_search = to_search + concepts
      for i in range(len(concepts) - 1):
         for j in range(i+1, len(concepts)):
            try:
               k = nx.dijkstra_path(G,concepts[i], concepts[j])
               #print k 
               if( len(k) == j-i+1 and k == concepts[i:j+1] ):  
                  to_search = list( set(to_search) - set(k) )      
                  word_to_add = "_".join(k)
                  to_search.append( word_to_add ) 

            except:
               continue            



   to_search = list( set(  to_search ) )

   sorted_by_length = sorted(to_search, key=lambda tup:len(tup.split("_")) )
   # print "--------------->Sorted sorted_by_length"
   print sorted_by_length
   # print "--------------->to_search"
   final_concepts = ','.join(to_search)
   print record[0],final_concepts
   cur.execute('update amazon_review SET concepts= %s where review_id=%s',(final_concepts,record[0]))
   # print "==================================================================================="


   for concept in to_search:
      try:
         print concept
         # print "concept---------------------------"
         concept_info =  sn.concept( concept)
         # print "polarity---------------------------"
         print concept_info
         # print sn.polarity( concept )
         # print "semantics---------------------------"
         # print sn.semantics( concept )
         # print "sentics---------------------------"
         # print sn.sentics(concept)
         # print "==================================================================================="
         try:
            cur.execute('insert into amazon_reviews_concepts (review_id,product_id,concept,info) values(%s,%s,%s,%s)',(record[0],record[1],concept,str(concept_info)))
         except:
            print sys.exc_info()
            sys.exit()
      except:
         print sys.exc_info()
         continue


# sentence = raw_input("Enter your search sentence ===>> " ).lower()
# performSentiNetAnalysis(sentence);