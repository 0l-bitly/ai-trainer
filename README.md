# ai-trainer
### This repo helps for training AI models with code.

> [!CAUTION]
> Be careful.
> If you don't test this project before use you can cleanly destroy your computer.
> The project can download To of data and if you have not a complete datacenter, you may not have enough disk space...
> To test the project I recommend to use the provided lists with only two or three words, and you can also comment the 95th line of crawler.py to deactivate the download.

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

### Use
See this:
```plaintext
$ python3 main.py --help
Git verification O.K.
usage: main.py [-h] [--debug] [--config_file CONFIG_FILE]
               [--compilation_config_file COMPILATION_CONFIG_FILE]
               {config,crawl} ...

AI Trainer Configuration

positional arguments:
  {config,crawl}
    config              Modify configuration
    crawl               Start crawl

options:
  -h, --help            show this help message and exit
  --debug, -d           Run in debug mode.
  --config_file, -cfg CONFIG_FILE
                        Custom config file path.
  --compilation_config_file COMPILATION_CONFIG_FILE
                        Custom compilation config file path.
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
python3 main.py --debug --compilation_config_file "cfg/compilation-testing.json" crawl --token "ghp_TOKEN_GITHUB" --keywords "main-testing-keywords.txt"
```
