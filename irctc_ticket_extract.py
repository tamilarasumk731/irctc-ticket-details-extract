from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from collections import defaultdict,OrderedDict
import pandas as pd
import re


from io import StringIO
def pdf_to_text(pdfname):
    resmanager = PDFResourceManager()
    io=StringIO()
    device = TextConverter(resmanager,io, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(resmanager, device)
    fp = open(pdfname,'rb')
    page=list(PDFPage.get_pages(fp))
    interpreter.process_page(page[0])
    fp.close()
    text = io.getvalue()
    device.close()
    io.close()
    return text

dictionary=defaultdict(list)
files=["C:/Users/Tamil SB/Documents/Python Scripts/1.pdf","C:/Users/Tamil SB/Documents/Python Scripts/1.pdf"]
for fp in files:
    t = pdf_to_text(fp)

    tablecontent=t[t.index('\xa0'):t.rindex('\xa0')].replace('\xa0',' ')

    pnr = int(list(re.findall(r'PNR No:[\s]+([0-9]{10})',tablecontent))[0])
    t_details = list(re.findall(r'Train No. & Name:[\s]+([0-9]{5})+[/]+([A-Z]+)+[\s]+([A-Z]+)',tablecontent))[0]
    quota = str(list(re.findall(r'Quota:[\s]+([A-Z]+)',tablecontent))[0])
    from_loc = str(list(re.findall(r'From:+([A-Z]+)',tablecontent))[0])
    to_loc = str(list(re.findall(r'To:+([A-Z]+)',tablecontent))[0])
    tic_fare = float(list(re.findall(r'Total Fare \(all inclusive\)([0-9.]+)',tablecontent))[0])
    t_no = int(list(t_details)[0])
    t_name = str(list(t_details)[1])+' '+str(list(t_details)[2])
    pass_det=str(re.findall(r'(PASSENGER DETAILS :[\S\s]+)Indian Railways GST Details',tablecontent))
    specs=re.findall(r'[A-Z\s]+[0-9]{1,2}\s(?:Male|Female)',pass_det)

    for i in range(len(specs)):
        split_specs=re.search(r'([A-Z\s]+)([0-9]{1,2}\s)((?:Male|Female))',specs[i])
        dictionary["PNR no."].append(pnr)
        dictionary["Ticket no."].append(t_no)
        dictionary["Passenger Name"].append(split_specs.group(1).strip())
        dictionary["Age"].append(split_specs.group(2).strip())
        dictionary["Gender"].append(split_specs.group(3).strip())
        dictionary["Train name"].append(t_name)
        dictionary["Quota"].append(quota)
        dictionary["From"].append(from_loc)
        dictionary["TO"].append(to_loc)
        dictionary["Ticket fare"].append(tic_fare)
df = pd.DataFrame.from_dict(OrderedDict(dictionary))
df1=df.drop_duplicates(subset=['PNR no.', 'Ticket no.','Passenger Name','Age'], keep="first")
df1.head()

output_loc = 'C:/Users/Tamil SB/Documents/Python Scripts/1.csv'

try:
    data = pd.read_csv(output_loc, nrows=1)
    if re.findall(r"'Ticket no.', 'Passenger Name', 'Age', 'Gender', 'Train name', 'Quota',\n       'From', 'TO', 'Ticket fare'",str(data.columns)):
        with open(output_loc, 'a') as f:
                df1.to_csv(f,header=False,index=False)
        else:
            print("replace error")
except FileNotFoundError:
    df1.to_csv(output_loc,index=False)

except:
    df1.to_csv(output_loc,index=False)