import pandas as pd
import warnings
warnings.filterwarnings("ignore")
filename = "../data/data.conv.txt.gz"
dataDirectory = '../data/'
def getDataOfSensor(df,sensorId):
    sensorId = "{0}-0".format(sensorId)
    df = df[df['sensorid']==sensorId]
    df.dropna(inplace=True)
    return df


def saveWeekDays(df,sensors):
    for i in range(1,8,1):
        date = '2017-03-0{0}'.format(i)
        dayDf = df[df['date']==date]
        dayDf.sort_values('time', inplace=True)
        dfs = []
        for sensor in sensors:
            sensorDf = getDataOfSensor(dayDf,sensor)
            dfs.append(sensorDf)
        dayDf = pd.concat(dfs)
        # print(dayDf['measurement'].describe())
        dayDf.to_csv(dataDirectory+'{0}_all.csv'.format(date),index=False)

if __name__=="__main__":
    df = pd.read_csv(filename, header=None, delimiter=" ", names=["date", "time", "sensorid", "measurement", "voltage"],
                     dtype={"measurement": float, "voltage": float})
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    first_date = '2017-02-28'
    firstDay = df[df['date'] == first_date]
    firstDay.sort_values('time', inplace=True)
    sensors = [1, 24,2,3,33,35,22,25]
    toremove = []
    firstDayDfs = []
    for i in sensors:
        dayDf = getDataOfSensor(firstDay, i)
        # if len(dayDf) < 2000:
        #     toremove.append(i)
        # else:
        firstDayDfs.append(dayDf)
    firstDayDf = pd.concat(firstDayDfs)
    # print(len(firstDayDf))
    # firstDayDf.drop(firstDayDf[firstDayDf['measurement'] <= 14].index,inplace = True)
    firstDayDf.to_csv(dataDirectory+'{0}_all.csv'.format(first_date), index=False)
    # print(firstDayDf['measurement'].describe())
    # for s in toremove:
    #     sensors.remove(s)
    saveWeekDays(df,sensors)