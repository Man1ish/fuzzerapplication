
# Fuzzing in serverless architecture

This project creates the fuzzer for serverless architecture



## Requirement Installation

Download and run openwhisk framework

```bash
#download openwhisk 
git clone https://github.com/apache/openwhisk.git
#running the framework
cd openwhisk
./gradlew core:standalone:bootRun

#download and setup the wsk tool
https://github.com/apache/openwhisk-cli

wsk property set \
  --apihost 'http://localhost:3233' \
  --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

#clone the repo 
git clone https://github.com/Man1ish/fuzzerapplication.git

#setup 
python3 -m venv venv
venv/bin/python -m pip install --upgrade pip
venv/bin/python -m pip install -r requirements.txt

#run the api server
python api_server.py

```
    
## Run project

To run the fuzzer

```bash
  python main.py
```

