import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os
import imageio

# Lista dei principali ticker globali
global_tickers = [
    "AAPL", "MSFT", "AMZN", "TSLA", "GOOGL",  # USA
    "RDSA.L", "BAS.DE", "AIR.PA", "SIE.DE", "BP.L",  # Europa
    "7203.T", "6758.T", "9984.T", "601318.SS", "600519.SS"  # Asia
]

# Cartelle di output
output_folder = "grafici_interattivi_gif"
os.makedirs(output_folder, exist_ok=True)

# Loop su ogni ticker
for ticker in global_tickers:
    print(f"Scarico dati per {ticker}...")

    # Scarichiamo i dati
    df = yf.download(ticker, period="1y", interval="1d")

    # Controlliamo se ci sono dati scaricati
    if df.empty:
        print(f"Nessun dato trovato per {ticker}, saltato.")
        continue

    # Resettiamo l'indice per rendere le date una colonna
    df = df.reset_index()

    # Se il DataFrame ha un MultiIndex nelle colonne, lo appiattiamo
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # Calcoliamo media mobile a 20 giorni
    df['MA20'] = df["Close"].rolling(window=20).mean()

    # Creiamo una lista di immagini per l'animazione
    frames = []
    for i in range(1, len(df)):
        # Creiamo un grafico interattivo con Plotly
        fig = go.Figure()

        # Linea principale dei prezzi
        fig.add_trace(go.Scatter(
            x=df["Date"][:i], y=df["Close"][:i],
            mode="lines+markers",
            line=dict(color="royalblue", width=3),
            marker=dict(size=6, color="red", opacity=0.7),
            name="Prezzo di chiusura"
        ))

        # Media mobile a 20 giorni
        if i >= 20:
            fig.add_trace(go.Scatter(
                x=df["Date"][:i], y=df["MA20"][:i],
                mode="lines",
                line=dict(color="orange", width=2, dash="dash"),
                name="Media Mobile 20gg"
            ))

        # Annotazioni: primo e ultimo valore
        fig.add_trace(go.Scatter(
            x=[df["Date"].iloc[0]],
            y=[df["Close"].iloc[0]],
            mode="markers+text",
            text=[f"Primo: {df['Close'].iloc[0]:.2f}"],
            textposition="bottom center",
            marker=dict(size=10, color="green", symbol="triangle-up"),
            name="Primo"
        ))
        fig.add_trace(go.Scatter(
            x=[df["Date"].iloc[i - 1]],
            y=[df["Close"].iloc[i - 1]],
            mode="markers+text",
            text=[f"Ultimo: {df['Close'].iloc[i - 1]:.2f}"],
            textposition="top center",
            marker=dict(size=10, color="purple", symbol="triangle-down"),
            name="Ultimo"
        ))

        # Layout del grafico
        fig.update_layout(
            title={
                "text": f"Andamento giornaliero di {ticker}",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top"
            },
            xaxis_title="Data",
            yaxis_title="Prezzo di chiusura",
            font=dict(family="Arial, sans-serif", size=12, color="black"),
            plot_bgcolor="white",
            paper_bgcolor="#f8f9fa",
            width=800,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40),
            annotations=[
                dict(
                    text=f"Ticker: {ticker} - Mercato: {ticker.split('.')[1] if '.' in ticker else 'USA'}",
                    x=0.5, y=-0.2,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=10, color="grey")
                )
            ]
        )

        # Salviamo il frame come immagine
        image_path = os.path.join(output_folder, f"{ticker}_frame_{i}.png")
        fig.write_image(image_path)
        frames.append(image_path)

    # Creiamo un'animazione GIF dai frame
    gif_path = os.path.join(output_folder, f"{ticker}_andamento.gif")
    with imageio.get_writer(gif_path, mode="I", duration=0.1) as writer:
        for frame in frames:
            writer.append_data(imageio.imread(frame))

    # Rimuoviamo i frame temporanei
    for frame in frames:
        os.remove(frame)

    print(f"Grafico interattivo animato salvato come GIF: {gif_path}")

print("Tutti i grafici interattivi animati sono stati generati con successo!")
