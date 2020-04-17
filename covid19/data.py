import pandas as pd
import os
import datetime
from django.conf import settings


class ECDCDataSet:
    """Data Set from European Centre for Disease Prevention and Control
    
    Returns:
        [type]: [description]
    """
    __covid_data = None
    __expiration = None

    @property
    def covid_data(self):
        if self.__covid_data is None or self.__expiration > datetime.datetime.now():
            local_file = os.path.join(settings.BASE_DIR, 'covid.csv')
            if os.path.exists(local_file):
                uri = local_file
            else:
                uri = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
            self.__covid_data = pd.read_csv(
                uri, 
                index_col='dateRep', 
                parse_dates=True,
                date_parser=lambda x: pd.datetime.strptime(x, "%d/%m/%Y")
            )

            self.__expiration = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 3)
        return self.__covid_data

    @property
    def columns(self):
        self.covid_data.columns

    def filter(self, column, value):
        return self.covid_data[self.covid_data[column] == value]
