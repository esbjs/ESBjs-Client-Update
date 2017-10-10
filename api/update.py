from request import  *;

class SDBDupdate(SDBDRequest):
    def __init__(self, tokenId, port=None):
        SDBDRequest.__init__(self, tokenId, port);

    def SendList(self):
        return True;

    def List(self, files, bus=None, project="", parameters=None):
        envelope = {"operation": "list", 'files' : files, "driver" : "update", "project" : project}
        if bus != None:
            envelope['bus'] = bus;
        return self.SendServers(self.servers, envelope=envelope);

    def Read(self, path, project, bus=None, parameters=None):
        envelope = {"operation": "read", 'path': path, "driver": "update", "project" : project}
        if bus != None:
            envelope['bus'] = bus;
        return self.SendServers(self.servers, envelope=envelope);

    def Projects(self, projects, bus=None, parameters=None):
        envelope = {"operation": "projects", 'projects': projects, "driver": "update"}
        if bus != None:
            envelope['bus'] = bus;
        return self.SendServers(self.servers, envelope=envelope);