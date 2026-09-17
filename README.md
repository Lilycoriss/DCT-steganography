# HOW IT WORKS
This algorithm operates in the image's frequency domain. To use it, we apply the Discrete Cosine Transform (DCT). It is important to work with the mid-range frequencies; otherwise, there is a risk of generating message-related artifacts or compromising the message due to image compression. We divide the image into 8x8 blocks to enable the DCT to function correctly, embed the message into the mid-range frequencies, and finally restore the image to its original state using the Inverse DCT (IDCT). The detailed operation is further explained and commented upon in the code. During the decoding phase, we perform the reverse process: after applying the DCT, we extract the binary message and decode it using a dedicated conversion function. 

## PREREQUISITES
1. **Clone your project**

2. **Create venv** (suggested):
   ```bash
   python -m venv .venv
   ```
   
3. **Activate venv**:
   * if you're using Windows, use this: `.venv\Scripts\Activate.ps1` (PowerShell)
   * or this: `.venv\Scripts\activate.bat` (CMD)
   * *if you're using Mac/Linux, use this: `source .venv/bin/activate`
  
4. **Install dependencies**:
     ```bash
     pip install -r requirements.txt
     ```

5. **Start the script**:
   ```bash
   python nome_del_tuo_file.py
   ```
   
   


