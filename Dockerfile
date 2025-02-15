# Step 1: Use a lightweight Python 3.9 image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container to /app
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 4: Install the dependencies inside the container
RUN pip install -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app/

# Step 6: Expose port 8000 for the Flask app to listen on
EXPOSE 8000

# Step 7: Run the Flask app using Python when the container starts
CMD ["python", "app.py"]
