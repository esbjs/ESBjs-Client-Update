from request import  *;

class SDBDtask(SDBDRequest):
    def __init__(self, tokenId, port=None):
        SDBDRequest.__init__(self, tokenId, port);

    def New(self, table, key, data, bus="any", parameters=None):
        envelope = {"operation": "new", 'table': table, "key": key, "data": data, 'version': 2,
                    "driver": "task"}
        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())
        return self.SendServers(self.servers, envelope=envelope);


    def HasworkV2(self, bus="any", parameters=None):
        envelope = {"operation": "haswork", 'version': 2,
                    "driver": 'task'}
        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())
        return self.SendServers(self.servers, envelope=envelope);


    def TaskSucess(self, name, pos, sucess, bus="any", parameters=None):
        envelope = {"operation": "tasksucess", "driver": "task", 'name': name, 'version': 2, "pos": pos, "sucess": sucess}
        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);
#
#     def Create(self, date_exec, table, key, data, bus=None):
#         try:
#             envelope = {"operation": "testinsert", "table": table,
#                         "version": 0, "key": key, "data": data, "driver": "task"}
#             if bus != None:
#                 envelope['bus'] = bus;
#             return self.SendServers(self.servers, envelope=envelope);
#         except Exception as e:
#             print "Erro dentro TestInsert: " + str(e);
#
#     def Next(self, table, bus=None, no_update=False):
#         envelope = {"operation": "next", 'table': table, 'versao': 1, "driver" : "task", "no_update": no_update}
#         return self.SendServers(self.servers, envelope=envelope);
#
#     def EnviarConfirmacao(self, table, tarefa, sucesso, output, adicionar=1, tentativas=5):
#         try:
#             if (tarefa.get('_id')):
#                 del tarefa['_id'];
#             if (tarefa.get('__v')):
#                 del tarefa['__v'];
#
#             if not tarefa.get('status'):
#                 tarefa['status'] = {};
#             if not tarefa.get('tentativas'):
#                 tarefa['tentativas'] = 0;
#
#             tarefa['tentativas'] += 1;
#
#             if sucesso:
#                 tarefa['status']['status'] = "sucesso";
#                 tarefa['status']['output'] = '';
#             else:
#                 if tarefa['tentativas'] >= tentativas:
#                     tarefa['status']['status'] = "erro";
#                     tarefa['status']['output'] = output;
#             return self.TestInsert(table,
#                                    {"chave": tarefa["chave"]}, 'task', tarefa, bus='home');
#             # print resultado;
#         except Exception as e:
#             print "Erro dentro do processar: " + str(e);
#             traceback.print_exc()