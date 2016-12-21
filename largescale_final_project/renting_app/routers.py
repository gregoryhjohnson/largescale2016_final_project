LOGICAL_SHARDS = 128
PHYSICAL_SHARDS = 2
BASE_DB_NAME = 'db' #rental_app

#Helper function to create a mapping from logical to physical shards
def create_log_to_phy_mapping(logical_shards, physical_shards):
  mapping = []
  for x in range(0, logical_shards):
    db = BASE_DB_NAME + str(x % physical_shards + 1) #db names starting with 1
    mapping.append(db)
  return mapping

def logical_to_physical(logical_shard):
  mapping = create_log_to_phy_mapping(LOGICAL_SHARDS, PHYSICAL_SHARDS)

  return mapping[logical_shard]

def logical_for_user(user_id):
  return user_id % LOGICAL_SHARDS

def get_num_physical_shards():
  return PHYSICAL_SHARDS

class UserRouter(object):

  def db_for_user(self, user_id):
    return logical_to_physical(logical_for_user(user_id))

  def db_for_read_write(self, model, **hints):
    if model._meta.app_label == 'auth' or model._meta.app_label == 'sessions':
      return 'auth_db'

    db = None

    try:
      instance = hints['instance']
      if instance.user_id:
        db = self.db_for_user(instance.user_id)
    except AttributeError:
        db = self.db_for_user(instance.id)
    except KeyError:
      try:
        db = self.db_for_user(int(hints['user_id']))
      except KeyError:
        print('no instance in hints')

    return db

  def db_for_read(self, model, **hints):
    if model._meta.model_name == "category":
      return "auth_db"

    return self.db_for_read_write(model, **hints)

  def db_for_write(self, model, **hints):
    #Save all categories to the "master" db (db1), will be replicated across all dbs
    if model._meta.model_name == "category":
      return "auth_db"
    return self.db_for_read_write(model, **hints)

  def allow_relations(self, obj1, obj2, **hints):
    if (obj1._meta.app_label == 'auth' and obj2._meta.app_label == 'auth'):
      return True
    return False

  def allow_migrate(self, db, app_label, model=None, **hints):
    return True
