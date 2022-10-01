from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Create and generate a word cloud image:
def generate_wordcloud(string_list):
    string_s = " ".join(string_list)
    wordcloud = WordCloud().generate(string_s)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #convert to png
    plt.savefig('static\images\wordcloud.png')

    