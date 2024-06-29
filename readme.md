# Project Deployment Guide

This guide will walk you through the process of setting up and running this project on your local machine.

## Prerequisites

- Python 3.10 or lower
- pip (Python package installer)

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/alexchenzl/metacast-pipeline
   ```

2. Navigate to the project directory:
   ```
   cd metacast-pipeline
   ```

3. Install the required Python packages:
   ```
   pip install airstack nest_asyncio
   pip install backoff
   # use older version to avoid dependency confict with airstack
   pip instal openai==0.28.0
   ```

## Configuration

1. Create a `config.json` file in the root directory of the project.

2. Add the following content to `config.json`, replacing the placeholders with your actual API keys and other configuration details:
   ```json
   {
     "airstack_api_key": "your_airstack_api_key",
     "openai_api_key": "your_openai_api_key",
     "api_url": "your_api_endpoint_url",
     "bearer_token": "your_bearer_token",
     "valid_keywords": ["keyword1", "keyword2", "keyword3"]
   }
   ```

## Running the Scripts

The project consists of several scripts that should be run in sequence. To run all scripts at once, use:

```
python start.py
```

This will execute the following scripts in order:

1. `0StepCleanTempData.py`
2. `1DailyGetDataFormAirstack.py`
3. `2Transform_data.py`
4. `3GptCheckRelated.py`
5. `4CheckKeywordManual.py`
6. `5submitData.py`

StepCleanTempData.py:

Cleans temporary data by moving and renaming .txt files to a backup directory, ensuring a clean workspace for new data processing.

DailyGetDataFormAirstack.py:

Fetches trending casts data from Airstack API, processes it, and saves the results to 'AllTrendOutput.txt' for further analysis.

Transform_data.py: 

Transforms the raw data from 'AllTrendOutput.txt', restructuring it into a more usable format and saving it to 'transformed_json.txt'.

GptCheckRelated.py: 

Uses OpenAI's GPT model to check the relevance of each cast against predefined keywords, saving results to 'GptChecked.txt'.

CheckKeywordManual.py:

Extracts the most relevant keyword for each cast using GPT, compares it with valid keywords, and saves results to 'ManualChecked.txt'.

submitData.py: 

Filters and reformats the processed data, then submits it to a specified API endpoint for final processing or storage.

## Output

- The scripts will generate several output files in the project directory.
- Logs will be stored in the `log` directory.
- The final output will be submitted to the API specified in your `config.json` file.

## Troubleshooting

- If you encounter any Unicode-related errors, ensure that your terminal supports UTF-8 encoding.
- Check the log files in the `log` directory for detailed error messages and script outputs.

## Note

Make sure to keep your `config.json` file secure and do not share it publicly, as it contains sensitive API keys.
