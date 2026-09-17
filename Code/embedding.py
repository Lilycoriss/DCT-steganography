from PIL import Image
from scipy.fftpack import dctn, idctn
import numpy as np

#funzioni utili per conversioni da bin a testo e viceversa
def text_to_bin() :
    messaggio=input("Inserisci messaggio da nascondere: ") + "###"
    return "".join([format(ord(x), '08b') for x in messaggio])

#per prima cosa creiamo un oggetto Image per aprire la nostra immagine e convertirla poi in scala di grigi
cover_image=Image.open("lena.png")
ycbcr_image=cover_image.convert("YCbCr") #usiamo YCbCr per poter mantenere i colori dell'immagine

y_channel, cb_channel, cr_channel=ycbcr_image.split()

#"convertiamo" l'immagine in un array numpy, ci sarà utile per manipolare le dimensioni e suddividerla in blocchi 8*8
img_arr=np.array(y_channel)
h,w=img_arr.shape
pad_h=(8-(h%8))%8
pad_w=(8-(w%8))%8
img=np.pad(img_arr, ((0,pad_h), (0,pad_w)), mode='edge')
image_resized = Image.fromarray(img)

#suddivido l'immagine in blocchi 8*8 e applico la DCT
stego_img=img.astype(float).copy()
new_h, new_w=img.shape

#preparo il messaggio
bin_message=text_to_bin()
size_message=len(bin_message)
index=0 #inizializzo l'indice di partenza
check_var=10.0 #variabile che ci permette di non andare incontro ad errori dovuti ad arrotondamenti

for i in range(0, new_h, 8):
    for j in range(0, new_w, 8):
        block=stego_img[i:i+8, j:j+8]

        dct=dctn(block, norm='ortho')

        #---FASE DI EMBEDDING DEL MESSAGGIO---
        if index<size_message:
            bit=bin_message[index]

        #coefficienti a media frequenza del singolo blocco
            cm1=dct[4,3]
            cm2=dct[5,2]

            if bit=='1':
                if cm1-cm2<check_var:
                    dct[4,3]=(cm1+cm2+check_var)/2
                    dct[5,2]=(cm1+cm2-check_var)/2
            elif bit=='0':
                if cm2-cm1<check_var:
                    dct[4,3]=(cm1+cm2-check_var)/2
                    dct[5,2]=(cm1+cm2+check_var)/2
            index+=1
        stego_img[i:i+8, j:j+8]=idctn(dct, norm='ortho')
#andiamo a modificare solo la luminanza per efficienza e per una questione di percezione umana, infatti l'occhio umano è poco sensibile ai piccoli dettagli
# di cromaticità, quindi possiamo anche lasciare Cb e Cr invariati
mod_y=np.clip(stego_img, 0, 255).astype(np.uint8) #andiamo a modificare solo la luminanza per efficienza e per una questione di percezione umana

y_cropped=mod_y[:h, :w]

y_img=Image.fromarray(y_cropped)

stego_image=Image.merge("YCbCr", (y_img, cb_channel, cr_channel)).convert("RGB") #riconverto a colori RGB
stego_image.save("stego-lena.png")

print("Immagine steganografata con successo.")
