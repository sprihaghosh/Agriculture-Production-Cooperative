# -*- coding: utf-8 -*-
import pandas as pd#to create tables
pd.set_option("display.max_columns",None,"display.width", None)
import mysql.connector as sqltor
mycon=sqltor.connect(host='localhost',
                     database='mydb',
                     user='root',
                     password='wassupsql')
cursor=mycon.cursor()#python-MySQL connectivity created
while True:#system starts in the loop form
    input("Please press the Enter key to proceed")
    print("\n*******************************************************************************")
    print("\t\t BHARAT AGRICULTURAL PRODUCTION COOPERATIVE SOCIETY ")       
    print("\t\t            BELGAON, BULANDSHAHAR")
    print("\t\t                UTTAR PRADESH")
    print("\n\n\t\t  MAIN MENU")
    print("\n\t\t 1. MEMBER")
    print("\t\t 2. ADMINISTRATOR")
    print("\t\t 3. EXIT")
    print("**********************************************************************************")
    a=int(input("\n Please select an option(1 to 3): "))
    if a==1:# if 'MEMBER' chosen
        while True:
            input("Please press the Enter key to proceed")
            print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("\n\t MAIN MEMBER MENU")
            print("\n\t 1. VIEW ALLOCATED GROUPS")
            print("\n\t 2. ENTER CROP YIELD BASED ON GROUP ALLOCATED")
            print("\n\t 3. VIEW CROP YIELD PER MEMBER")
            print("\n\t 4. BACK TO MAIN MENU")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            b=int(input("Please select your option(1 to 4): "))
            if b==1:# if 'VIEW ALLOCATED GROUPS'
                print("\nMEMBER_CROP_ALLOCATION TABLE\n")
                lst3=[]
                cursor.execute("SELECT * FROM member_crop_allocation")
                r2=cursor.fetchall()
                for row in r2:
                    lst3.append(row)
                t3=pd.DataFrame(lst3, columns=['allocation_id','farmer1_id','farmer1_name',
                                               'farmer2_id','farmer2_name','crop_grown_id','crop_name',
                                               'total_area','fertilizers_amt_in_Kg','pesticide_amt_in_L','harvesting_months'])
                pd.set_option('display.width', None)
                print(t3)            
            elif b==2: #if 'ENTER CROP YIELD BASED ON GROUP ALLOCATED' is chosen                
                while True:
                    print("\n\t\tMEMBER_CROP_ALLOCATION TABLE")
                    print("\n---Enter valid allocation_id from member_allocation_table---")
                    l1=int(input("ENTER THE ALLOCATION_ID: "))
                    l2=float(input("ENTER THE CROP YIELD PER SQ. M IN KG: "))
                    l3=input("RATIO IN WHICH YIELD BE DIVIDED AMONG INDIVIDUAL MEMBERS: ")
                    #insert new row in groupwise_crop_yield table
                    q37="""
                        INSERT INTO groupwise_crop_yield(allocation_id,crop_yield_per_sqm_in_kg,dividing_ratio)
                        VALUES({},{},'{}');
                        """.format(l1,l2,l3)
                    cursor.execute(q37)
                    mycon.commit()
                    #update crop name in groupwise_crop_yield table
                    q38="""
                        UPDATE groupwise_crop_yield AS g
                        INNER JOIN member_crop_allocation AS m
                        ON g.allocation_id = m.allocation_id
                        SET g.crop_name = m.crop_name
                        WHERE g.allocation_id = %s
                        """%(l1)
                    cursor.execute(q38)
                    mycon.commit()
                        
                    q39="""
                        UPDATE groupwise_crop_yield AS g
                        INNER JOIN member_crop_allocation AS m
                        ON g.allocation_id = m.allocation_id
                        SET g.harvesting_months = m.harvesting_months
                        WHERE g.allocation_id = %s
                        """%(l1)
                    cursor.execute(q39)
                    mycon.commit()
                        
                    q40="""
                        UPDATE groupwise_crop_yield AS g
                        INNER JOIN member_crop_allocation AS m
                        ON g.allocation_id = m.allocation_id
                        SET g.total_amt_of_crop = g.crop_yield_per_sqm_in_kg * m.total_area * 4046.86
                        WHERE g.allocation_id = %s
                        """%(l1)
                    cursor.execute(q40)
                    mycon.commit()
                    # update individual yield of individual_crop_yield table
                    q47="""
                        UPDATE individual_crop_yield AS i
                        INNER JOIN groupwise_crop_yield AS g
                        ON i.allocation_id1 = g.allocation_id
                        SET i.individual_yield_in_kg = 0.5 * g.total_amt_of_crop
                        WHERE i.allocation_id1 = %s
                        """%(l1)
                    cursor.execute(q47)
                    mycon.commit()
                        
                    ans=input("DO YOU WANT TO ADD MORE?(y/n): ")
                    if ans=="y":
                        continue
                    else:
                        print("\n NEW RECORDS SUCCESSFULLY ADDED\n")
                        cursor.execute("SELECT * FROM groupwise_crop_yield;")
                        rec8=cursor.fetchall()
                        lst22=[]
                        for i in rec8:
                            lst22.append(i)
                        t22=pd.DataFrame(lst22, columns=['allocation_id','crop_name','harvesting_months',
                                                         'crop_yield_per_sqm_in_kg',
                                                         'total_amt_of_crop','dividing_ratio'])
                        print(t22)
                        break            
            elif b==3: #if 'VIEW CROP YIELD PER MEMBER' is chosen
                m1=int(input("ENTER FARMER_ID: "))
                q50="""
                    SELECT * FROM individual_crop_yield
                    WHERE farmer_id = %s;
                    """%(m1)
                cursor.execute(q50)
                rec10=cursor.fetchall()
                print("\nRECORD OF CROP YIELDS OF FARMER WITH FARMER_ID ",m1," \n")
                lst5=[]
                for row in rec10:
                    lst5.append(row)
                t5=pd.DataFrame(lst5, columns=['yield_id','farmer_id','farmer_name','allocation_id1',
                               'crop_name','individual_yield_in_kg'])
                print(t5)                    
            elif b==4:#if 'BACK TO MAIN MENU' chosen
                break
            else: # if option other than 1-4 chosen 
                print("INVALID OPTION SELECTED!")                
    elif a==2: #if'ADMINISTRATOR' chosen
        pw="123456789"
        e=str(input("Enter the password: "))
        if e==pw:#if correct password entered
            while True:
                input("Please press the Enter key to proceed")
                print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("\n\t\t Welcome Mr. Admin")
                print("\n\t MAIN ADMIN MENU")
                print("\n\t 1. MEMBER INFORMAION")
                print("\n\t 2. CROP INFORMAION ")
                print("\n\t 3. EQUIPMENTS STOCK")
                print("\n\t 4. CROP ALLOCATION")
                print("\n\t 5. BACK TO MAIN MENU")
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                f=int(input("Please select your option(1 to 5): "))
                if f==1:#if "MEMBER INFORMAION" entered
                    while True:
                        input("Please press the Enter key to proceed")
                        print("\n..............................................................")
                        print("\n\t SUBMENU")
                        print("\n\t 1. EDIT INFORMATION")
                        print("\n\t 2. ADD NEW MEMBER")
                        print("\n\t 3. REMOVE MEMBER")
                        print("\n\t 4. VIEW TABLE")
                        print("\n\t 5. BACK TO ADMIN MENU")
                        print("...............................................................")
                        g=int(input("Please select your option(1 to 5): "))                        
                        if g==1:#if "EDIT INFORMATION" entered
                            a1=input("ENTER FARMER ID OF THE RECORD TO BE UPDATED: ")
                            print("\nColumns of the 'Farmers' table:")
                            print("[farmer_id, name, land_area_owned, num_of_member, equip_id1, count1, equip_id2, count2,")
                            print("equip_id3, count3, equip_id4, count4, equip_id5, count5, equip_id6, count6]")
                            a2=input("\nCOLUMN TO BE UPDATED? ")
                            a3=input("SET NEW VALUE: ")                
                            if a2=="name": #as string value gets updated
                               q1= """
                                  update farmers
                                  set %s='%s'
                                  where farmer_id=%s
                                   """%(a2,a3,a1)
                               cursor.execute(q1)
                               mycon.commit()
                               cursor.execute("select * from farmers;")
                               rec=cursor.fetchall()
                               print("\nUPDATED TABLE\n")
                               lst6=[]
                               for i in rec:
                                  lst6.append(i)
                               t6=pd.DataFrame(lst6, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                        'equip_id1','count1','equip_id2','count2','equip_id3',
                                                'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                               print(t6)                              
                            else:
                                q3= """
                                  update farmers
                                  set %s=%s
                                  where farmer_id=%s
                                   """%(a2,a3,a1)
                                cursor.execute(q3)
                                mycon.commit()
                                cursor.execute("select * from farmers;")
                                rec=cursor.fetchall()
                                print("\nUPDATED TABLE\n")
                                lst7=[]
                                for i in rec:
                                   lst7.append(i)
                                t7=pd.DataFrame(lst7, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                            'equip_id1','count1','equip_id2','count2','equip_id3',
                                                'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                                print(t7)                                
                        elif g==2:#if "ADD NEW MEMBER" is entered
                            b1=input("ENTER NEW MEMBER ID: ")
                            b2=input("ENTER NAME: ")
                            b3=input("ENTER AREA OF LAND OWNED IN ACRES: ")
                            b4=input("ENTER NUMBER OF WORKING MEMBERS: ")
                            b5=input("ENTER NUMBER OF PLOUGHS OWNED: ")
                            b6=input("ENTER NUMBER OF SICKLES OWNED: ")
                            b7=input("ENTER NUMBER OF RAKES OWNED: ")
                            b8=input("ENTER NUMBER OF TRACTORS OWNED: ")
                            b9=input("ENTER NUMBER OF HARVESTORS OWNED: ")
                            b10=input("ENTER NUMBER OF SPRINKLERS OWNED: ")
                            q5= """
                               insert into farmers
                               values({},'{}',{},{},1,{},2,{},3,{},4,{},5,{},6,{});
                               """.format(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10)
                            cursor.execute(q5)
                            mycon.commit()
                            cursor.execute("select * from farmers;")
                            rec2=cursor.fetchall()
                            print("\n FARMERS TABLE\n")
                            lst8=[]
                            for i in rec2:
                                lst8.append(i)
                            t8=pd.DataFrame(lst8, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                            'equip_id1','count1','equip_id2','count2','equip_id3',
                                                           'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                            print(t8)                                
                        elif g==3:#if "REMOVE MEMBER" is entered
                            print("\n[farmer_id,name]-- [1,Mohit], [2,Pankaj], [3,Anmol], [4,Adwit], [5,Ramesh]")
                            print("                   [6,Vipul], [7,Uday], [8,Akul], [9,Anish], [10,Sameer ]")
                            c1=int(input("ENTER THE FARMER ID OF RECORD TO BE REMOVED: "))
                            q7="""
                               delete from farmers
                               where farmer_id=%s;
                               """%(c1)
                            cursor.execute(q7)
                            mycon.commit()
                            cursor.execute("select * from farmers;")
                            rec3=cursor.fetchall()
                            print("\n FARMERS TABLE\n")
                            lst9=[]
                            for i in rec3:
                                lst9.append(i)
                            t9=pd.DataFrame(lst9, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                            'equip_id1','count1','equip_id2','count2','equip_id3',
                                                           'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                            print(t9)                            
                        elif g==4:#if"VIEW TABLE" is entered
                            cursor.execute("select * from farmers;")
                            rec4=cursor.fetchall()
                            lst10=[]
                            for i in rec4:
                                 lst10.append(i)
                            t10=pd.DataFrame(lst10, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                            'equip_id1','count1','equip_id2','count2','equip_id3',
                                                           'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                            print(t10)                                 
                        elif g==5:#if "BACK TO ADMIN MENU" is entered
                            break                        
                        else:#if any other option other than 1-5 is entered
                            print("INVALID OPTION SELECTED!")                        
                elif f==2:#if "CROP INFORMAION" is entered
                    while True:
                        input("Please press the Enter key to proceed")
                        print("\n.......................................................")
                        print("\n\t SUBMENU")
                        print("\n\t 1. EDIT ")
                        print("\n\t 2. ADD CROP")
                        print("\n\t 3. DELETE CROP INFO")
                        print("\n\t 4. VIEW TABLE")
                        print("\n\t 5. BACK TO ADMIN MENU")
                        print("........................................................")
                        h=int(input("Please select your option(1 to 5): "))                        
                        if h==1:#if "EDIT" is entered
                            d1=int(input("ENTER CROP ID OF THE RECORD TO BE UPDATED: "))
                            print("\nColumns of the 'crops' table:")
                            print("[cropid, cropname, harvesting_time_in_months, pesticides_mL_per_sqm,")
                            print("fertilizers_kg_per_sqm, water_L_per_sqm, pesticide_type, fertilizer_type]")
                            d2=input("COLUMN TO BE UPDATED? ")
                            d3=input("SET NEW VALUE: ")
                
                            if d2=="cropname" or "fertilizer_type" or "pesticide_type":#if string value is to be updated
                               q10= """
                                  update crops
                                  set %s='%s'
                                  where cropid=%s
                                   """%(d2,d3,d1)
                               cursor.execute(q10)
                               mycon.commit()
                               cursor.execute("select * from crops;")
                               rec=cursor.fetchall()
                               print("\nUPDATED TABLE\n")
                               lst11=[]
                               for i in rec:
                                  lst11.append(i)
                               t11=pd.DataFrame(lst11, columns=['cropid','cropname','harvesting_time_in_months',
                                                  'pesticides_mL_per_sqm','fertilizers_kg_per_sqm','water_L_per_sqm',
                                                   'pesticide_type','fertilizer_type'])
                               print(t11)                                
                            else:
                                q12= """
                                  update crops
                                  set %s=%s
                                  where cropid=%s
                                   """%(d2,d3,d1)
                                cursor.execute(q12)
                                mycon.commit()
                                cursor.execute("select * from crops;")
                                rec=cursor.fetchall()
                                print("\nUPDATED TABLE\n")
                                lst12=[]
                                for i in rec:
                                   lst12.append(i)
                                t12=pd.DataFrame(lst12, columns=['cropid','cropname','harvesting_time_in_months',
                                                  'pesticides_mL_per_sqm','fertilizers_kg_per_sqm','water_L_per_sqm',
                                                   'pesticide_type','fertilizer_type'])
                                print(t12)                                      
                        elif h==2:#if "ADD CROP" is entered
                            e1=input("ENTER NEW CROP ID: ")
                            e2=input("ENTER CROP NAME: ")
                            e3=input("ENTER TIME NEEDED FOR HARVESTING: ")
                            e4=input("ENTER PESTICIDES (ML/SQ. M) REQUIRED: ")
                            e5=input("ENTER FERTILIZERS (KG/SQ. M) REQUIRED: ")
                            e6=input("ENTER WATER (L/ SQ. M) REQUIRED: ")
                            e7=input("ENTER PESTICIDE TYPE: ")
                            e8=input("ENTER FERTILIZER TYPE: ")
                            q14= """
                               insert into crops
                               values({},'{}',{},{},{},{},'{}','{}');
                               """.format(e1,e2,e3,e4,e5,e6,e7,e8)
                            cursor.execute(q14)
                            mycon.commit()
                            cursor.execute("select * from crops;")
                            rec2=cursor.fetchall()
                            print("\nCROP TABLE\n")
                            lst13=[]
                            for i in rec2:
                                lst13.append(i)
                            t13=pd.DataFrame(lst13, columns=['cropid','cropname','harvesting_time_in_months',
                                                  'pesticides_mL_per_sqm','fertilizers_kg_per_sqm','water_L_per_sqm',
                                                   'pesticide_type','fertilizer_type'])
                            print(t13)                                  
                        elif h==3:#if "DELETE CROP INFO" is entered
                            print("\n[cropid, name]-- [1,paddy], [2,wheat], [3,sunflower], [4,mustard], [5,potato]")
                            f1=int(input("ENTER THE CROP ID OF RECORD TO BE REMOVED: "))
                            q16="""
                               delete from crops
                               where cropid=%s;
                               """%(f1)
                            cursor.execute(q16)
                            mycon.commit()
                            cursor.execute("select * from crops;")
                            rec3=cursor.fetchall()
                            print("\nCROP TABLE\n")
                            lst14=[]
                            for i in rec3:
                                lst14.append(i)
                            t14=pd.DataFrame(lst14, columns=['cropid','cropname','harvesting_time_in_months',
                                                  'pesticides_mL_per_sqm','fertilizers_kg_per_sqm','water_L_per_sqm',
                                                   'pesticide_type','fertilizer_type'])
                            print(t14)                              
                        elif h==4:#i "VIEW TABLE" is entered
                            cursor.execute("select * from crops;")
                            rec4=cursor.fetchall()
                            print("\nCROP TABLE\n")
                            lst15=[]
                            for i in rec4:
                                 lst15.append(i)
                            t15=pd.DataFrame(lst15, columns=['cropid','cropname','harvesting_time_in_months',
                                                  'pesticides_mL_per_sqm','fertilizers_kg_per_sqm','water_L_per_sqm',
                                                   'pesticide_type','fertilizer_type'])
                            print(t15)                                   
                        elif h==5:#if "BACK TO ADMIN MENU" is entered
                            break                        
                        else:#if any other option other than 1-5 is entered
                            print("INVALID OPTION SELECTED!")                        
                elif f==3:#if "EQUIPMENTS STOCK" is entered
                    while True:
                        input("Please press the Enter key to proceed")
                        print("\n.............................................................")
                        print("\n\t SUBMENU")
                        print("\n\t 1. EDIT ")
                        print("\n\t 2. ADD NEW EQUIPMENT")
                        print("\n\t 3. DELETE EQUIPMENT(S)")
                        print("\n\t 4. VIEW EQUIPMENTS STOCK")
                        print("\n\t 5. BACK TO ADMIN MENU")
                        print("..............................................................")
                        j=int(input("Please select your option(1 to 5): "))                        
                        if j==1:#if "EDIT" is entered
                            g1=input("ENTER EQUIPMENT ID OF THE RECORD TO BE UPDATED: ")
                            print("\nColumns of 'tools_machinery' table:")
                            print("[equip_id, name, count, last_service_date, cost_per_item, maintenance_cost_per_item]")
                            g2=input("COLUMN TO BE UPDATED? ")
                            g3=input("SET NEW VALUE: ")                
                            if g2=="name":#if string value is to be updated
                               q19= """
                                  update tools_machinery
                                  set %s='%s'
                                  where equip_id=%s
                                   """%(g2,g3,g1)
                               cursor.execute(q19)
                               mycon.commit()
                               cursor.execute("select * from tools_machinery;")
                               rec=cursor.fetchall()
                               print("\nUPDATED TABLE\n")
                               lst16=[]
                               for i in rec:
                                  lst16.append(i)
                               t16=pd.DataFrame(lst16, columns=['equip_id','name','count','last_service_date',
                                                              'cost_per_item','maintenance_cost_per_item'])
                               print(t16)                              
                            else:
                                q21= """
                                  update tools_machinery
                                  set %s=%s
                                  where equip_id=%s
                                   """%(g2,g3,g1)
                                cursor.execute(q21)
                                mycon.commit()
                                cursor.execute("select * from tools_machinery;")
                                rec=cursor.fetchall()
                                print("\nUPDATED TABLE\n")
                                lst17=[]
                                for i in rec:
                                   lst17.append(i)
                                t17=pd.DataFrame(lst17, columns=['equip_id','name','count','last_service_date',
                                                              'cost_per_item','maintenance_cost_per_item'])
                                print(t17)                        
                        elif j==2:#if "ADD NEW EQUIPMENT" is entered
                            h1=int(input("ENTER NEW EQUIPMENT ID: "))
                            h2=input("ENTER NAME OF EQUIPMENT: ")
                            h3=input("ENTER TOTAL NUMBER AVAILABLE: ")
                            h4=input("ENTER THE LAST SERVICE DATE: ")
                            h5=input("ENTER THE COST PER EQUIPMENT: ")
                            h6=input("ENTER MAINTENANCE COST PER EQUIPMENT: ")
                            q23= """
                               insert into tools_machinery
                               values({},'{}',{},'{}',{},{});
                               """.format(h1,h2,h3,h4,h5,h6)
                            cursor.execute(q23)
                            mycon.commit()
                            cursor.execute("select * from tools_machinery;")
                            rec=cursor.fetchall()
                            lst18=[]
                            print("\nTOOLS_MACHINERY TABLE\n")
                            for i in rec:
                                lst18.append(i)
                            t18=pd.DataFrame(lst18, columns=['equip_id','name','count','last_service_date',
                                                              'cost_per_item','maintenance_cost_per_item'])
                            print(t18)                                
                        elif j==3:#if "DELETE EQUIPMENT(S)" is entered
                            print("\n[equip_id,name]-- [1,plough], [2,sickle], [3,rake], [4,tractor], [5,harvestor], [6,sprinkler]")
                            h1=int(input("ENTER THE EQUIPMENT ID OF RECORD TO BE REMOVED: "))
                            q25="""
                               delete from tools_machinery
                               where equip_id=%s;
                               """%(h1)
                            cursor.execute(q25)
                            mycon.commit()
                            cursor.execute("select * from tools_machinery;")
                            rec3=cursor.fetchall()
                            lst19=[]
                            print("\nTOOLS_MACHINERY TABLE\n")
                            for i in rec3:
                                lst19.append(i)
                            t19=pd.DataFrame(lst19, columns=['equip_id','name','count','last_service_date',
                                                              'cost_per_item','maintenance_cost_per_item'])
                            print(t19)                            
                        elif j==4:#if "VIEW EQUIPMENTS STOCK" is entered
                            cursor.execute("select * from tools_machinery;")
                            rec4=cursor.fetchall()
                            lst20=[]
                            print("\nTOOLS_MACHINERY TABLE\n")
                            for i in rec4:
                                lst20.append(i)
                            t20=pd.DataFrame(lst20, columns=['equip_id','name','count','last_service_date',
                                                              'cost_per_item','maintenance_cost_per_item'])
                            print(t20)                                 
                        elif j==5:#if "BACK TO ADMIN MENU" is entered
                            break                        
                        else:#if any other option other than 1-5 is entered
                            print("\n INVALID OPTION SELECTED!")                              
                elif f==4:
                     print("\n\t CROP-MEMBER ALLOCATION")
                     print("\n MEMBERS WITH MORE THAN 4 ACRES OF LAND\n")
                     q28="""
                         select * from farmers
                         where land_area_owned > 4;
                         """
                     cursor.execute(q28)
                     rec5=cursor.fetchall()
                     lst21=[]
                     for i in rec5:
                         lst21.append(i)
                     t21=pd.DataFrame(lst21, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                      'equip_id1','count1','equip_id2','count2','equip_id3',
                                                      'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                     print(t21)
                     print("\n MEMBERS WITH MORE THAN 4 WORKERS\n")
                     q29="""
                         select * from farmers
                         where num_of_member > 4;
                         """
                     cursor.execute(q29)
                     rec6=cursor.fetchall()
                     lst23=[]
                     for i in rec6:
                        lst23.append(i)
                     t23=pd.DataFrame(lst23, columns=['farmer_id','name','land_area_owned','num_of_member',
                                                      'equip_id1','count1','equip_id2','count2','equip_id3',
                                                      'count3','equip_id4','count4','equip_id5','count5','equip_id6','count6'])
                     print(t23)                        
                     while True:
                         print("\n CREATE MEMBER_CROP_ALLOCATION TABLE")
                         k1=int(input("ENTER NEW ALLOCATION_ID TO INSERT: "))
                         k2=int(input("ENTER FARMER_ID OF FIRST FARMER: "))
                         k3=int(input("ENTER FARMER_ID OF SECOND FARMER: "))
                         print("\n[cropid, name]-- [1,paddy], [2,wheat], [3,sunflower], [4,mustard], [5,potato]")
                         k4=int(input("ENTER CROP_ID OF THE CROP ALLOTTED: "))
                         k5=input("ENTER THE HARVESTING MONTHS: ")
                         # insert new row in member_crop_allocation table
                         q31="""
                             insert into member_crop_allocation(allocation_id,farmer1_id,farmer2_id,crop_grown_id,harvesting_months)
                             values({},{},{},{},'{}');
                             """.format(k1,k2,k3,k4,k5)
                         cursor.execute(q31)
                         mycon.commit()
                         # insert new row in individual_crop_yield table
                         q42="""
                             INSERT INTO individual_crop_yield(allocation_id1,farmer_id)
                             VALUES({},{});
                             """.format(k1,k2)
                         cursor.execute(q42)
                         mycon.commit()
                         # insert new row in individual_crop_yield table
                         q43="""
                             INSERT INTO individual_crop_yield(allocation_id1,farmer_id)
                             VALUES({},{});
                             """.format(k1,k3)
                         cursor.execute(q43)
                         mycon.commit()
                         # update farmer name 1 in member_crop_allocation
                         q32="""
                             UPDATE member_crop_allocation
                             INNER JOIN farmers 
                             ON member_crop_allocation.farmer1_id = farmers.farmer_id
                             SET member_crop_allocation.farmer1_name = farmers.name
                             WHERE member_crop_allocation.allocation_id = %s
                             """%(k1)
                         cursor.execute(q32)
                         mycon.commit()
                         # update farmer name 2 in member_crop_allocation
                         q33="""
                             UPDATE member_crop_allocation
                             INNER JOIN farmers 
                             ON member_crop_allocation.farmer2_id = farmers.farmer_id
                             SET member_crop_allocation.farmer2_name = farmers.name
                             WHERE member_crop_allocation.allocation_id = %s
                             """%(k1) 
                         cursor.execute(q33)
                         mycon.commit()
                         #update farmer name in individual_crop_yield table
                         q45="""
                             UPDATE individual_crop_yield AS i
                             INNER JOIN farmers AS f
                             ON i.farmer_id = f.farmer_id
                             SET i.farmer_name = f.name
                             WHERE i.farmer_id = %s
                             """%(k2)
                         cursor.execute(q45)
                         mycon.commit()
                         #update another farmer name in individual_crop_yield table
                         q46="""
                             UPDATE individual_crop_yield AS i
                             INNER JOIN farmers AS f
                             ON i.farmer_id = f.farmer_id
                             SET i.farmer_name = f.name
                             WHERE i.farmer_id = %s
                             """%(k3)
                         cursor.execute(q46)
                         mycon.commit()
                         # update crop name in member_crop_allocation table
                         q34="""
                             UPDATE member_crop_allocation
                             INNER JOIN crops 
                             ON member_crop_allocation.crop_grown_id = crops.cropid
                             SET member_crop_allocation.crop_name = crops.cropname
                             WHERE member_crop_allocation.allocation_id = %s
                             """%(k1)
                         cursor.execute(q34)
                         mycon.commit()
                         #add crop name to individual_crop_yield table
                         q44="""
                            UPDATE individual_crop_yield AS i
                            INNER JOIN member_crop_allocation AS m
                            ON i.allocation_id1 = m.allocation_id
                            SET i.crop_name = m.crop_name
                            WHERE i.allocation_id1 = %s
                            """%(k1)
                         cursor.execute(q44)
                         mycon.commit()
                         #add the total area in member_crop_allocation table
                         q35="""
                              UPDATE member_crop_allocation AS m
                             INNER JOIN farmers AS f
                             ON m.farmer1_id = f.farmer_id
                             SET m.total_area = f.land_area_owned
                             WHERE m.allocation_id = %s
                             """%(k1)
                         cursor.execute(q35)
                         mycon.commit()
                         #add the total area in member_crop_allocation table
                         q38="""
                              UPDATE member_crop_allocation AS m
                             INNER JOIN farmers AS f
                             ON m.farmer2_id = f.farmer_id
                             SET m.total_area = m.total_area + f.land_area_owned
                             WHERE m.allocation_id = %s
                             """%(k1)
                         cursor.execute(q38)
                         mycon.commit()
                         #enter the fertilizer amount in member_crop_allocation table
                         q36="""
                             UPDATE member_crop_allocation AS m
                             INNER JOIN crops AS c 
                             
                             ON m.crop_grown_id = c.cropid
                             SET m.fertilizers_amt_in_Kg = m.total_area *  0.01
                             WHERE m.allocation_id = %s
                             """%(k1)
                         cursor.execute(q36)
                         mycon.commit()
                         #enter the pesticide amount in member_crop_allocation table
                         q37="""
                             UPDATE member_crop_allocation AS m
                             INNER JOIN crops AS c
                             ON m.crop_grown_id = c.cropid
                             SET m.pesticide_amt_in_L = m.total_area * 10 * 0.001
                             WHERE m.allocation_id = %s
                             """%(k1)
                         cursor.execute(q37)
                         mycon.commit()                         
                         ans=input("DO YOU WANT TO ADD MORE?(y/n): ")
                         if ans=="y":
                             continue
                         else:
                             print("\n NEW RECORDS SUCCESSFULLY ADDED\n")
                             cursor.execute("SELECT * FROM member_crop_allocation;")
                             rec7=cursor.fetchall()
                             print("\nMEMBER_CROP_ALLOCATION TABLE\n")
                             lst24=[]
                             for i in rec7:
                                 lst24.append(i)
                             t24=pd.DataFrame(lst24, columns=['allocation_id','farmer1_id','farmer1_name',
                                                            'farmer2_id','farmer2_name','crop_grown_id','crop_name',
                                                            'total_area','fertilizers_amt_in_Kg','pesticide_amt_in_L','harvesting_months'])
                             print(t24)
                             break
                elif f==5:#if "BACK TO MAIN MENU" is entered
                    break                
                else:#if any other option except 1-5 is entered
                    print("\n INVALID OPTION SELECTED!")
        else: #if wrong password is entered 
            print("\n WRONG PASSWORD!")            
    elif a==3:#if "EXIT" is selected
        print("\n-----------------------------------SYSTEM CLOSED---------------------------------") 
        break    
    else:#if any other option except 1-3 is entered
        print("\n INVALID OPTION SELECTED!")
mycon.close()#python-MySQL connectivity is closed
