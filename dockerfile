# Step 1: Specify the base image
FROM python:3.10

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install the dependencies
RUN pip install -r requirements.txt

# Step 5: Expose the port the app runs on
EXPOSE 5000

# Step 6: Define the command to run the application
CMD ["python", "app.py"]
