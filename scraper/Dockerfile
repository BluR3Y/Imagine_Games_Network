FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY imagine_games_scraper /usr/src/app/imagine_games_scraper

WORKDIR /usr/src/app/imagine_games_scraper

CMD ["python", "run_program.py"]