import psycopg2
from config import host, user, db_name
from cve_parser import CVE 

def getSolution(name):
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()
        with connection.cursor() as cursor:

            cursor.execute(f"SELECT solution FROM solutions WHERE LOWER(name)= LOWER('{name}');")
            solutionQuery = cursor.fetchone()
            if solutionQuery != None:
                str = ''.join(solutionQuery)
                return(f"{str}")
            else:
                return None
                            

    except Exception as _ex:
        return('[INFO] Error while working with PostgreSQL', _ex)
        #finally:
        # if connection:
        #     connection.close()
            
        #     print('[INFO] PostgreSQL connection closed')
    
def getDescription(name):
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()
        with connection.cursor() as cursor:

            cursor.execute(f"SELECT description FROM solutions WHERE LOWER(name)= LOWER('{name}');")
            solutionQuery = cursor.fetchone()
            if solutionQuery != None:
                str = ''.join(solutionQuery)
                return(f"{str}")
            else:
                return None
                            

    except Exception as _ex:
        return('[INFO] Error while working with PostgreSQL', _ex)
        
    

def getReference(name):
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()
        with connection.cursor() as cursor:

            cursor.execute(f"SELECT reference FROM solutions WHERE LOWER(name)= LOWER('{name}');")
            solutionQuery = cursor.fetchone()
            if solutionQuery != None:
                str = ''.join(solutionQuery)
                return(f"{str}")
            else:
                return None
                            

    except Exception as _ex:
        return('[INFO] Error while working with PostgreSQL', _ex)

def isExist(name):
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()
        with connection.cursor() as cursor:

            cursor.execute(f"SELECT id FROM solutions WHERE LOWER(name)= LOWER('{name}');")
            solutionQuery = cursor.fetchone()
            if solutionQuery != None:                
                return True
            else:
                return False
                            

    except Exception as _ex:
        return('[INFO] Error while working with PostgreSQL', _ex)

def doQuery(query):
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()
        with connection.cursor() as cursor:

            #cursor.execute(f"SELECT name FROM solutions WHERE cvss > 8;")
            cursor.execute(query)
            list = []
            if cursor!=None:
                for row in cursor:
                    list.append(row)
                return list
            else:
                return None
            # solutionQuery = cursor.fetchone()
            # str = ''
            # while solutionQuery!= None:
            #     str = f"{str}\n{solutionQuery}"
            #     solutionQuery = cursor.fetchone()
            # return str
        
            # if solutionQuery != None:
            #     str = ''.join(solutionQuery)
            #     return(f"{str}")
            # else:
            #     return None
                            

    except Exception as _ex:
        return(None)
    
def addCVEToDB(cve: CVE):     
    try:
        #connect to db
        connection = psycopg2.connect(host = host, user = user, database = db_name)
        cursor = connection.cursor()        
        cursor.execute(f"INSERT INTO solutions (name, description, solution, reference, cvss) VALUES ({cve.get_name}, {cve.get_description}, {cve.get_solution}, {cve.get_reference}, {cve.get_cvss})")
        connection.commit()                      

    except Exception as _ex:
        return('[INFO] Error while working with PostgreSQL', _ex)

