import pandas as pd


##############################################################################################
########################  FIRST FILE  ########################################################
##############################################################################################

## Loading data
raw_data = pd.read_csv('C:/Users/Pepe/Desktop/Projekty/ds_laptop_price_prediction/mediaexpert.csv', engine='python')
df = pd.read_csv('C:/Users/Pepe/Desktop/Projekty/ds_laptop_price_prediction/mediaexpert.csv', engine='python')

## Adding brand column
Brands = ["hp", "lenovo", "asus", "msi", "acer", "microsoft", "huawei", "apple", "dell", "lg", "fujitsu", "dynabook", "hiro", "hyperbook", "kiano", "kruger&matz" ]
def func(x):
    for item in Brands:
        if item in x.lower():
            return item
    else:
        return 0
df["Brand"] = df.Title.apply(lambda x: func(x))
df[df.Brand == 0]

## Spliting Screen column
df["screen_inches"] = df.Screen.apply(lambda x: x.split(',')[0].replace('"','')).astype(float)
df["screen_res"] = df.Screen.apply(lambda x: x.split(',')[1].replace('px','').replace(" ",""))
df["screen_touch"] = df.Screen.apply(lambda x: 1 if "dotykowy" in x.lower() else 0)

## Adding simplified CPU column
CPUs = ['i3', 'i5', 'i7', 'i9', 'xeon','celeron', 'athlon','ryzen 3','ryzen 5', 'ryzen 7','pentium']
def check_cpu(x):
    for item in CPUs:
        if item in x.lower():
            return item
    else:
            return "other"
df["CPU"] = df["Processor"].apply(lambda x: check_cpu(x))

## Adjusting RAM column
df["RAM"] = df["RAM"].astype(str)

## Spliting and cleaning Disk column
df.Disk.unique()

df["disk_hdd"] = df.Disk.apply(lambda x: x.split('+')[0] if "HDD" in x.split('+')[0] else "0")
df["disk_ssd"] = df.Disk.apply(lambda x: x.split('+')[0] if "SSD" in x.split('+')[0] else "0")
df["disk_flash"] = df.Disk.apply(lambda x: x.split('+')[0] if "Flash" in x.split('+')[0] else "0")
df["disk_emmc"] = "0"

df["rest"] = df.Disk.apply(lambda x: x.split(' + ')[1] if "+" in x else 0)
df.loc[df.rest.str[-3:] == "SSD", "disk_ssd"] = df.rest
df.loc[df.rest.str[-3:] == "HDD", "disk_hdd"] = df.rest
df.loc[df.rest.str[-5:] == "Flash", "disk_flash"] = df.rest

df.drop("rest", axis=1, inplace=True)

df["disk_hdd"] = df['disk_hdd'].apply(lambda x: str(x).replace("GB HDD","").replace(" ","").replace("250","256").replace("500","512").replace("1000", "1024").replace("2000", "2048"))
df["disk_ssd"] = df['disk_ssd'].apply(lambda x: str(x).replace("GB SSD","").replace(" ","").replace("250","256").replace("500","512").replace("1000", "1024").replace("2000", "2048"))
df["disk_ssd"] = df['disk_ssd'].apply(lambda x: str(x).replace("512(x2)","1024").replace("1000(x2)","2048").replace("1024(x2)","2048").replace("250","256"))
df["disk_flash"] = df['disk_flash'].apply(lambda x: str(x).replace("GB Flash","").replace(" ","").replace("250","256").replace("500","512").replace("1000", "1024").replace("2000", "2048"))

## Adding simplified GPU column
df["GPU"] = df["Graphic_card"].apply(lambda x: "integrated" if "Intel" in x or "Radeon Graphics" in x else x)

GPUs = ["geforce gtx", "geforce rtx", "geforce mx", "quadro rtx", "radeon vega", "radeon pro", "radeon rx", "radeon r", "radeon 5", "integrated" ]
def check_gpu(x):
    for item in GPUs:
        if item in x.lower():
            return item
    else:
            return "other"
df["GPU"] = df["GPU"].apply(lambda x: check_gpu(x))
                            
df.GPU.unique()


## Adding simplified OS column
def check_os(x):
    if "windows" in x.lower():
        return "windows"
    elif "macos" in x.lower() or "mac os" in x.lower():
        return "macOS"
    elif "linux" in x.lower():
        return "linux"
    elif "chrome os" in x.lower():
        return "chrome OS"
    else:
        return "none"

df["OS"] = df["Operating_system"].apply(lambda x: check_os(str(x)))

## Deleting rows without price
df = df[df["Discounted_price"].notna()]

## Adding info if the price is discounted
df["is_discounted"] = df.Price.apply(lambda x: 1 if pd.notnull(x) else 0)

