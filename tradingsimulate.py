from flask import Flask, jsonify
import numpy as np
import yfinance as yf

app = Flask(__name__)

# Lista de las 4 principales criptomonedas
criptomonedas = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'XRP-USD', 'LTC-USD']


def obtener_datos(cripto, start='2024-10-06', end='2024-10-07'):
    data = yf.download(cripto, start=start, end=end, interval='1h')
    return data


def jump_diffusion_simulation(precio_inicial, mu, sigma, Lambda, a, b, dias_simulacion, n_simulaciones):
    dt = 1 / dias_simulacion
    predicciones = np.zeros((n_simulaciones, dias_simulacion, 4))  # [open, high, low, close]

    for i in range(n_simulaciones):
        # Inicializa los valores de la primera vela
        predicciones[i, 0, 0] = precio_inicial  # Open
        predicciones[i, 0, 3] = precio_inicial  # Close
        predicciones[i, 0, 1] = precio_inicial  # High
        predicciones[i, 0, 2] = precio_inicial  # Low

        for t in range(1, dias_simulacion):
            epsilon = np.random.normal(0, 1)  # Componente Browniana
            salto_ocurre = np.random.poisson(Lambda * dt)  # Proceso de Poisson para determinar si ocurre un salto
            magnitud_salto = np.exp(a + b * np.random.normal()) if salto_ocurre > 0 else 1  # Magnitud del salto

            # Calcular el precio utilizando el modelo de Jump Diffusion
            precio = predicciones[i, t - 1, 3] * np.exp(
                (mu - 0.5 * sigma ** 2) * dt + sigma * epsilon * np.sqrt(dt)) * magnitud_salto

            # Asigna los valores de apertura, cierre, máximo y mínimo para el día t
            predicciones[i, t, 0] = predicciones[i, t - 1, 3]  # Open = Close del día anterior
            predicciones[i, t, 3] = precio  # Close
            predicciones[i, t, 1] = max(predicciones[i, t, 0], precio)  # High
            predicciones[i, t, 2] = min(predicciones[i, t, 0], precio)  # Low

    return predicciones.tolist()


@app.route('/simulate', methods=['GET'])
def simulate():
    resultados_criptomonedas = {}

    # Iterar sobre las 4 criptomonedas principales
    for cripto in criptomonedas:
        data = obtener_datos(cripto)

        # Usar el último precio como precio inicial
        precio_inicial = data['Close'].iloc[-1]

        # Calcular la tasa de crecimiento media y la volatilidad usando retornos logarítmicos
        retornos = np.diff(np.log(data['Close'].values))  # Retornos logarítmicos
        mu = np.mean(retornos)  # Tasa de crecimiento media
        sigma = np.std(retornos)  # Volatilidad (desviación estándar)

        # Configurar los parámetros de simulación
        dias_simulacion = 30  # Días a predecir
        n_simulaciones = 1000  # Número de simulaciones
        Lambda = 0.25  # Tasa de ocurrencia de saltos
        a = 0.2  # Media de la distribución lognormal para el salto
        b = 0.2  # Desviación estándar de la distribución lognormal para el salto

        # Ejecutar la simulación para la criptomoneda actual usando Jump Diffusion
        resultados = jump_diffusion_simulation(precio_inicial, mu, sigma, Lambda, a, b, dias_simulacion, n_simulaciones)

        # Agregar resultados al diccionario usando el nombre de la criptomoneda
        resultados_criptomonedas[cripto] = resultados

    # Devolver resultados en formato JSON
    return jsonify(resultados_criptomonedas)


@app.route('/cryptocurrency', methods=['GET'])
def cryptocurrencies():
    cryptos = [
        {"Name": "Bitcoin", "image": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
        {"Name": "Ethereum", "image": "https://www.pngall.com/wp-content/uploads/10/Ethereum-Logo-PNG-Pic.png"},
        {"Name": "Binance Coin", "image": "https://seeklogo.com/images/B/binance-coin-bnb-logo-CD94CC6D31-seeklogo.com.png"},
        {"Name": "Cardano", "image": "https://cdn4.iconfinder.com/data/icons/crypto-currency-and-coin-2/256/cardano_ada-1024.png"},
        {"Name": "Ripple", "image": "https://icons.iconarchive.com/icons/cjdowner/cryptocurrency/256/Ripple-icon.png"},
        {"Name": "Litecoin", "image": "https://icons.veryicon.com/png/System/Button%20UI%20-%20Requests%20%236/LiteCoin.png"}
    ]
    return jsonify(cryptos)


if __name__ == '__main__':
    app.run(debug=True)
