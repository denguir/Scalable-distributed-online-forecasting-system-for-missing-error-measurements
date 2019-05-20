import pandas as pd

filename = "../data/data.conv.txt"
dataDirectory = '../data/'
def getDataOfSensor(df,sensorId):
    sensorId = "{0}-0".format(sensorId)
    return df[df['sensorid']==sensorId]


def saveWeekDays(df,sensors):

    for i in range(1,8,1):
        date = '2017-03-0{0}'.format(i)
        dayDf = df[df['date']==date]
        dayDf.sort_values('time', inplace=True)
        dayDf.to_csv(dataDirectory+'{0}_all.csv'.format(date),index=False)
        for sensor in sensors:
            sensorDf = getDataOfSensor(dayDf,sensor)
            sensorDf.to_csv(dataDirectory+'{0}_sensor_{1}.csv'.format(date,sensor),index=False)

if __name__=="__main__":
    df = pd.read_csv(filename, header=None, delimiter=" ", names=["date", "time", "sensorid", "measurement", "voltage"],
                     dtype={"measurement": float, "voltage": float})
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    first_date = '2017-02-28'
    firstDay = df[df['date'] == first_date]
    firstDay.to_csv(dataDirectory+'{0}_all.csv'.format(first_date), index=False)
    firstDay.sort_values('time', inplace=True)
    sensors = [1, 24,2,3,33,35,22,25]
    for i in sensors:
        dayDf = getDataOfSensor(firstDay, i)
        dayDf.to_csv(dataDirectory+'{0}_sensor_{1}.csv'.format(first_date,i), index=False)
    saveWeekDays(df,sensors)