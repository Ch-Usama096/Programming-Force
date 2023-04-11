import numpy as np
from fractions import Fraction
from flask import Flask , render_template , url_for , request

def solution(m):
    #Get the length of the Matrix
    matrixSize = len(m)
    
    # Find the Total Sum of the All Rows
    sumRow = [sum(r) for r in m]
    
    # Apply the Check
    if sumRow[0] == 0:
        return [1, 1]

    # Indentifing the Which Row is 0
    rowZero = dict(zip(list(i for i in range(len(m))), list(0 if i == 0 else 1 for i in sumRow)))
    
    # Sort the Data
    rowZeros = {k: v for k, v in sorted(rowZero.items(), key=lambda item: item[1])}

    # Find the Row which are Zeros and Non-Zeros
    totalZeros = list(rowZero.values()).count(0)
    totalNzeros = len(m) - totalZeros

    # Performing the Absorbing Markov Chain 
    matrix = np.array(m)
    
    # Filter the Rows with Zeros
    matrixRow = matrix[list(rowZeros.keys()), :]
    # shafal with Columns
    matricRowCol = matrixRow[:, list(rowZeros.keys())]

    # Now, replacing the Fraction Number
    matrixRowSum = [sum(r) for r in matricRowCol]
    matrixNew = []
    for i in range(len(matricRowCol)):
        matrixNew.append(list(map(lambda x: 0 if matrixRowSum[i] == 0 
                            else x / matrixRowSum[i], matricRowCol[i])))

    matrixNew = np.array(matrixNew)

    # Find Q,R etc
    Q = matrixNew[totalZeros:, totalZeros:]
    R = matrixNew[totalZeros:, :totalZeros]
    ImQ = np.subtract(np.identity(totalNzeros), Q)
    F = np.linalg.inv(ImQ)
    FR = np.matmul(F, R)
    
    # fraction
    frac = []
    for i in range(totalNzeros):
        frac.append([Fraction.from_float(x).limit_denominator(max_denominator = 2**32) for x in FR[i]])

    # Transform final result
    maxd = max(list(map(lambda x: x.denominator, frac[0])))
    indv = list(map(lambda x: (x*maxd).numerator, frac[0]))
    return list(indv + [maxd])


# Create the Object of the Flask
app = Flask(__name__)

# Create the First Decorator
@app.route('/')
def home_page():
    return render_template("homePage.html")

@app.route('/matrix_request')
def user_matrix():
    return render_template("matrixPage.html")

@app.route('/process_request' , methods = ["GET" , "POST"])
def process():
    if request.method == "POST":
        matrix = request.form["matrix"]

        matrixSplit = matrix[1:-1].split("],")
        matrixList = []
        count = 0
        for index in range(0,len(matrixSplit)):
            getData = lambda count: 1 if count == 0 else 2
            var = getData(count)
            listData = []
            for data in matrixSplit[index][var::3]:
                listData.append(int(data))
            count += 1   
            matrixList.append(np.array(listData))
            
        finalMatrix = np.array(matrixList)
        
        # Call the Solution Function
        result = solution(finalMatrix)
        return render_template("displayResult.html" , res = result)

if "__main__" == __name__:
    app.run(debug=True)

