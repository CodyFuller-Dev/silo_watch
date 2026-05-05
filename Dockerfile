#Tells docker I need a small system to run a specific version on python
FROM python:3.12-slim

# creates a workspace inside the virtual computer, moves us into it automatically and makes it so every command runs from inside that folder 
WORKDIR /app

#sends the list of dependencies needed to actually run everything over to the virtual computer
COPY requirements.txt .

#takes the list of dependencies from above and actually installs them in the container
RUN pip install --no-cache-dir -r requirements.txt

#this copies the rest of the project files into the container again into the /app folder specifically
COPY . . 

#tells docker to make all communication through port 5000
EXPOSE 5000

#this tells the virtual computer upon start up start python AND my app.py application
CMD ["python", "app.py"]