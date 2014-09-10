from pandas import *
from ggplot import *
import os

os.chdir("/Users/genghis/projects/udacity/visualizations")

def plot_weather_data(turnstile_weather):
    
    days = []
    
    df = turnstile_weather
    def day(date):
        return datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%w')

    for date in turnstile_weather['DATEn']:
        days.append(day(date))

    df['Days'] = days
    grouping = df.groupby(['Days'],as_index=False).sum()
    #grouping['order'] = [4, 0, 5, 6, 3, 1, 2]
    plot = ggplot(grouping, aes('Days', 'ENTRIESn_hourly')) + \
           geom_bar(aes(weight='ENTRIESn_hourly'), fill='blue', stat = 'bar') + \
           scale_x_discrete(labels=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']) + \
           ggtitle('Subway Ridership for Days of the Week') + \
           xlab('Day of the Week') + \
           ylab('Entries Per Hour')
    return plot

if __name__ == "__main__":
    image = "plot.png"
    with open(image, "wb") as f:
        turnstile_weather = pandas.read_csv("turnstile_data_master_with_weather.csv")
        turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
        gg =  plot_weather_data(turnstile_weather)
        ggsave(f, gg)