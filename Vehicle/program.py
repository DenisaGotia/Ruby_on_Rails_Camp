import math

class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Speed:
    # Speed = distance / time
    def __init__(self, distance, time):
        self.distance = distance
        self.time = time


class Car:
    networkBuffer = []
    def __init__(self, manufacturer, model, uniqueID):
        self._manufacturer = manufacturer
        self._model = model
        self._uniqueID = uniqueID
        self.speed = None
        self.coord = None

    def printinfo(self):
        print(f"Hi! My manufacturer is {self._manufacturer}, I'm {self._model} model and {self._uniqueID} is my unique ID")

    def readMessage(self):
            ctor=0
            for i in Car.networkBuffer:

                if i[1] == self:
                    print(Car.networkBuffer[ctor][2])
                ctor = ctor + 1

            #print(f"The car speed, coordinates or info were not set before")


    def sendinfo(self, object, identifier):
        if(identifier == "speed"):
            Car.networkBuffer.append(tuple((self, object, "Speed sent from " + self._uniqueID + " to " + object._uniqueID + " is " + str(self.getSpeed()) + "km/h")))
        elif(identifier == "coordinates"):
            Car.networkBuffer.append(tuple((self, object, "Coordinates sent from " + self._uniqueID + " to " + object._uniqueID + " is " + str(self.getCoordinates()))))
        else:
            Car.networkBuffer.append(tuple((self, object, "Information sent from " + self._uniqueID + " to " + object._uniqueID + " are: " + "uniqueId-" + self._uniqueID + ", manufacturer-" + self._manufacturer + ", model-" + self._model)))

    def getCoordinates(self):
        return (self.coordX, self.coordY)

    def setcoordinates(self, x, y):
        #global list
        self.coord = Coordinates(x, y)
        self.coordX = getattr(self.coord, 'x')
        self.coordY = getattr(self.coord, 'y')

        print(f"{self._uniqueID} from {self._manufacturer}: My current location in coordinates x and y is: ({self.coordX}, {self.coordY})")

    def getSpeed(self):
        return int(self.speed.distance / self.speed.time)

    def setspeed(self, distance, time):
        self.speed = Speed(distance, time)

        print(f"{self._uniqueID} from {self._manufacturer}: My current speed is {distance}/{time}")

    @staticmethod
    def getdistance(car1, car2):
        distance = math.sqrt(
                math.pow(car2.coordX - car1.coordX, 2)
                                +
                math.pow(car2.coordY - car1.coordY, 2)
                  )
        print(f"Distance between {car1._uniqueID} from {car1._manufacturer} and {car1._uniqueID} from {car2._manufacturer} is: {distance} km")

        return distance

    @staticmethod
    def picktheClosestCar(carlist, uniqueID):
         dictionary = {
             "uniqueID":  "distance"
         }
         for i in range(len(carlist)):
             # otherwise it will calculate the distance between herself and herself
             if carlist[i]._uniqueID != uniqueID._uniqueID:
               dictionary.update({carlist[i]._uniqueID: Car.getdistance(carlist[i], uniqueID)})

         dictionary.pop("uniqueID")
         for key, value in dictionary.items():
             if min(dictionary.values()) == value:
               print(f"The closest car to {uniqueID._uniqueID} from {uniqueID._manufacturer} is {key}")


def main():
    carlist = []
    audi = Car("AUDI", "A8", "i345")
    audi.printinfo()
    carlist.append(audi)

    bmw = Car("BMW", "Series 7", "g35g")
    bmw.printinfo()
    carlist.append(bmw)

    ford = Car("FORD", "Fiesta", "jie48")
    ford.printinfo()
    carlist.append(ford)

    seat = Car("SEAT", "Ibiza", "bgy5")
    seat.printinfo()
    carlist.append(seat)

    # set cars speed
    audi.setspeed(100, 1)
    ford.setspeed(80,1)

    # set cars coordinate
    audi.setcoordinates(4,5)
    bmw.setcoordinates(0,7)
    ford.setcoordinates(3,3)
    seat.setcoordinates(0,0)

    # calculate distance between audi and bmw
    Car.getdistance(audi,bmw)

    # get the closest car to audi
    Car.picktheClosestCar(carlist, audi)

    # send information between cars -> you can send between speed, coordinates or each car info
    audi.sendinfo(bmw, "coordinates") # audi send his coordinates to bmw
    ford.sendinfo(audi,"speed") # ford send his current speed to audi
    bmw.readMessage() # bmw reads what audi sent him
    audi.readMessage() # audi reads what ford sent him

if __name__ == '__main__':
 main()
