import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set(rc={'figure.figsize':(11, 4)})

dataDirectory = '../data/'
graphsDirectory = 'graphs/'
def visDay(dfs,sensors,day):
    plt.clf()
    fig, axs = plt.subplots(len(dfs),sharex=True,sharey=True,gridspec_kw={'hspace': 0.5},figsize=(20, 10))
    fig.suptitle('Measurements for day {0}'.format(day))

    for i in range(len(dfs)):
        axs[i].plot(dfs[i]['measurement'],marker='.', alpha=0.5, linestyle='None')
        axs[i].set_title('Sensor {0}'.format(sensors[i]))
        axs[i].set_ylabel('Temperature in °C')
    plt.ylim([15,30])
    plt.savefig(graphsDirectory+"day_{0}_sensors_{1}.pdf".format(day,str(sensors).replace(' ','')))

def visSingleSensor(df,day,sensor):
    # print("sensor {0} on day {1}".format(sensor,day))
    print(day,'&',sensor,'&',len(df),'&',df['measurement'].max(),"&",  df['measurement'].min(),"&",df['measurement'].mean(),'&',df['measurement'][0],'&',df['measurement'][-1])
    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.plot(df['measurement'],marker='.', alpha=0.5, linestyle='None')
    plt.title('Temperature for sensor {0} on day {1}'.format(sensor,day))
    plt.ylabel('Temperature in °C')
    # plt.show()
    plt.savefig(graphsDirectory+"day_{0}_sensor_{1}.pdf".format(day,sensor))


def createGraphsDayOne():
    firstDate = '2017-02-28'
    for sens in [sensors1,sensors24]:
        sensorDfs = []
        for i in sens:
            df = pd.read_csv(dataDirectory + firstDate + '_sensor_{0}.csv'.format(i), dtype={"measurement": float, "voltage": float})
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time',inplace=True)
            df.index = df.index.time
            visSingleSensor(df,1,i)
            sensorDfs.append(df)
        visDay(sensorDfs,sens,1)

def anomaliesDayOne():
    firstDate = '2017-02-28'
    for i in [1,24]:
        df = pd.read_csv(dataDirectory + firstDate + '_sensor_{0}.csv'.format(i),
                         dtype={"measurement": float, "voltage": float})
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        # df.index = df.index.time
        groups = df.groupby(pd.Grouper(freq='60s'))
        count = 0
        for group in groups:
            if len(group[1]) > 2:
                count += len(group[1]) - 2

        print(i,count,len(df)-count)


def createGraphsAllWeek():
    for day in range(1,8,1):
        date = '2017-03-0{0}'.format(day)
        for sens in [sensors1, sensors24]:
            sensorDfs = []
            for sensor in sens:
                df = pd.read_csv(dataDirectory + date + '_sensor_{0}.csv'.format(sensor),
                                 dtype={"measurement": float, "voltage": float})
                df['time'] = pd.to_datetime(df['time'])
                df.set_index('time', inplace=True)
                df.index = df.index.time
                visSingleSensor(df, day+1, sensor)
                sensorDfs.append(df)
            visDay(sensorDfs, sens, day+1)

if __name__=="__main__":

    sensors = [1, 24, 2, 3, 33, 35, 22, 25]
    sensors1 = [1, 2]#, 3, 33, 35]
    sensors24 = [24,22]#,25]

    # createGraphsDayOne()
    # createGraphsAllWeek()
    anomaliesDayOne()