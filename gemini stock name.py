import yfinance as yf
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

sectors = {
    "IT": [
        "TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", 
        "LTIM.NS", "COFORGE.NS", "PERSISTENT.NS", "MPHASIS.NS", "KPITTECH.NS",
        "CYIENT.NS", "TATAELXSI.NS", "BSOFT.NS", "ZENSARTECH.NS", "SONATSOFTW.NS"
    ],
    "Banking & Finance": [
        "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS", 
        "PNB.NS", "BOB.NS", "INDUSINDBK.NS", "FEDERALBNK.NS", "BAJFINANCE.NS",
        "BAJAJFINSV.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "IDFCFIRSTB.NS"
    ],
    "Auto": [
        "TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", 
        "TVSMOTOR.NS", "EICHERMOT.NS", "ASHOKLEY.NS", "BOSCHLTD.NS", "MRF.NS",
        "BALKRISIND.NS", "APOLLOTYRE.NS", "ESCORTS.NS", "TIINDIA.NS", "MOTHERSON.NS"
    ],
    "Pharma": [
        "SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "LUPIN.NS", 
        "AUROPHARMA.NS", "BIOCON.NS", "TORNTPHARM.NS", "ZYDUSLIFE.NS", "GLENMARK.NS",
        "MANKIND.NS", "ABBOTINDIA.NS", "SYNGENE.NS", "LAURUSLABS.NS", "IPCALAB.NS"
    ],
    "FMCG": [
        "ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS", "TATACONSUM.NS", 
        "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "COLPAL.NS", "VBL.NS",
        "UBL.NS", "UNITEDSPR.NS", "PGHH.NS", "RADICO.NS", "EMAMILTD.NS"
    ],
    "Energy & Power": [
        "RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS", 
        "ADANIPOWER.NS", "TATAPOWER.NS", "GAIL.NS", "BPCL.NS", "IOC.NS",
        "HINDPETRO.NS", "NHPC.NS", "SJVN.NS", "TORNTPOWER.NS", "JSWENERGY.NS"
    ]
}

results = []
for sector, tickers in sectors.items():
    try:
        data = yf.download(tickers, period="1d", group_by="ticker", threads=True, progress=False)
        for ticker in tickers:
            try:
                if len(tickers) > 1:
                    # yf.download dictionary/dataframe structure handling
                    df = data[ticker] if ticker in data else None
                else:
                    df = data
                    
                if df is not None and not df.empty and 'Close' in df:
                    ltp = df['Close'].iloc[-1]
                    if pd.isna(ltp):
                        continue
                        
                    ltp = round(float(ltp), 2)
                    stock_name = ticker.replace(".NS", "")
                    
                    # Core trading rules calculation
                    entry = ltp
                    target = round(ltp * 1.05, 2)
                    sl = round(ltp * 0.98, 2)
                    
                    results.append({
                        "Sector": sector,
                        "Stock Name": stock_name,
                        "LTP (Live Price)": entry,
                        "Entry Price": entry,
                        "Target (Exit)": target,
                        "Stop Loss": sl
                    })
            except Exception as e:
                pass
    except Exception as e:
        pass

df_results = pd.DataFrame(results)
file_path = "/mnt/data/Sector_Wise_Stock_Levels.txt"
# Save as comma-separated txt which easily imports to Google Sheets
df_results.to_csv(file_path, sep=",", index=False)
print(f"File created at {file_path} with {len(df_results)} records.")