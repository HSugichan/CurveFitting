from statistics import mode
import sys
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import csv
import error_code as err
import fitting_model as fit
import os.path
import logging  # as log


logger = logging.getLogger()


def check_file_provided():
    if len(sys.argv) < 2:
        sys.exit(err.ErrorCode.MissingParameter)
    else:
        logging.info(f"{sys.argv[1]} is exist")
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
        logger.error("No valid line in file.")
        sys.exit(err.ErrorCode.NoContents)

    return x_array, y_array


def get_fitting_model_id():
    if len(sys.argv) < 3:
        sys.exit(err.ErrorCode.MissingParameter)
    id = fit.FittingModel.Linear
    try:
        id = fit.FittingModel.value_of(sys.argv[2])
    except ValueError:
        sys.exit(err.ErrorCode.InvalidArgs)

    logger.info(id.value)
    return id


linear = lambda x, a, b: a * x + b
parabolic = lambda x, a, b, c: a * x**2 + b * x + c
square = lambda x, a, b: parabolic(x, a, 0, b)
# sinusoidal = lambda x, a, q, b: a * np.sin(x - q) + b


def get_fitting_model(id: fit.FittingModel):
    if id == fit.FittingModel.Linear:
        return linear
    elif id == fit.FittingModel.Square:
        return square
    elif id == fit.FittingModel.Parabolic:
        return parabolic
    # elif id == fit.FittingModel.Sinusoidal:
    #     return sinusoidal
    else:
        sys.exit(err.ErrorCode.InvalidArgs)


def get_fitting_func(id: fit.FittingModel, popt):
    func = get_fitting_model(id)
    if id == fit.FittingModel.Linear:
        return lambda x: func(x, popt[0], popt[1])
    elif id == fit.FittingModel.Square:
        return lambda x: func(x, popt[0], popt[1])
    elif id == fit.FittingModel.Parabolic:
        return lambda x: func(x, popt[0], popt[1], popt[2])
    # elif id == fit.FittingModel.Sinusoidal:
    #     return lambda x: func(x, popt[0], popt[1], popt[2])
    else:
        sys.exit(err.ErrorCode.InvalidArgs)


def get_equation_name(id: fit.FittingModel, popt):
    if id == fit.FittingModel.Linear:
        return f"{popt[0]:.3e}x {popt[1]:+.3e}"
    elif id == fit.FittingModel.Parabolic:
        return f"{popt[0]:.3e}x^2 {popt[1]:+.3e}x {popt[2]:+.3e}"
    elif id == fit.FittingModel.Square:
        return f"{popt[0]:.3e}x^2 {popt[1]:+.3e}"
    else:
        raise ValueError(f"{id.value} is INVALID")


def view_fitting_curve(out_path, x, y, fit_x, fit_y, r_squared, func_name):
    plt.scatter(x, y, label="Raw")
    plt.plot(fit_x, fit_y, "--", label="Fitting")
    plt.legend()
    plt.title(f"func = {func_name}\nR^2 = {r_squared:.4f}")
    plt.savefig(
        out_path, dpi=300, orientation="portrait", transparent=False, pad_inches=0.0
    )
    if len(sys.argv) >= 4 and sys.argv[3] == "1":
        plt.show()

    plt.close()
    return


MIN_R2 = 0.95


def calc_r2(x, y, fit_y):
    residuals = np.array(y) - np.array(fit_y)
    rss = np.sum(residuals**2)  # residual sum of squares = rss
    tss = np.sum((y - np.mean(y)) ** 2)  # total sum of squares = tss
    r_squared = 1 - (rss / tss)
    logger.info(f"R^2={r_squared}")
    return r_squared


def get_dest_file():
    if len(sys.argv) < 5:
        logger.error("Not identified destination.")
        sys.exit(err.ErrorCode.MissingParameter)
    return sys.argv[4]


def write_csv(dest: str, popt):
    with open(dest, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [f"param{int(i)}" for i in np.linspace(0, len(popt) - 1, len(popt))]
        )
        writer.writerow(popt)


def setup_logger(dest_filename: str):
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")
    fh = logging.FileHandler(filename=dest_filename, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def main():
    file_path = check_file_provided()
    folderpath, file_name = os.path.split(file_path)
    filename_without_ext = os.path.splitext(file_name)[0]
    log_dir = f"{folderpath}/logs"
    os.makedirs(log_dir, exist_ok=True)
    setup_logger(f"{log_dir}/{filename_without_ext}.log")

    logger.info(f"args: {sys.argv}")
    x, y = read_model_data(file_path)
    id = get_fitting_model_id()
    fitting_func = get_fitting_model(id)
    popt, pcov = optimize.curve_fit(fitting_func, x, y)
    logger.info(f"params: {popt}")
    logger.info(f"covariance: {pcov}")
    write_csv(get_dest_file(), popt)

    f = get_fitting_func(id, popt)

    fit_x = np.linspace(0, max(x), 100)
    fit_y = f(fit_x)
    f_name = get_equation_name(id, popt)
    r2 = calc_r2(x, y, f(np.array(x)))
    view_fitting_curve(
        f"{folderpath}/{filename_without_ext}_fit.jpg", x, y, fit_x, fit_y, r2, f_name
    )
    if r2 < MIN_R2:
        logger.error(f"The residuals are TOO large.(R2 < {MIN_R2})")
        sys.exit(err.ErrorCode.LargeResidual)


# comanndline parameters <target file> <fitting model> <result viewer ON/OFF> <dest file>
if __name__ == "__main__":
    try:
        main()
        sys.exit(err.ErrorCode.Success)
    except Exception as e:
        logger.critical(e)
        sys.exit(err.ErrorCode.Unexpected)
