# Getting-to-philosophy

Exploring the Wikipedia's philosophy phenomena 


## Project description

Project is about exploring how many hops does it take from random wiki link to reach the philosophy page. I take any random article on Wikipedia (example: http://en.wikipedia.org/wiki/Art) and click on the first link
on the main body of the article that is not within parenthesis or italicized. I repeat this process for each
subsequent article. 

Here I am defining main body as paragraph text mentioned after first heading. Only consecutive \<p\> tags
are considered. For example: for given link (https://en.wikipedia.org/wiki/Jonathan_Wells_(American_football)), main body is defined as following:

```
Jonathan Wells (born July 21, 1979) is a former American football running back. He played college football at Ohio State University and professionally in the National Football League (NFL) with the Houston Texans.
```

I also gather statistics such as: 

* Average number of hops 
* Percentage of random pages that land to philosophy page
* Reducing the number of http requests using **hashing**

## Statistics and discussion:

For 500 random pages:
* Average number of hops : 12.576419214
* Median number of hops : 13.0
* Percentage of random pages that land to philosophy page : 91.6 %
* Number of http requests :  1752
* Generate a matplotlib figure which is histogram of path lengths (number of hops) for all those pages among 500 pages which landed on philosophy.

For 10 pages, comparing the number of http requests without hashing and with hashing:

**Without hashing**

* Average number of hops : 12.4
* Median number of hops : 13.0
* Percentage of random pages that land to philosophy page : 70.0 %
* Total number of http requests : 104

**With hashing**

* Average number of hops : 12.875
* Median number of hops : 13.0
* Percentage of random pages that land to philosophy page: 80.0 %
* Total number of http requests : 82

**Clearly hashing reduces the number of http requests**.

*Note:* Don't give large number of random pages as an argument to [wikipedia_philosophy.py](https://github.com/shuklaham/getting-to-philosophy/blob/master/wikipedia_philosophy.py) as it is very slow and has been implemented without hashing.

## Code description 

* [wikipedia_philosophy.py](https://github.com/shuklaham/getting-to-philosophy/blob/master/wikipedia_philosophy.py) : Finds above mentioned statistics of given number of random pages. Number of random pages is provided as an external argument.
* [wikipedia_philosophy_hashing.py](https://github.com/shuklaham/getting-to-philosophy/blob/master/wikipedia_philosophy_hashing.py) : It performs the same operation as above but with **hashing**
* [test.py](https://github.com/shuklaham/getting-to-philosophy/blob/master/test.py) : It allows user to count the number of hops from the link provided the user
* [requirements.txt](https://github.com/shuklaham/getting-to-philosophy/blob/master/requirements.txt) : This file describes dependencies.

## Running the code in terminal

Clone the repo:

```
git clone https://github.com/shuklaham/getting-to-philosophy.git
```

Get into the directory:

```
cd getting-to-philosophy
```

Install virtual env:

```
pip install virtualenv
```

Setting up a virtual environment:

```
virtualenv wikiproject
```

Activate virtual environment:

```
source wikiproject/bin/activate
```

Installing dependencies:

```
pip install -r requirements.txt
```

**Running wikipedia_philosophy.py**: python wikipedia_philosophy.py \<num\>

```
python wikipedia_philosophy.py 10
```

**Running wikipedia_philosophy_hashing.py**: python wikipedia_philosophy_hashing.py \<num\>

```
python wikipedia_philosophy_hashing.py 10
```

OR
```
python wikipedia_philosophy_hashing.py 500
```

**Running test.py**: python test.py \<url\>

```
python test.py https://en.wikipedia.org/wiki/Design_Patterns
```

Deactivate the virtual environment:

```
deactivate
```

Delete the environment folder:

```
rm -rf wikiproject
```