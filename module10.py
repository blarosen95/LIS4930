import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import ggplot


def first(dataframe):
    names = dataframe['Speed'].unique().astype(str)
    values = dataframe['Speed'].value_counts(dropna=False)
    plt.bar(names, values)
    plt.show()


def second(dataframe):
    plot = ggplot.ggplot(ggplot.aes(x='Speed'), data=dataframe) + ggplot.geom_bar(
        color='lightblue') + ggplot.ggtitle("Frequencies of Speeds Among Interfaces") + ggplot.theme_xkcd()
    plot.show()


def extra(dataframe):
    mpl.rcParams["figure.figsize"] = "18, 4"
    plot = ggplot.ggplot(dataframe,
                         ggplot.aes(x='Time', y='Speed')) + ggplot.geom_path(color='lightblue',
                                                                             size=5) + ggplot.ggtitle(
        'Ports & Speeds') + ggplot.scale_y_reverse() + ggplot.theme_xkcd()
    plot.show()


df = pd.read_csv('switch1.csv')
first(df)
data = df['Speed']
data2 = pd.DataFrame(data, index=None).astype(str)
second(pd.DataFrame(data2))
df2 = pd.read_csv('switchparts.csv')
data3 = df2[['Time', 'Speed']]
data4 = pd.DataFrame(data3, index=None).astype(str)
extra(data4)
