# Base image (mirror my local python version)
FROM python:3.13

# Move to the directory with the project files
WORKDIR /Users/josecosta/Documents/projects/arknights-wallpaper-generator

# Copy all local files into the image (files/folders can be ignored in the .dockerignore)
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the streamlit port
EXPOSE 8501

# Startup the streamlit app
CMD ["streamlit", "run", "./streamlit_app.py"]