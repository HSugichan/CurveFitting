from statistics import mode
import sys
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import csv
import error_code as err
import math
import fitting_model as fit

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
    id= fit.FittingModel.Linear
    try:
        id = fit.FittingModel.value_of(sys.argv[2])
    
    except ValueError:
        sys.exit(err.ErrorCode.InvalidArgs)

    print(id.value)
    return id


linear = lambda x, a, b: a * x + b
quadratic=lambda x,a,b,c:a*x**2+b*x+c
square = lambda x, a, b: quadratic(x,a,0,b)
sinusoidal=lambda x,a,q,b: a*math.sin(x-q)+b

def get_fitting_model(id: fit.FittingModel):
    if id == fit.FittingModel.Linear:
        return linear
    elif id == fit.FittingModel.Square:
        return square
    elif id== fit.FittingModel.Quadratic:
        return quadratic
    elif id == fit.FittingModel.Sinusoidal:
        return sinusoidal
    else:
        sys.exit(err.ErrorCode.InvalidArgs)

def get_fitting_func(id: fit.FittingModel,popt):
    func=get_fitting_model(id)
    if id == fit.FittingModel.Linear:
        return lambda x: func(x,popt[0],popt[1])
    elif id == fit.FittingModel.Square:
        return lambda x: func(x,popt[0],popt[1])
    elif id== fit.FittingModel.Quadratic:
        return lambda x: func(x,popt[0],popt[1],popt[2])
    elif id==fit.FittingModel.Sinusoidal:
        return lambda x: func(x,popt[0],popt[1],popt[2])
    else:
        sys.exit(err.ErrorCode.InvalidArgs)


def view_fitting_curve(x, y, id: fit.FittingModel, popt):
    if len(sys.argv) < 4 or sys.argv[3] != "1":
        return
    plt.scatter(x, y, label="Raw")
    x_new = np.linspace(0, max(x), 100)
    fit_y = [get_fitting_func(id,popt)(x_i) for x_i in x_new]
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
    view_fitting_curve(x, y, id, popt)


# comanndline parameters <target file> <fitting model> <view model>
if __name__ == "__main__":
    main()
    sys.exit(err.ErrorCode.Success)
