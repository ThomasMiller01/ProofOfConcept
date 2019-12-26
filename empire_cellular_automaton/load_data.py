import couchdb

server = couchdb.Server('http://localhost:5984/')


db = server['dataset_test_1']

i = 0

print("Documents:")
for _id in db:
    data = db[_id]
    print('-----------')
    print('[' + str(i) + ']')
    print('id: ' + str(_id))
    print(data['settings'])
    print('-----------')
    i += 1
