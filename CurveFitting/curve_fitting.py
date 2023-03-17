from statistics import mode
import sys
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import csv
import error_code as err


def check_file_provided():
    default_path = "./test.exe"
    if len(sys.argv) < 2:
        sys.exit(err.ErrorCode.MissingParameter)
    else:
        print("")
        print(f"{sys.argv[1]} is exist")
        print("")
        return sys.argv[1]


def read_model_data(model_file: str):
    with open(model_file, mode="r", encoding="utf-8", newline="") as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        print(header)
        x_array = []
        y_array = []
        for row in reader:
            if len(row) < 2:
                print(row)
                continue
            x = float(row[0])
            y = float(row[1])
            x_array.append(x)
            y_array.append(y)
            print(f"(x,y)=({x},{y})")
    if len(x_array) < 1 or len(y_array) < 1:
        print("No valid line in file.")
        sys.exit(err.ErrorCode.NoContents)

    return x_array, y_array


def get_fitting_model_id():
    if len(sys.argv) < 3:
        sys.exit(err.ErrorCode.MissingParameter)
    id = int(sys.argv[2])
    if id == 1:
        print("linear")
    elif id == 2:
        print("square")
    else:
        sys.exit(err.ErrorCode.InvalidArgs)
    return id


linear = lambda x, a, b: a * x + b
square = lambda x, a, b: a * x**2 + b


def get_fitting_model(id: int):
    if id == 1:
        return linear
    elif id == 2:
        return square
    else:
        sys.exit(err.ErrorCode.InvalidArgs)


def view_fitting_curve(x, y, fitting_model, popt):
    if len(sys.argv) < 4 or sys.argv[3] != "1":
        return
    plt.scatter(x, y, label="Raw")
    x_new = np.linspace(0, max(x), 100)
    fit_y = [fitting_model(x_i, popt[0], popt[1])
             for x_i in np.linspace(0, max(x), 100)]
    plt.plot(x_new, fit_y, "--", label="Fitting")
    plt.legend()
    plt.title(f"Proportional Constant = {popt[0]}")
    plt.show()
    plt.close()


def main():
    print(f"args: {sys.argv}")
    file_path = check_file_provided()
    x, y = read_model_data(file_path)
    id = get_fitting_model_id()
    fitting_func = get_fitting_model(id)
    popt, pcov = optimize.curve_fit(fitting_func, x, y)
    print(f"params: {popt}")
    print(f"covariance: {pcov}")
    view_fitting_curve(x, y, fitting_func, popt)


# comanndline parameters <target file> <fitting model> <view model>
if __name__ == "__main__":
    main()
    sys.exit(err.ErrorCode.Success)