## Deleting space in price
df["Price_int"] = df["Discounted_price"].apply(lambda x: x.replace(" ","")).astype(int)

## Adding shop name
df["Shop"] = "mediaexpert"

df1 = df

##############################################################################################
########################  SECOND FILE  #######################################################
##############################################################################################

raw_data = pd.read_csv('C:/Users/Pepe/Desktop/Projekty/ds_laptop_price_prediction/rtveuroagd.csv', engine='python')
df = pd.read_csv('C:/Users/Pepe/Desktop/Projekty/ds_laptop_price_prediction/rtveuroagd.csv', engine='python')

## Ajusting brand column
df.Brand = df.Brand.apply(lambda x: x.lower())

## Spliting Screen column
df["screen_inches"] = df.Screen.apply(lambda x: x.split(' ')[0].replace(',','.')).astype(float)
df["screen_res"] = df.Screen.apply(lambda x: x.split(',')[-1].replace("ekran dotykowy","").split("pikseli")[0].replace(" ",""))
df["screen_touch"] = df.Screen.apply(lambda x: 1 if "dotykowy" in x.lower() else 0)

## Adding simplified CPU column
df["CPU"] = df["Processor"].apply(lambda x: x.replace("Pentium®", "pentium").replace("Ryzen™","ryzen"))
df["CPU"] = df["CPU"].apply(lambda x: check_cpu(x))

## Adjusting RAM column
df['RAM'] = df['RAM'].apply(lambda x: x.split(" ")[0]).astype('str')

## Getting rid of disks without a type

list = df.Disk.apply(lambda x: len(x.split(" "))).values
for i in range(df.shape[0]):
    if list[i] !=3 and list[i] !=6:
        df.drop(i, inplace=True)
        
## Spliting and cleaning Disk column
df.Disk.unique()
        
df["disk_hdd"] = df.Disk.apply(lambda x: x.split(' ')[0] if "HDD" in x.split(' ')[2] else "0")
df["disk_ssd"] = df.Disk.apply(lambda x: x.split(' ')[0] if "SSD" in x.split(' ')[2] else "0")
df["disk_flash"] = df.Disk.apply(lambda x: x.split(' ')[0] if "Flash" in x.split(' ')[2] else "0")
df["disk_emmc"] = df.Disk.apply(lambda x: x.split(' ')[0] if "eMMC" in x.split(' ')[2] else "0")


def func1(x,y):
    try:
        if y in x.split(' ')[5]:
            return x.split(' ')[3]
    except IndexError:
            return 0

df.loc[(df["disk_ssd"]==0),"disk_ssd"] = df.Disk.apply(lambda x: func1(x,"SSD"))
df.loc[(df.Disk == '1 TB SSD 512 GB SSD'),"disk_ssd"] = "1536"

df["disk_hdd"] = df["disk_hdd"].astype('category').replace("250","256").replace("500","512").replace("1","1024").replace("2","2048").replace("2,00","2048")
df["disk_ssd"] = df["disk_ssd"].astype('category').replace("250","256").replace("500","512").replace("1","1024").replace("2","2048")
df["disk_flash"] = df["disk_flash"].astype('category').replace("250","256").replace("500","512").replace("1","1024").replace("2","2048")
df["disk_emmc"] = df["disk_emmc"].astype('category')

## Adding simplified GPU column
df["GPU"] = df["Graphic_card"].apply(lambda x: x.split(" + ")[0] if " + " in x else x)
df["GPU"] = df["GPU"].apply(lambda x: x.replace("nVidia®","Nvidia").replace("Intel®","Intel").replace("GeForce®","Geforce").replace("Radeon®","Radeon"))
df["GPU"] = df["GPU"].apply(lambda x: "integrated" if "Intel" in x or "Radeon Graphics" in x else x)
df["GPU"] = df["GPU"].apply(lambda x: check_gpu(x))

## Adding simplified OS column
df["OS"] = df["Operating_system"].apply(lambda x: check_os(str(x)))

## Deleting rows without price
df = df[df["Price"].notna()]

## Adding info if the price is discounted
df["is_discounted"] = df.Price.apply(lambda x: 1 if "taniej" in x.lower() else 0)

## Deleting cleaning price data
df["Price_int"] = df.Price.apply(lambda x: x.split(" z")[0].replace(" ",""))
df["Price_int"] = df["Price_int"].astype(int)

## Adding shop name
df["Shop"] = "eurortvagd"

## Adding discounted price column so we can combine dataframes 
df["Discounted_price"]=0

## Combining dataframes
df2 = pd.concat([df1,df])


###################### EXPORTING ####################
df2.to_csv('cleaned_data.csv', index=False)
