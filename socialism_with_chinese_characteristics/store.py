import pickle
import os


class PretreatMgr:

    @staticmethod
    def save(weiboid, datas):
        file_name = "weibo_data/{weiboid}datas.pkl".format(weiboid=weiboid)
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, 'wb')
        pickle.dump(datas, file)

    @staticmethod
    def restore(weiboid):
        file_name = "weibo_data/{weiboid}datas.pkl".format(weiboid=weiboid)
        file = open(file_name, 'rb')
        return pickle.load(file)

    @staticmethod
    def save_file(folder_name, filename, datas):
        file_name = "{folder_name}/{filename}.pkl".format(folder_name=folder_name, filename=filename)
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, 'wb')
        pickle.dump(datas, file)

    @staticmethod
    def restore_file(folder_name, filename):
        file_name = "{folder_name}/{filename}.pkl".format(folder_name=folder_name, filename=filename)
        file = open(file_name, 'rb')
        return pickle.load(file)
