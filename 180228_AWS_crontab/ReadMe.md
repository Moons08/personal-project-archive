## AWS test
[archive](https://github.com/Moons08/personal-project-archive)

#### what to do
- scrape daily headlines with link
- send results to my slack channel every morning
- by AWS, automatically

#### what I used
- AWS, selenium, Xvfp, crontab
- slack, incoming webhooks api

#### code
- [newsfeed.py](https://github.com/Moons08/personal-project-archive/blob/master/180228_AWS_crontab/newsfeed.py)
- [newsfeed2.py](https://github.com/Moons08/personal-project-archive/blob/master/180228_AWS_crontab/newsfeed2.py)
- crontab:
    - 00 00  * * * /home/ubuntu/.pyenv/shims/python3.6 newsfeed.py
    - need to check which python version to excute

#### result
![Alt text](https://github.com/Moons08/personal-project-archive/blob/master/180228_AWS_crontab/screenshot.png)

#### review
There was an error which took my time. The python code worked separatedly, but it did not work with crontab. I thoght that the python libraries crashed with crontab, such as Xvfb. I wasted time to figure it out. But, it was just a trivial crontab problem.

So, when using crontab, should **check python version** to proceed. And must install mail. **crontab send error messages by mail.**
