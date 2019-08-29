class constraintClass:
    def __init__(self):
        self.time_min = '2010-07-10T00:00:00Z'
        self.time_max = '2016-08-10T00:00:00Z'
        self.lon_min = -72.0
        self.lon_max = -69.0
        self.lat_min = 38.0
        self.lat_max = 41.0

    def updateTimeMin(self, timeMin):
        self.time_min = timeMin

    def updateTimeMax(self, timeMax):
        self.time_max = timeMax

    def updatelonMin(self, lonMin):
        self.lon_min = lonMin

    def updatelonMax(self, lonMax):
        self.lon_max = lonMax

    def updatelatMin(self, latMin):
        self.lat_min = latMin

    def updatelatMax(self, latMax):
        self.lat_max = latMax


class dataSetsClass:
    def __init__(self):
        self.dataset_ID = []
        self.lon = []
        self.lat = []
        self.has_LonLat = 'False'
        self.datasetType = ''


    def set_ID(self,datasetID):
        self.dataset_ID = datasetID

    def set_datasetType(self,datasetType):
        self.datasetType = datasetType

    def set_lon_lat(self, lon,lat):
        if self.datasetType == 'tabledap':
            if len(lon) != len(lat):
                print('longitue and latitude are not equal')
            else:
                self.lon = lon
                self.lat = lat
        else:
            self.lon = lon
            self.lat = lat


class serverClass:
    def __init__(self,serverURL):
        self.url = serverURL
        self.datasets = []
        self.Err = True
        self.num_tableDAP = 0
        self.num_gridDAP = 0
        self.num_WMS = 0

    def addDatasets(self,dataset):
        self.datasets.append(dataset)
        #self.Err = 'False'

    def set_num_TableGridWms(self,table,grid,WMS):
        self.num_tableDAP = table
        self.num_gridDAP = grid
        self.num_WMS = WMS
        
    def removeDatasets(self,dataset):
        num_datasets = len(self.datasets)
        flag = False
        index = -99999
        for i in range(num_datasets):
            if self.datasets[i].dataset_ID == dataset.dataset_ID:
                index = i
                flag = True
                break
        self.datasets.pop(index)
        
                


class MetaDataClass:
    def __init__(self,servers):
        self.servers = servers

    def addServers(self,servers):
        for count in range(len(servers)):
            self.servers.append(servers[count])

     


