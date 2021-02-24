<h1 align="center"><code>student-home-cleaner</code></h1>

<div align="center">
  <sub>Created by <a href="https://github.com/jmakela42">Jani Mäkelä (dal)</a> and <a href="https://github.com/jgengo">Jordane Gengo (titus)</a></sub>
</div>
<div align="center">
  <sub>From <a href="https://hive.fi">Hive Helsinki</a></sub>
  <br />
</div>

<br><br>

<a href="#">student-home-cleaner</a> is a tool used at Hive Helsinki to detect inactive students via the 42 intra API and delete their student home image.


<br><br>
# Table of contents
- [Configuration](#Configuration)
- [Setup in production](#Setup-in-production)

<br /><br />
# Configuration

## 1. home-student-cleaner config.yml

You can find `config.yml` in the root of the repository. That's where are stored all the config variables needed to run this tool and adapt it to another school.


| key | ? |
| :---: | :---: |
| `home_dir` |  absolute path of the homes dir | 
| `campus_id` | your intra campus_id |
| `inactive_duration_month` | inactive month time allowed |
| `allowed_list` | a list of allowed students to keep their homes (test accounts for example) |

<br><br>
## 2. API lib config.yml

Create in the `tools/` directory, a config.yml with your 42 API credentials. A simple app with public scope is enough.

```sh
cp tools/config_sample.yml tools/config.yml
vim tools/config.yml
```

  [go back to menu](#Table-of-contents)

<br /><br />
# Setup in production

1. Git clone the repository to the student-storage VM
```sh
git clone git@github.com:hivehelsinki/student-home-cleaner.git /opt/student-home-cleaner
```
2. Edit the config.yml to match your needs on the root folder
```
vim /opt/student-home-cleaner/config.yml
```
3. Edit the config.yml in tools/ with your API credentials (an app with scope `public` is enough)
```sh
cp /opt/student-home-cleaner/tools/config_sample.yml /opt/student-home-cleaner/tools/config.yml
vim /opt/student-home-cleaner/tools/config.yml
```
4. Install python3-pip package
```sh
apt-get update && apt-get install -y python3-pip
```
5. Install the python dependencies
```sh
cd /opt/student-home-cleaner ; pip3 -r requirements.txt
```
6. Execute the script **without** `--perform` option and check it works as you want:
```sh
python3 -B app.py
```
7. If it works well, you can add a daily/weekly/monthly cron on the VM. It's up to you.

```sh
crontab -e
```

(example) everyday at 1 am
```sh
0 1 * * * /usr/bin/python3 -B /opt/student-home-cleaner/app.py --perform
```

(example) every monday at 1 am
```sh
0 1 * * 1 /usr/bin/python3 -B /opt/student-home-cleaner/app.py --perform
```

(example) every 1st day-of-month at 1 am
```sh
0 1 1 * * /usr/bin/python3 -B /opt/student-home-cleaner/app.py --perform
```