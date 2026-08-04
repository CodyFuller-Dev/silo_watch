#this is the base python image and the slim tells us that its just the basics needed to extra stuff
FROM python:3.12-slim

#this sets the working directory where all the rest of the work and project files get loaded
WORKDIR /app

#this litterally coppies the requirements file over to the app
#only the req file is coppied first because once its written it usually dose not change
#doing this first then runing pip below keeps newer builds from runing though the pip of all the req's if "anything" in the main app.py changes
COPY requirements.txt .

#this actually goes through and installs all the items listed out in the req file. 
#It also tells the app not to save any instalation files because we would never "reinstall" something inside a container we would just spin up a different container
RUN pip install --no-cache-dir -r requirements.txt

#this coppies everything else in the project over to the app
COPY . . 

#shows what port the app operates on but dose not acually open that port
EXPOSE 5001

#this actually starts up the flask app thus cranking up the engine
CMD ["python", "app.py"]