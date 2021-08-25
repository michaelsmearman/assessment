import csv
import sys
from operator import itemgetter


def weather(filename):
    data = []
    #read in file
    with open(filename) as csvfile:
        data_obj = csv.reader(csvfile)
        header = next(data_obj)
        for row in data_obj:
            data.append(row)

    # split date
    for entry in data:
        entry[1] = entry[1].split()

    # create dict with key = location|date and the value = a dictionary with high,low,start,end
    data_dict = {}
    for entry in data:
        if entry[0] + "|" + entry[1][0] not in data_dict:
            #add to dictionary
            data_dict[entry[0] + "|" + entry[1][0]] = {
                "low": float(entry[2]),
                "high": float(entry[2]),
                "start": float(entry[2]),
                "end": float(entry[2])
            }
        else:
            #if start
            if entry[1][1] + " " + entry[1][2] == "12:00:00 AM":
                data_dict[entry[0] + "|" + entry[1][0]]["start"] = float(
                    entry[2])
            #if end
            if entry[1][1] + " " + entry[1][2] == "11:00:00 PM":
                data_dict[entry[0] + "|" + entry[1][0]]["end"] = float(
                    entry[2])
            #if high
            if float(entry[2]) > data_dict[entry[0] + "|" +
                                           entry[1][0]]["high"]:
                data_dict[entry[0] + "|" + entry[1][0]]["high"] = float(
                    entry[2])
            #if low
            if float(
                    entry[2]) < data_dict[entry[0] + "|" + entry[1][0]]["low"]:
                data_dict[entry[0] + "|" + entry[1][0]]["low"] = float(
                    entry[2])

    #sort keys so output file is sorted
    key_list = sorted(data_dict)

    #write to csv file
    with open("temperatureData.csv", 'w') as csvfile:
        fieldnames = [
            "Station Name", "Date", "Min Temp", "Max Temp", "First Temp",
            "Last Temp"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in key_list:
            date = key.split("|")
            writer.writerow({
                "Station Name": date[0],
                "Date": date[1],
                "Min Temp": data_dict[key]["low"],
                "Max Temp": data_dict[key]["high"],
                "First Temp": data_dict[key]["start"],
                "Last Temp": data_dict[key]["end"]
            })


if __name__ == "__main__":
    weather(sys.argv[1])
