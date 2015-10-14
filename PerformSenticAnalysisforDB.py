import requests
import re
import psycopg2
import MainSentinet as SenticNetAnalyzer


con = psycopg2.connect("dbname='SenticNet' user='postgres' host='ec2-52-89-108-22.us-west-2.compute.amazonaws.com' password='swm123'")
con.autocommit = True
cur = con.cursor()


query = 'Select * from amazon_review where review_id > 1'
cur.execute(query);
results = cur.fetchall()
for record in results:
    input = record[2]
    print "Sentence:",input
    SenticNetAnalyzer.performSentiNetAnalysis(con,record);