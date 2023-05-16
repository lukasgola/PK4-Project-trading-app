'''
This file contains a simple animation demo using mplfinance "external axes mode".

In this example, instead of creating the Figure and Axes external to mplfiance,
we allow mplfinance to create the Figure and Axes using its "panel method", and
set kwarg `returnfig=True` so that mplfinance will return the Figure and Axes.

We then take those Axes and pass them back into mplfinance ("external axes mode")
as part of the animation.

Note that presently mplfinance does not support "blitting" (blitting makes animation
more efficient).  Nonetheless, the animation is efficient enough to update at least
once per second, and typically more frequently depending on the size of the plot.
'''
import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

import yfinance as yf

idf = yf.download(tickers='BTC-USD', period='2d', interval='2m')

pkwargs=dict(type='candle', mav=(10,20))


fig, axes = mpf.plot(idf.iloc[0:50],returnfig=True,volume=True,
                     figsize=(11,8),panel_ratios=(2,1),
                     title='\n\nS&P 500 ETF',**pkwargs)
ax1 = axes[0]
ax2 = axes[2]

def animate(ival):
    if (50+ival) > len(idf):
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    
    idf2 = yf.download(tickers='BTC-USD', period='2d', interval='2m')

    data = idf2.iloc[0+ival:50+ival]
    ax1.clear()
    ax2.clear()
    mpf.plot(data,ax=ax1,volume=ax2,**pkwargs)

ani = animation.FuncAnimation(fig, animate, interval=1000)

mpf.show()