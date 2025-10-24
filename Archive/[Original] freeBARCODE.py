#apt install python3-qrcode or pip3 install qrcode[pil] (Windows)
#pip3 install Pillow

#cd C:\Users\nhulo\Documents\iMESPRO\BARCODE
##nohup uvicorn freeBARCODE:freeBARCODEApp --workers 1 --host 0.0.0.0 --port 25000

###################################################################################

# Libraries
from PIL import Image, ImageDraw, ImageFont
import qrcode
import uuid
import json
import requests
import random
import os
import re
import ast
import ssl
import time
import threading
import shutil
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncio
from fastapi.middleware.cors import CORSMiddleware

#Logging
import logging
logging.basicConfig(filename=r'BARCODE.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%y-%H:%M:%S')
logging.info('BARCODE') 

### AUTHENTICATION ENV ###
AUTH_USER = "imes"
AUTH_PASSWORD = "AHsguq6663ASgwfQw"

# Define params template	
class FreeBARCODEParams(BaseModel):
   USER: str
   PASSWORD: str
   Barcode_Text: str
   Printer_Name: Optional[str] = None
   
# Define API Instance	
freeBARCODEApp = FastAPI()
freeBARCODEApp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origin
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả method: GET, POST, PUT, DELETE, ...
    allow_headers=["*"],  # Cho phép tất cả headers
)

def freeBARCODEFunc_URL(**kargs):  
  
   dest_file_barcode = kargs["dest_file_barcode"]  
   Printer_Name = kargs["Printer_Name"]
   
   if (".pdf" in dest_file_barcode) and ("Thermal_Barcode" in Printer_Name):

      # Printing	  
      cmdline = 'FoxitPDFReader.exe /t \"'+dest_file_barcode+'\" '+Printer_Name
      print(cmdline)
      os.system(cmdline)

   else:
      return '{ "Result": "OK" }'
      
async def freeBARCODEFunc(**kargs): 

   # Input Params
   barcode_text = kargs["Barcode_Text"]
   printer_name = kargs["Printer_Name"]   
   
   RAND = time.strftime("%Y%m%d%H%M%S")+str(random.randint(10000000,99999999)) + "_" + str(uuid.uuid4())

   ###################################### 1st stamp QR #############################################################

   barcode_image = qrcode.make(barcode_text)
   barcode_image.save(f'Storage\\{RAND}.png')

   # CMD
   cmdline = f'magick "Storage\\{RAND}.png" -resize 260x260 "Storage\\{RAND}.png"'
   print(cmdline)   
   tmp_var = os.popen(cmdline).read()
   tmp_var = tmp_var.rstrip("\n")
       
   # CMD
   cmdline = f'java -jar pdfstamp\\pdfstamp.jar -i "Storage\\{RAND}.png" -l "22","0" -e "{RAND}" "Storage\\Thermal_Paper_35_22.pdf"'
   print(cmdline)
   tmp_var = os.popen(cmdline).read()
   tmp_var = tmp_var.rstrip("\n")

   ############################################ 2nd Stamp ###############################################

   # Empty image with white border and new size
   new_image = Image.new('RGB', (1200, 50), (255, 255, 255))

   # Object to draw text
   draw = ImageDraw.Draw(new_image)

   # Draw text
   fnt = ImageFont.truetype("Font\\arial.ttf", 45)
   draw.text((0, 0), barcode_text, fill=(0, 0, 0), font=fnt)

   # Save in file
   new_image.save(f'Storage\\{RAND}_2.png', 'PNG')

   # CMD
   cmdline = f'magick "Storage\\{RAND}_2.png" -resize 70% "Storage\\{RAND}_2.png"'
   print(cmdline)
   tmp_var = os.popen(cmdline).read()
   tmp_var = tmp_var.rstrip("\n")

   # CMD
   cmdline = f'java -jar pdfstamp\\pdfstamp.jar -i "Storage\\{RAND}_2.png" -l "110","25" -e "{RAND}" "Storage\\Thermal_Paper_35_22_{RAND}.pdf"'
   print(cmdline)
   tmp_var = os.popen(cmdline).read()
   tmp_var = tmp_var.rstrip("\n")

   os.rename(f"Storage\\Thermal_Paper_35_22_{RAND}_{RAND}.pdf", f"Storage\\Thermal_Paper_35_22_{RAND}_final.pdf")
   dest_file_barcode = f"Storage\\Thermal_Paper_35_22_{RAND}_final.pdf"

   ############################################  Printing Endpoint ###############################################
   try:   
      print(f"Printing file {dest_file_barcode} at printer {printer_name}...") 
      freeBARCODEFunc_URL(dest_file_barcode = dest_file_barcode, Printer_Name = printer_name)

   except:
      return '{ "Result": "ERROR. PRINTING FUNC" }'
	  
   return '{ "Result": "OK" }'
   
@freeBARCODEApp.post("/freeBARCODEReq")
async def freeBARCODEReq(request: Request, freeBARCODEParams: FreeBARCODEParams):

   logging.info(request.url)
   logging.info(request.client)
   logging.info(request.headers.get('User-Agent'))
   logging.info(freeBARCODEParams)
   
   # Params
   USER = freeBARCODEParams.USER
   PASSWORD = freeBARCODEParams.PASSWORD
   Barcode_Text = freeBARCODEParams.Barcode_Text
   Printer_Name = freeBARCODEParams.Printer_Name
   
   # Authentication API
   if ((USER == AUTH_USER) and (PASSWORD == AUTH_PASSWORD)):
      pass
      
   else:
      raise HTTPException(status_code=503, detail="Wrong Credentials")
	  
   # Call function
   resultFreeBARCODE = await freeBARCODEFunc(USER = USER, PASSWORD = PASSWORD, Barcode_Text = str(Barcode_Text), Printer_Name = str(Printer_Name))
   logging.info(resultFreeBARCODE)

   # Response
   if (json.loads(resultFreeBARCODE)["Result"] == "OK"):
      return json.loads(resultFreeBARCODE) 

   else:
      raise HTTPException(status_code=403, detail="Try Again")

### END ###