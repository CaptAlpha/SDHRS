from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
# Create and generate a word cloud image:
def generate_wordcloud(string_list):
    string_s = " ".join(string_list)
    wordcloud = WordCloud().generate(string_s)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

generate_wordcloud(string_list)

    