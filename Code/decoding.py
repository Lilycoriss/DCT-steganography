from PIL import Image
from scipy.fftpack import dctn
import numpy as np

def bin_to_text(binary) :
    text="" #inizializzo una stringa vuota
    for i in range(0, len(binary), 8): #scorriamo la stringa
        byte=binary[i:i+8]
        if len(byte)==8: #controlla che il byte sa effettivamente composto da 8 bit
            text+=chr(int(byte,2)) #se il controllo non è errato, fa la conversione a char
    return text

#apriamo l'immagine steganografata
stego_img=Image.open("stego-lena.png")
y, cb, cr=stego_img.split()

#padding in Y, consiste nell'aggiungere pixel inpiù in modo da avere blocchi perfetti da 8x8, altrimenti la dct non funziona correttamente
img_arr=np.array(y)
h,w=img_arr.shape
pad_h=(8-(h%8))%8
pad_w=(8-(w%8))%8
img=np.pad(img_arr, ((0,pad_h), (0,pad_w)), mode='edge').astype(float)

new_h, new_w=img.shape
bits=""

#ciclo per prendere i bit e decodificarli
for i in range(0, new_h, 8):
    for j in range(0, new_w, 8):
        chunk=img[i:i+8, j:j+8]
        dct=dctn(chunk, norm='ortho')

        cm1=dct[4,3]
        cm2=dct[5,2]

        #rispettando la regola in embedding, capiamo se il bit è 0 o 1
        if cm1>cm2:
            bits+="1"
        elif cm1<cm2:
            bits+="0"

#questa è la parte dove ci occupiamo di memorizzare SOLO il messaggio, in modo da poterlo stampare in maniera pulita e corretta,
#sia in binario che in formato testo.
raw_text=bin_to_text(bits)
text=raw_text.split("###")[0]
bits_found = bits[:(len(text) + 3) * 8]
binary_message = " ".join([bits_found[i:i+8] for i in range(0, len(bits_found), 8)])

print("Trovato messaggio in binario:")
print(binary_message)
print("\n\nDecodifico messaggio...");
print("Messaggio decodificato: ", text)
