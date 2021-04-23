from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Classification:
    lat: float
    lon: float
    name: str = field(init=False)
    minlon: float = field(init=False)
    minlat: float = field(init=False)
    maxlon: float = field(init=False)
    maxlat: float = field(init=False)

    def get_classification(self) -> object:
        """
          Get a classification to coordinates based in the business rules
          :return: str
        """
        if (-46.361899 <= self.lat <= -34.276938) and (
            -2.196998 >= self.lon >= -15.411580
        ):
            self.minlat = (-46.361899,)
            self.maxlat = (-34.276938,)
            self.minlon = (-2.196998,)
            self.maxlon = (-15.411580,)
            self.name = "ESPECIAL1"

        elif (-52.997614 <= self.lat <= -44.428305) and (
            -19.766959 >= self.lon >= -23.966413
        ):
            self.minlat = (-52.997614,)
            self.maxlat = (-44.428305,)
            self.minlon = (-19.766959,)
            self.maxlon = (-23.966413,)
            self.name = "ESPECIAL2"

        elif (-54.777426 <= self.lat <= -46.603598) and (
            -26.155681 >= self.lon >= -34.016466
        ):
            self.minlat = (-54.777426,)
            self.maxlat = (-46.603598,)
            self.minlon = (-26.155681,)
            self.maxlon = (-34.016466,)
            self.name = "NORMAL"

        else:
            """
            Create a range to filter in dataframe
            """
            self.minlat = (self.lat - 30.0000,)
            self.maxlat = (self.lat + 30.0000,)
            self.minlon = (self.lon - 30.0000,)
            self.maxlon = (self.lon + 30.0000,)
            self.name = "TRABALHOSO"

        return self.name

    def __repr__(self):
        return f"Entity: {self.__class__.__name__}<lat: {self.lat}, lon: {self.lon}>"
