import streamlit as st
from matplotlib import pyplot as plt
import numpy as np

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Digital transmission dashboard',
    page_icon=':robot_face:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data

def digital_transmission(n,f):
    T = 1/f # periodo del reloj
    tiempo = np.arange(0,9*T,T/10)
    reloj = ((tiempo % T) < T/2)*(5)
    gradas = ((tiempo - T/2)//T).astype(int)
    datos = ((n>>gradas)&0b1)*5
    modulo = tiempo % T
    periodo = tiempo*0 + T/2
    fig = plt.figure(figsize=(6,4))

    ## gráfico superior (ax1)

    ax1 = plt.subplot(211)
    plt.ylabel("clock")
    plt.tick_params('x', labelbottom=False)
    ax1.set_xticks(np.arange(T/2,9*T,T))
    labels = []
    for i in range(0,9,1):
        labels.append(str(i) + 'T')
        if i != 0:
            plt.vlines(i*T-0.00005,0,5,linestyles ="dashed", colors ="c")
    ax1.set_xticklabels(labels)
    ax1.set_yticks([0,5])
    plt.plot(tiempo,reloj)

    ## gráfico inferior (ax2)
    ax2 = plt.subplot(212, sharex=ax1)
    plt.ylabel("voltage (V)")
    for i in range(1,9,1):
        plt.text(i*T-0.00005, 2.4, str(int(datos[int(np.where(tiempo == i*T)[0][0])]/5)))
        plt.vlines(i*T-0.00005,0,5,linestyles ="dashed", colors ="c")
    ax2.set_yticks([0,5])
    plt.plot(tiempo,datos)
    return fig    

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :robot_face: Digital transmission example

Change the number to be send and observe the result
'''

# Add some spacing
''
''

number = st.slider("Select the number to send", 0, 255)
n = int(number)
f = 1000            # frecuencia del reloj

b = bin(n)

f'''
## Steps
* Data Encoding: the number is encoded in binary format; in this case, the number {n} can be represented in binary as {b}.
* Signal Encoding: the signal is encoded such that a 1 corresponds to 5V and a 0 to 0V, and the order is defined as MSB (most significant bit first).
* Synchronizing transmitter and receiver: the clock will have a frequency of 1kHz, meaning that one bit is sent every 1ms.
* Sending data bit by bit: the transmitter changes the value of the bit when the clock transitions from 5V to 0V, and the receiver reads the bit when the clock transitions from 0V to 5V.
* Decoding the signal: the signal is decoded such that 5V corresponds to a 1 and 0V to a 0.
* Decoding the data: the number is decoded from the received binary; in this case, the binary {b} corresponds to the number {n}.
'''


st.pyplot(digital_transmission(n,f))