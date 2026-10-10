from flask import Flask,jsonify,request
from database import get_db_connection
from flask_cors import CORS
from datetime import date

app=Flask(__name__)
CORS(app)
REQUIRED_FIELDS=["ResearchTitle","ResearchDescription","ResearchArea","FacultyMemberName","Department","RequiredSkills","NumberOfAvailablePosition","ApplicationDeadline","Status"]

def validate_opportunity(data, partial=False):
        if not isinstance(data, dict):
            return "Request body must be a JSON object"

        if not partial:
            missing=[
                field for field in REQUIRED_FIELDS
                if field not in data
                or data[field] is None
                or (isinstance(data[field], str) and not data[field].strip())
            ]

            if missing:
                return "Missing or empty required fields:"+",".join(missing)
        string_fields=["ResearchTitle","ResearchDescription","ResearchArea","FacultyMemberName","Department","RequiredSkills"]
        
        for field in REQUIRED_FIELDS:
            if field not in data:
                continue
            value=data[field]
            if field in string_fields:
                if not isinstance(value,str) or not value.strip():
                    return field+" must be a non-empty string"
            elif field=="NumberOfAvailablePosition":
                if isinstance(value,bool) or not isinstance(value,int):
                    return "NumberOfAvailablePosition must be an integer"
                if value<1:
                    return "NumberOfAvailablePosition must be atleast 1"
            elif field=="ApplicationDeadline":
                if not isinstance(value,str):
                    return "ApplicationDeadline must use YYYY-MM-DD format"
                try:
                    date.fromisoformat(value)
                except ValueError:
                    return "ApplicationDeadline must be a valid date in YYYY-MM-DD format"
            elif field=="Status":
                if value not in ["Open","Closed"]:
                    return "Status must either be open or closed"
        return None
        
@app.route("/",methods=["GET"])
def home():
    return jsonify({"message":"University Research Opportunity Portal API is running"}),200
@app.route("/test-db", methods=["GET"])
def test_db():
    connection=None
    cursor=None
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute("SELECT 1")
        result=cursor.fetchone()
        
        return jsonify({"message":"Database connected successfully","result": result[0]}),200

    except Exception as error:
        app.logger.exception("Database connection test failed")
        return jsonify({"error": "Database connection failed",}),500
    
    finally:
        if cursor is not None:
            cursor.close()
        
        if connection is not None and connection.is_connected():
            connection.close()

@app.route("/api/opportunities",methods=["POST"])
def create_opportunity():
    data=request.get_json(silent=True)
    error=validate_opportunity(data)

    if error:
        return jsonify({"error": error}), 400
    
    connection=None
    cursor=None
    
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        query = """
            INSERT INTO opportunities (
                ResearchTitle,
                ResearchDescription,
                ResearchArea,
                FacultyMemberName,
                Department,
                RequiredSkills,
                NumberOfAvailablePosition,
                ApplicationDeadline,
                Status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values=tuple(data[field] for field in REQUIRED_FIELDS)
        cursor.execute(query,values)
        connection.commit()
        new_id=cursor.lastrowid
        return jsonify({
            "message":"Research Opportunity created successfully",
            "ID":new_id
        }),201
    except Exception:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Failed to create opportunity")
        return jsonify({"error":"Internal server error"}),500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            
@app.route("/api/opportunities",methods=["GET"])
def get_all_opportunities():
    connection=None
    cursor=None
    
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities ORDER BY ID")
        opportunities=cursor.fetchall()
        
        for opportunity in opportunities:
            if opportunity["ApplicationDeadline"] is not None:
                opportunity["ApplicationDeadline"]=(opportunity["ApplicationDeadline"].isoformat())
        return jsonify(opportunities),200
    
    except Exception:
        app.logger.exception("Failed to retrieve opportunities")
        return jsonify({"error":"Internal server error"}),500
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route("/api/opportunities/<int:opportunity_id>",methods=["GET"])
def get_opportunity(opportunity_id):
    connection=None
    cursor=None
    
    try:
        connection=get_db_connection()
        cursor=connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities WHERE ID=%s",(opportunity_id,))
        opportunity=cursor.fetchone() 
        
        if opportunity is None:
            return jsonify({"error":"Research opportunity not found"}),404
        if opportunity["ApplicationDeadline"] is not None:
           opportunity["ApplicationDeadline"]=(opportunity["ApplicationDeadline"].isoformat())
        return jsonify(opportunity),200
    
    except Exception:
        app.logger.exception("Failed to retrieve opportunity")
        return jsonify({"error":"Internal server error"}),500
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()         

@app.route("/api/opportunities/<int:opportunity_id>",methods=["PUT"])
def update_opportunity(opportunity_id):
    data=request.get_json(silent=True)
    
    if not isinstance(data,dict) or not data:
        return jsonify({"error":"Request body must be a non-empty JSON object"}),400
     
    unknown_fields=set(data.keys())-set(REQUIRED_FIELDS)
    if unknown_fields:
        return jsonify({"error":"Unknown fields:"+",".join(sorted(unknown_fields))}),400
    
    error=validate_opportunity(data,partial=True)
    if error:
        return jsonify({"error":error}),400
    
    connection=None
    cursor=None
    
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute("SELECT ID FROM opportunities WHERE ID=%s",(opportunity_id,))
        
        if cursor.fetchone() is None:
            return jsonify({"error":"Research opportunity not found"}),400
        
        columns=list(data.keys())
        assignments=",".join(f"{column}=%s" for column in columns)
        values=[data[column] for column in columns]
        values.append(opportunity_id)
        query=f"""
                UPDATE opportunities
                SET {assignments}
                WHERE ID=%s  
            """
        cursor.execute(query,tuple(values))
        connection.commit()
        return jsonify({
            "message":"Research opportunity updated successfully",
            "ID":opportunity_id
        }),200
        
    except Exception:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Failed to update opportunity")
        return jsonify({"error":"Internal server error"}),500
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
    
@app.route("/api/opportunities/<int:opportunity_id>",methods=["DELETE"])
def delete_opportunity(opportunity_id):
    connection=None
    cursor=None
    
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute(
            "DELETE FROM opportunities WHERE ID=%s",
            (opportunity_id,)
        )  
        
        if cursor.rowcount==0:
            return jsonify({"error":"Research opportunity not found"}),404
        connection.commit() 
        return jsonify({
            "message":"Research opportunity deleted successfully",
            "ID":opportunity_id
        }),200
    
    except Exception:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Failed to delete opportunity")
        return jsonify({"error":"Internal server error"}),500
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
               
if __name__=="__main__":
    app.run(debug=True)