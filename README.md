# ai-trainer
### This repo helps for training AI models with code.

> [!CAUTION]
> This project is not available for production and there is certainly a lot of bugs.

It is now in development and does not working.
### Project structure
```tree
/README.md
/LICENCE
/src
--/main.py
--/trainer.py
--/funcs.py
--/compiler.py
--/crawler.py
--/src
----/{random-generated-name}-source-code.{extension}
----/sums
------/{random-generated-name}-sum.sum
--/cfg
----/config.json
----/licenses.json
----/compilers.json
--/comp
---/{languages-compilers-bins}
--/dist
----/{random-generated-names-compiled-bins}
```
### Project overview
It crawls github and look at for free repos. (You are limited by your rate limit)
config.json file structure (read by main.py):
```json
{
    "compile": true,
    "train": false,
    "sum" : false,
    "compilerscfgfile": "./cfg/compilers.json",
    "licensescfgfile": "./cfg/licenses.json",
    "gitpath": "/usr/bin/git",
    "outdir": "./dist/",
    "auth": ["API_KEY", "OTHER_API_KEY"]
}
```
licenses.json file structure: 
```json
{
    "licenses" : {
        "authorised_license_name": true,
        "forbidden_license_name": false
    }

}
```
compilers.json file structure :
```json
{
    "compilables": [
        {"langage": "Python", "extension": ".py"}
    ]
    "compilerspath" : "./comp/"
}
```

### Installing
No build required.
```bash
git clone https://www.github.com/0l-bitly/ai-trainer
```
```bash
cd ai-trainer/
```
```bash
python3 main.py [options]
```
For help:
```bash
python3 main.py --help
```
Example usage:
```bash
python3 main.py crawl --token "ghp_TOKEN_GITHUB" --keywords "main-testing-keywords.txt"
```