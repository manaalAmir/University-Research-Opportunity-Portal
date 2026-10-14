from flask import Flask,jsonify,request
from database import get_db_connection
from flask_cors import CORS
from datetime import date

app=Flask(__name__)
CORS(app)
fields=["ResearchTitle","ResearchDescription","ResearchArea","FacultyMemberName","Department","RequiredSkills","NumberOfAvailablePosition","ApplicationDeadline","Status"]

def checkData(data):
        if not isinstance(data,dict):
            return "Request body must be a JSON object"

        for field in fields:
                if field not in data or data[field] is None or data[field]=="":
                        return field+" is missing or empty"
        
        value=data["NumberOfAvailablePosition"]
        if isinstance(value,bool) or not isinstance(value,int):
                return "NumberOfAvailablePosition must be an integer"
        if value<1:
                return "NumberOfAvailablePosition must be atleast 1"
                
        try:
                date.fromisoformat(data["ApplicationDeadline"])
        except (ValueError,TypeError):
                return "ApplicationDeadline must be a valid date in YYYY-MM-DD format"
        
        if data["Status"]!="Open" and data["Status"]!="Closed":
                return "Status must be Open or Closed"
        return None
        
@app.route("/",methods=["GET"])
def home():
    return jsonify({"message":"University Research Opportunity Portal API is running"}),200
        
@app.route("/test-db", methods=["GET"])
def testDb():
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute("SELECT 1")
        result=cursor.fetchone()
        cursor.close()
        connection.close()
        
        return jsonify({"message":"Database connected successfully","result": result[0]}),200

    except Exception as error:
        print(error)
        return jsonify({"error": "Database connection failed",}),500

@app.route("/api/opportunities",methods=["POST"])
def createOpportunity():
    data=request.get_json(silent=True)
    error=checkData(data)

    if error:
        return jsonify({"error": error}), 400
            
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        SQL=""" INSERT INTO opportunities 
                (ResearchTitle,ResearchDescription,ResearchArea,FacultyMemberName,Department,RequiredSkills,NumberOfAvailablePosition,ApplicationDeadline,Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
            
        values=[]
        for field in fields:
            values.append(data[field])
                
        cursor.execute(SQL,tuple(values))
        connection.commit()
        newID=cursor.lastrowid
        cursor.close()
        connection.close()
        return jsonify({"message":"Research Opportunity created successfully","ID":newID}),201
            
    except Exception as error:
            print(error)
            return jsonify({"error":"Internal server error"}),500
            
@app.route("/api/opportunities",methods=["GET"])
def getAllOpportunities():
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities ORDER BY ID")
        opportunities=cursor.fetchall()
        cursor.close()
        connection.close()
        
        for opportunity in opportunities:
            if opportunity["ApplicationDeadline"] is not None:
                opportunity["ApplicationDeadline"]=(opportunity["ApplicationDeadline"].isoformat())
        return jsonify(opportunities),200
    
    except Exception as error:
            print(error)
            return jsonify({"error":"Internal server error"}),500
            
@app.route("/api/opportunities/<int:opportunityID>",methods=["GET"])
def getOpportunity(opportunityID):
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities WHERE ID=%s",(opportunityID,))
        opportunity=cursor.fetchone() 
        cursor.close()
        connection.close()
        
        if opportunity is None:
            return jsonify({"error":"Research opportunity not found"}),404
        if opportunity["ApplicationDeadline"] is not None:
           opportunity["ApplicationDeadline"]=(opportunity["ApplicationDeadline"].isoformat())
        return jsonify(opportunity),200
    
    except Exception as error:
        print(error)
        return jsonify({"error":"Internal server error"}),500
            
@app.route("/api/opportunities/<int:opportunityID>",methods=["PUT"])
def updateOpportunity(opportunityID):
        data=request.get_json(silent=True)
        error=checkData(data)
        
        if error:
                return jsonify({"error": error}), 400
        
        try:
                connection=get_db_connection()
                cursor=connection.cursor()
                cursor.execute("SELECT ID FROM opportunities WHERE ID=%s",(opportunityID,))
                
                if cursor.fetchone() is None:
                        cursor.close()
                        connection.close()
                        return jsonify({"error":"Research opportunity not found"}),404
        
                SQL=""" UPDATE opportunities
                        SET ResearchTitle=%s,ResearchDescription=%s,ResearchArea=%s,FacultyMemberName=%s,Department=%s,RequiredSkills=%s,NumberOfAvailablePosition=%s,ApplicationDeadline= %s,Status=%s
                        WHERE ID=%s """

                values=[]
                for field in fields:
                        values.append(data[field])
                
                values.append(opportunityID)
                cursor.execute(SQL,tuple(values))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"message":"Research opportunity updated successfully","ID":opportunityID}),200
        
        except Exception as error:
                print(error)
                return jsonify({"error":"Internal server error"}),500

@app.route("/api/opportunities/<int:opportunityID>",methods=["DELETE"])
def deleteOpportunity(opportunityID):
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute("DELETE FROM opportunities WHERE ID=%s",(opportunityID,))  
        connection.commit()
        deleted=cursor.rowcount
        cursor.close()
        connection.close()
            
        if deleted==0:
            return jsonify({"error":"Research opportunity not found"}),404
        return jsonify({"message":"Research opportunity deleted successfully","ID":opportunityID}),200
    
    except Exception as error:
        print(error)
        return jsonify({"error":"Internal server error"}),500
               
if __name__=="__main__":
    app.run(debug=True)
