# Task

Write a query to collect all relations from dbpedia for every individual person listed 
in it. The task requires running a SPARQL request at https://dbpedia.org/sparql.

# Solution

An individual person has URI http://dbpedia.org/ontology/Person. To find all person-connected
relations, we need to unite relations to and from every person. Finally, we deduplicate
relations types using **distinct** clause:

```
select distinct
?r where {
  {[] ?r <http://dbpedia.org/ontology/Person>}
UNION
  {<http://dbpedia.org/ontology/Person> ?r []}
} LIMIT 100
``` 

# Results
[Press here to get live results from dbpedia.org](https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=select+distinct%0D%0A%3Fr+where+%7B%0D%0A++%7B%5B%5D+%3Fr+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPerson%3E%7D%0D%0AUNION%0D%0A++%7B%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPerson%3E+%3Fr+%5B%5D%7D%0D%0A%7D+LIMIT+100&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+)

Snapshot from 20-Mar-2019:

| r |
|---|
|http://www.w3.org/1999/02/22-rdf-syntax-ns#type|
|http://www.w3.org/2000/01/rdf-schema#domain|
|http://www.w3.org/2000/01/rdf-schema#range|
|http://www.w3.org/2002/07/owl#disjointWith|
|http://www.w3.org/2000/01/rdf-schema#subClassOf|
|http://www.w3.org/2002/07/owl#equivalentClass|
|http://www.w3.org/2000/01/rdf-schema#label|
|http://www.w3.org/ns/prov#wasDerivedFrom|
