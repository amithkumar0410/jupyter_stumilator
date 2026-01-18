import json
import pandas as pd
import os
class op:
    def __init__(self):
       
        self.data={}
    def save_data(self,inputs,outputs,name,user):
        df=pd.DataFrame(columns=["inputs","outputs"])

        df["inputs"]=inputs
        df["outputs"]=outputs
        name=name.replace('"','')     
        path="user\\"+user+"\\"+name+".csv"       
        df.to_csv(path)
        
    def open(self,data2,username):
        print(os.getcwd())
        name=data2+".csv"
        file=f"user\\"+username+"\\"+name
        print(file)
        df=pd.read_csv(file)
        inp=list(df["inputs"])
        out=list(df["outputs"])
        return inp,out

if __name__=="__main__":
    obj=op()
    obj.open("data")
        
        
        



            
