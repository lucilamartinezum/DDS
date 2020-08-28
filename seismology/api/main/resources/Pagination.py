from main.models import SensorModel
from main.models import UserModel

class SensorPagination:
    def __init__(self, sensors):
        self.sensors = sensors
    #filters
    def __userId_filter(self, *value):
        return self.sensors.filter(SensorModel.userId == value)
    def __status_filter(self, *value):
        return self.sensors.filter(SensorModel.status == value)
    def __active_filter(self, *value):
        return self.sensors.filter(SensorModel.active == value)
    def __userEmail_filter(self, *value):
        return self.sensors.join(SensorModel.user).filter(UserModel.email.like('%'+value+'%'))
    #order
    def __name_order_by_desc(self, *value):
        return sensors.order_by(SensorModel.name.desc() == value)
    def __name_order_by_asc(self, *value):
        return sensors.order_by(SensorModel.name.asc() == value)
    def __userId_order_by_desc(self, *value):
        return sensors.order_by(SensorModel.userId.desc() == value)
    def __userId_order_by_asc(self, *value):
        return sensors.order_by(SensorModel.userId.asc() == value)
    def __active_order_by_desc(self, *value):
        return sensors.order_by(SensorModel.active.desc() == value)
    def __active_order_by_asc(self, *value):
        return sensors.order_by(SensorModel.name.asc() == value)
    def __status_order_by_desc(self, *value):
        return sensors.order_by(SensorModel.status.desc() == value)
    def __status_order_by_asc(self, *value):
        return sensors.order_by(SensorModel.status.asc() == value)
    def __useremail_order_by_desc(self, *value):
        return sensors.join.order_by(SensorModel.user.email.desc() == value)
    def __useremail_order_by_asc(self, *value):
        return sensors.join.order_by(SensorModel.user.email.asc() == value)

    def apply_filter(self, key, value):
        filter_dict = {
            "sensorId": self.__userId_filter(),
            "status": self.__status_filter(),
            "active": self.__active_filter(),
            "user.email": self.__userEmail_filter()
        }
        return filter_dict[key](value)
    def apply_sortby(self, key, value):
        order_dict = {
            "sort_by": {
                "name.desc": self.__name_order_by_desc(),
                "name.asc": self.__name_order_by_asc(),
                "userId.des": self.__userId_order_by_desc(),
                "userId.asc": self.__userId_order_by_asc(),
                "active.des": self.__active_order_by_desc(),
                "active.asc": self.__status_order_by_asc(),
                "status.des": self.__status_order_by_desc(),
                "status.asc": self.__status_order_by_asc(),
                "user.email.des": self.__useremail_order_by_desc(),
                "user.email.asc": self.__useremail_order_by_asc()
            }
        }
        return order_dict[key][key](value)