<h1 align="center"><code>student-home-cleaner</code></h1>

<div align="center">
  <sub>Created by <a href="https://github.com/jmakela42">Jani Mäkelä (dal)</a> and <a href="https://github.com/jgengo">Jordane Gengo (titus)</a></sub>
</div>
<div align="center">
  <sub>From <a href="https://hive.fi">Hive Helsinki</a></sub>
  <br />
</div>

<h1 align="center">WIP</h1>

<a href="#">student-home-cleaner</a> is a tool used at Hive Helsinki to detect inactive students via the 42 intra API and delete their student home image.

**This tool is not dockerized, I don't want to setup docker on our student-storage VM, just for that tool.**

<br><br>
# Table of contents
- [Configuration](#Configuration)
- [Setup in production](#Setup-in-production)

<br /><br />
# Configuration

You can find `config.yml` in the root of the repository. That's where are stored all the config variables needed to run this tool and adapt it to another school.


| key | ? |
| :---: | :---: |
| `home_dir` |  absolute path of the homes dir | 
| `campus_id` | your intra campus_id |
| `inactive_duration_month` | inactive month time allowed |
| `allowed_list` | a list of allowed students to keep their homes (test accounts for example) |


  [go back to menu](#Table-of-contents)

<br /><br />
# Setup in production

1. Fork this repository on your Github organization
2. Add your student-storage SSH key as a deploy key
3. Push your edited config.yml to match your needs 
4. Git clone your forked repository from the student-storage VM
5. Install the python dependencies
```sh
pip -r requirements.txt
```
6. Run a dry-run test and check it works as you want :
```sh
./app.py --dry-run
```
7. If it works well, you can add a daily/weekly cron on the VM. It's up to you #TODO give a cron example