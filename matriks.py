def transpose(matrix):
    return list(map(list, zip(*matrix)))

def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

def matrix_inverse(matrix):
    n = len(matrix)
    identity = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    augmented = [matrix[i] + identity[i] for i in range(n)]

    for i in range(n):
        if augmented[i][i] == 0:
            for j in range(i + 1, n):
                if augmented[j][i] != 0:
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    break
            else:
                raise ValueError("Matrix is singular.")

        factor = augmented[i][i]
        augmented[i] = [x / factor for x in augmented[i]]

        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [x_j - factor * x_i for x_j, x_i in zip(augmented[j], augmented[i])]

    return [row[n:] for row in augmented]

def prepare_matrices(subset, model_types, transmission_types, fuel_types):
    X = []
    Y = []
    for _, row in subset.iterrows():
        model_features = [1 if row['model'] == model else 0 for model in model_types]
        transmission_features = [1 if row['transmission'] == trans else 0 for trans in transmission_types]
        fuel_features = [1 if row['fuelType'] == fuel else 0 for fuel in fuel_types]

        features = [1, row['mileage'], row['year'], row['engineSize'], row['mpg'], row['tax']]
        features.extend(model_features + transmission_features + fuel_features)
        X.append(features)
        Y.append(row['price'])
    return X, Y