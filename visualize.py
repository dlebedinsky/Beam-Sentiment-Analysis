import matplotlib.pyplot as plt

def read_results(file):
    results = {}
    with open(file, 'r') as f:
        for line in f:
            print(f"Line: {line.strip()}")  # Add this print statement for debugging. Correct format below:
            # “Outlet Name | sentiment | 24-hour period | count”
            parts = line.strip().split(' | ')
            if len(parts) == 4:
                source, sentiment, window, count = parts
                print(f"source: {source}, sentiment: {sentiment}, window: {window}, count: {count}")
                count = int(count)
                if source not in results:
                    results[source] = {'positive': 0, 'negative': 0, 'neutral': 0}
                # In case chatgpt misbehaved:
                pos= "positive" in sentiment.lower().replace(" ", "") 
                neg= "negative" in sentiment.lower().replace(" ", "") 
                if(pos):
                    results[source]['positive'] += count
                elif(neg):
                    results[source]['negative'] += count
                else:
                    results[source]['neutral'] += count
                print(f"Adding {count} {sentiment} headlines to {source}")  
                # print statement for debugging
    print(f"Results: {results}")  # print statement for debugging
    return results

def plot_results(results):
    sources = list(results.keys())
    positive_counts = [results[source]['positive'] for source in sources]
    negative_counts = [results[source]['negative'] for source in sources]
    neutral_counts = [results[source]['neutral'] for source in sources]

    bar_width = 0.25
    positions = list(range(len(sources)))

    plt.bar(positions, positive_counts, color='g', width=bar_width, edgecolor='white', label=f'Positive: {sum(positive_counts)}')
    plt.bar([p + bar_width for p in positions], negative_counts, color='r', width=bar_width, edgecolor='white', label=f'Negative: {sum(negative_counts)}')
    plt.bar([p + 2*bar_width for p in positions], neutral_counts, color='b', width=bar_width, edgecolor='white', label=f'Neutral: {sum(neutral_counts)}')

    plt.xlabel('Source', fontweight='bold')
    plt.xticks([p + bar_width for p in positions], sources, rotation=90)
    plt.ylabel('Headline Count')
    plt.title('Headline Sentiment Counts by Source')
    plt.legend()
    plt.show()


results = read_results('output_results.txt')
plot_results(results)