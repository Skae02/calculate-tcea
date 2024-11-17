import os
import numpy as np
from flask import Flask, jsonify, request

app=Flask(__name__)

@app.route("/calc-tcea", methods=["POST"])
def get_TCEA():
    data = request.get_json()
    cf = data["cf"]
    fecha = data["fecha"]
    print(fecha)
    print(cf)
    #cf=[71991.95,-11431,-10101,-9911,-13521, -10861, -10196, -11146]

    #fecha=['2024/11/17','2025/05/02', '2025/02/03', '2025/02/04','2025/02/02', '2025/02/05', '2025/05/02', '2025/01/04']

    year=[]
    fcha=[]

    for z in range(len(fecha)):
        fcha.append(int(fecha[z][0:4])*360+int(fecha[z][5:7])*30+int(fecha[z][8:10]))

    for z in range(len(fecha)):
        year.append(round(float((fcha[z])-fcha[0])/360,4))

    vant = []
    van = float(0)

    i = -9999
    while i<10000:
        for z in range(len(cf)):
            van = van + (-cf[z]/(1+i/10000)**(year[z]))
        vant.append(np.where(van>0,1,-1))
        van = 0
        if len(vant)>1:
            if vant[len(vant)-1]+vant[len(vant)-2]==0:
                print('El TIR es: ', round(float(i)/100,2),'%')
                tir=round(float(i)/100,2)
        i+=1
    tcea = {
       "tcea": tir
    }
    return jsonify(tcea),201

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
