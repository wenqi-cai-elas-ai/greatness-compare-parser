# Greatness Compare Parser

The Greatness Compare Parser takes the output of the "Greatness.Compare" pipeline and converts it into an Excel sheet. This formatted output can be easily loaded with tools such as pandas for data analysis, enabling the generation of insightful tables and statistical analysis.

## How to Use

The parser can be run using either a local environment or Docker.

### Using Local Environment

To set up and run the parser locally, execute the following steps:

1. Create a new conda environment:
```shell
conda create -n mccParser python=3.7
```
2. Activate the conda environment:
```shell
conda activate mccParser
```
3. Install the required dependencies:
```shell
pip install -r requirements.txt
```
4. Run the application:
```shell
python app.py
```
5. Access the application by opening your web browser and navigating to:
http://127.0.0.1:5000/

### Using Docker
Alternatively, you can run the parser in a Docker container:
1. Ensure Docker is installed on your machine.
2. Build the Docker image:
```shell
docker build -t mccParser .
```
3.Start a container from the image:
```shell
docker run -dp 5000:5000 mccParser
```
4. Open the application in a web browser:
In VS Code, go to the Docker section, find your container under CONTAINERS, right-click it, and choose 'Open in Browser'.
Or, directly in any web browser, visit: http://localhost:5000
