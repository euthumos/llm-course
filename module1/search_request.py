from elasticsearch import Elasticsearch

es_client = Elasticsearch('http://localhost:9200') 
index_name = "course-questions"

def elastic_search(query: str):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["question^4", "text"],
                            "type": "best_fields"
                        }
                    }
                ]
                ,
                "filter": [
                    {
                        "term": {
                            "course": "machine-learning-zoomcamp"
                        }
                    }
                ]
            }
        }
    }

    resp = es_client.search(index=index_name, body=search_query)

    return [
        {
            **hit["_source"],
            "_score": hit["_score"]
        }
        for hit in resp["hits"]["hits"]
    ]


if __name__ == "__main__":
    q = "How do copy a file to a Docker container?"
    results = elastic_search(q)

    for doc in results[:3]:
        print(f"score:   {doc['_score']:.3f}")
        print(f"section: {doc['section']}")
        print(f"question:{doc['question']}")
        print(f"answer:  {doc['text']}\n")
