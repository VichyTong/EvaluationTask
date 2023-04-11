wget https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/java.zip
unzip java.zip
gunzip java/final/jsonl/test/java_test_0.jsonl.gz

wget https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/python.zip
unzip python.zip
gunzip python/final/jsonl/test/python_test_0.jsonl.gz

python3 get_random_code.py

rm -r java python java.zip python.zip java_dedupe_definitions_v2.pkl python_dedupe_definitions_v2.pkl java_licenses.pkl python_licenses.pkl