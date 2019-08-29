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
        self.Err = 'True'
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


class MetaDataClass:
    def __init__(self,servers):
        self.servers = servers

    def addServers(self,servers):
        for count in range(len(servers)):
            self.servers.append(servers[count])

     


