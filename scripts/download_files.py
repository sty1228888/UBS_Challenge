
import os, sys, requests
file_urls = [
                "https://www.ubs.com/microsites/stockpitch-campus-competition/sc/financial-data-engineers/_jcr_content/mainpar/toplevelgrid/col1/innergrid/xcol2/textimage.1582499322.file/dGV4dD0vY29udGVudC9kYW0vYXNzZXRzL21pY3Jvc2l0ZXMvc3RvY2twaXRjaC1jYW1wdXMtY29tcGV0aXRpb24vbWFya2V0LWRhdGEtc3dhcC1yYXRlcy5jc3Y=/market-data-swap-rates.csv", 
                "https://www.ubs.com/microsites/stockpitch-campus-competition/sc/financial-data-engineers/_jcr_content/mainpar/toplevelgrid/col1/innergrid/xcol2/textimage.1837879185.file/dGV4dD0vY29udGVudC9kYW0vYXNzZXRzL21pY3Jvc2l0ZXMvc3RvY2twaXRjaC1jYW1wdXMtY29tcGV0aXRpb24vbWFya2V0LWRhdGEtc3dhcHRpb24tdm9scy5jc3Y=/market-data-swaption-vols.csv", 
                "https://www.ubs.com/microsites/stockpitch-campus-competition/sc/financial-data-engineers/_jcr_content/mainpar/toplevelgrid/col1/innergrid/xcol2/textimage.1710251132.file/dGV4dD0vY29udGVudC9kYW0vYXNzZXRzL21pY3Jvc2l0ZXMvc3RvY2twaXRjaC1jYW1wdXMtY29tcGV0aXRpb24vdHJhZGUtaW5mb3JtYXRpb24uY3N2/trade-information.csv", 
                "https://www.ubs.com/microsites/stockpitch-campus-competition/sc/financial-data-engineers/_jcr_content/mainpar/toplevelgrid/col1/innergrid/xcol2/textimage.1596096521.file/dGV4dD0vY29udGVudC9kYW0vYXNzZXRzL21pY3Jvc2l0ZXMvc3RvY2twaXRjaC1jYW1wdXMtY29tcGV0aXRpb24vdHJhZGUtcHJpY2UtaXItdmVnYXMuY3N2/trade-price-ir-vegas.csv"
            ]

def download_files(): 
    for file_url in file_urls: 
        filename = file_url.split('/')[-1]
        if (not os.path.exists(os.path.join("..", "assets", filename))): 
            print (f"Download the file {filename} ... ", end = "")
            try: 
                dst_path = os.path.join("..", "assets", filename)
                response = requests.get(file_url)
                with open(dst_path, "wb") as file:
                    file.write(response.content)
                if (os.path.exists(os.path.join("..", "assets", filename))): 
                    print ("SUCCESSFUL")
                    sys.stdout.flush()
                else: raise Exception
            except Exception: 
                print ("FAILED")
                sys.stdout.flush()
                print (f"-   Please manually download the file from {file_url} and save it to the assets folder. ")
        else: print (f"The file {filename} has already been downloaded. ")
