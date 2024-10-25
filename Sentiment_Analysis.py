import json
from datetime import datetime, timedelta
import openai

# Loading data from file
def get_values(json_string):
    dictlist = json.loads(json_string)
    headline = dictlist.get('title', None)
    source = dictlist.get('source', {}).get('name', None)
    date = dictlist.get('publishedAt', None)
    return headline, source, date

# Performing sentiment analysis with ChatGPT API
openai_key=open("/home/daniel_a_lebedinsky/openai_key", 'r')
openai.api_key = openai_key.readline()

def headline_sentiment(headline):
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=f"What is the sentiment of these headlines: {headline}? Give a 1-word response: positive, negative, or neutral.",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).get("choices")[0].text
    return response.strip().lower()

def parse_date(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_result(kv):
    key, count = kv
    source, sentiment, window_start_str = key
    window_start = datetime.strptime(window_start_str, "%Y-%m-%d %H:%M:%S")
    window_end = window_start + timedelta(days=1)
    return f"{source} | {sentiment} | {window_start_str} - {window_end.strftime('%Y-%m-%d %H:%M:%S')} | {count}"

# Distributed, parallel operations with Apache Beam
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import StandardOptions

options = PipelineOptions()
google_cloud_options = options.view_as(GoogleCloudOptions)
google_cloud_options.project = 'verdant-tempest-385915'
google_cloud_options.job_name = 'headline-sentiment-analysis-job'
google_cloud_options.staging_location = 'gs://headline-sentiment-analysis-bucket/staging'
google_cloud_options.temp_location = 'gs://headline-sentiment-analysis-bucket/temp'
options.view_as(StandardOptions).runner = 'DataflowRunner'
# It is possible to set the number of workers with the following options:
# 2 is enough, the free tier of NewsAPI gives about 0.5MB of data.
from apache_beam.options.pipeline_options import WorkerOptions
worker_options = options.view_as(WorkerOptions)
worker_options.num_workers = 2 

with beam.Pipeline(options=options) as pipeline:
    results = (
        pipeline
        | 'Read lines from text file' >> beam.io.ReadFromText('all_articles.txt')
        | 'Convert JSON strings to dictionaries and get values' >> beam.Map(get_values)
        | 'Determine headline sentiment' >> beam.Map(lambda x: (x[0], x[1], x[2], headline_sentiment(x[0])))
        | 'Parse date' >> beam.Map(lambda x: (x[0], x[1], parse_date(x[2]), x[3]))
        | 'Apply windowing' >> beam.WindowInto(beam.window.FixedWindows(60*60*24, 0))
        | 'Group by source and sentiment' >> beam.Map(lambda x: ((x[1], x[3], x[2]), 1))
        | 'Count headlines' >> beam.CombinePerKey(sum)
        | 'Format results' >> beam.Map(format_result)
        | 'Write results to text file' >> beam.io.WriteToText('gs://headline-sentiment-analysis-bucket/output_results.txt')
    )

openai_key.close()