from operator import contains
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from werkzeug.exceptions import HTTPException
from flask import make_response
from datetime import date
from application.models import Users, List, Card
from .models import db

#***************ERRORS***********************************************************************************************
class UserNotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('User not found.', status_code)
class InternalServerError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('Internal Server Error.', status_code)      
class ValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_mssg):
        message={"error_code":error_code,"error_msg":error_mssg}
        self.response=make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})


class NoListError(HTTPException):
    def __init__(self, status_code):
       # message={"error_code":error_code,"error_msg":error_mssg}
        self.response=make_response('User has no lists.', status_code)
class ListNotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('No list was found.', status_code)
class InvalidListError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('Invalid List.', status_code)

class CardNotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('Card not found.', status_code)
class NoCardsError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('No card in the list.', status_code)
class MovementNotAllowedError(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('Card movement to the requested list id is not allowed.', status_code)

class Success(HTTPException):
    def __init__(self, status_code):
        self.response=make_response('Successfully deleted', status_code)  
#****************MARSHALS***************************************************************************************

user_output={
    "id_":fields.Integer,
    "name":fields.String,
    "email":fields.String,
    #"lists":fields.
}
list_output={
    "l_id":fields.Integer,
    "user_id":fields.Integer,
    "l_name":fields.String,
    "dsp":fields.String
}

card_output={
    "c_id":fields.Integer,
    "c_name":fields.String,
    "cont":fields.String,
    "comp":fields.String,
    "deadline":fields.String,
    "list_id":fields.Integer,
}
#*********************************************************************************************************
create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')


create_list_parser=reqparse.RequestParser()
create_list_parser.add_argument('l_name')
create_list_parser.add_argument('dsp')


create_card_parser=reqparse.RequestParser()
create_card_parser.add_argument('c_name')
create_card_parser.add_argument('cont')
create_card_parser.add_argument('comp')
create_card_parser.add_argument('list_id')
create_card_parser.add_argument('deadline')

#**********************USER API**********************************************************
class Userapi(Resource):
    @marshal_with(user_output)
    def get(self, name,email,passw):
       
        
           
            if "@" not in email or "." not in email:
                raise ValidationError(status_code=400,error_code="U04", error_mssg="Invalid email")

            if len(passw)<6:
                raise ValidationError(status_code=400,error_code="U05", error_mssg="Invalid password, minimum 6 character password required.")     

            found_usr=Users.query.filter_by(name=name, email=email, passw=passw).first()
            if found_usr:
                return found_usr, 200
            else:
                raise UserNotFoundError( status_code=404)
        


    @marshal_with(user_output)
    def post(self):
        
            args=create_user_parser.parse_args()
            user_name=args.get('user_name', None)
            email=args.get('email', None)
            password=args.get('password', None)
        
            if user_name is None or len(user_name)<1 or len(user_name)>25:
                raise ValidationError(status_code=400,error_code="U01", error_mssg="Invalid User name")
            if user_name[0]==" ":
                raise ValidationError(status_code=400,error_code="U01", error_mssg="Invalid User name")
            if email is None or len(email)<1 or len(email)>25:
                raise ValidationError(status_code=400,error_code="U02", error_mssg="email id is required")

            if password is None:
                raise ValidationError(status_code=400,error_code="U03", error_mssg="Password required")    

            if "@" not in email or "." not in email:
                raise ValidationError(status_code=400,error_code="U04", error_mssg="Invalid email")
            if " " in email:
                raise ValidationError(status_code=400,error_code="U04", error_mssg="Invalid email")
            if len(password)<6 or len(password)>25:
                raise ValidationError(status_code=400,error_code="U05", error_mssg="Invalid password, minimum 6 character password required.") 
            if " " in password:
                raise ValidationError(status_code=400,error_code="U05", error_mssg="Invalid password, minimum 6 character password required.") 
            f=Users.query.filter_by(email=email).first()
            if f:
                raise ValidationError(status_code=409,error_code="E01", error_mssg="email id is not unique")

            u=Users(name=user_name,email=email,passw=password)    
            db.session.add(u)
            db.session.commit()
        
            us=Users.query.filter_by(name=user_name,email=email,passw=password).first()
        
            return us, 201
        

#*******************************LIST API*****************************************************************
class Listapi(Resource):
    def get(self,u_id):
       

            found_usr=Users.query.filter_by(id_=u_id).first()
            found_li=List.query.filter_by(user_id=u_id).all()
        
            if found_usr:
                if found_li:
                    lists=[]
                    for i in found_li:
                        l={
                            "l_id":i.l_id,
                            "user_id":i.user_id,
                            "l_name":i.l_name,
                            "dsp":i.dsp
                        }
                        lists.append(l)
                    return lists, 200
                else:
                    raise NoListError(status_code=404)    
            else:
                raise UserNotFoundError(status_code=404)
             

    def post(self,u_id):
        
            args=create_list_parser.parse_args()
            l_name=args.get('l_name', None)
            dsp=args.get('dsp', None)

    

            if l_name is None or len(l_name)<1 or len(l_name)>20:
                raise ValidationError(status_code=400,error_code="U013", error_mssg="Invalid List name.")
            if l_name[0]==" ":
                raise ValidationError(status_code=400,error_code="U013", error_mssg="Invalid List name.") 
            if len(dsp)>45:
                raise ValidationError(status_code=400,error_code="U014", error_mssg="Invalid description.")       
            u=Users.query.filter_by(id_=u_id).first()
            if u:
                li=List(user_id=u_id,l_name=l_name,dsp=dsp)

                db.session.add(li)
                db.session.commit()

                found_usr=Users.query.filter_by(id_=u_id).first()
                lis=List.query.filter_by(user_id=u_id).all()
            
                if found_usr:
                    if lis:
                        l=[]
                        for i in lis:
                            list1={
                                "l_id":i.l_id,
                                "user_id":u_id,
                                "l_name":i.l_name,
                                "dsp":i.dsp
                            }
                            l.append(list1)
                        return l, 201
                    else:
                        raise NoListError(status_code=404)
                else:
                    raise UserNotFoundError(status_code=404)     
            else:
                raise UserNotFoundError(status_code=404)                                     
            

    def delete(self,u_id,l_id):
       

            u=Users.query.filter_by(id_=u_id).first()
            l=List.query.filter_by(l_id=l_id,user_id=u_id).first()
            if u:
                if l:
                    db.session.delete(l)
                    db.session.commit()
                    raise Success(status_code=200)
                    

                else:
                    raise InvalidListError(status_code=404)
            else:
                raise UserNotFoundError(status_code=404)
        


    @marshal_with(list_output)
    def put(self,u_id,l_id):
        
            args=create_list_parser.parse_args()
            l_name=args.get('l_name', None)
            dsp=args.get('dsp', None)

            
            if l_name is None or len(l_name)<1 or len(l_name)>20:
                raise ValidationError(status_code=400,error_code="U013", error_mssg="Invalid List name.")
            if l_name[0]==" ":
                raise ValidationError(status_code=400,error_code="U013", error_mssg="Invalid List name.")
            if len(dsp)>45:
                raise ValidationError(status_code=400,error_code="U014", error_mssg="Invalid description.")       
            u=Users.query.filter_by(id_=u_id).first()
            li=List.query.filter_by(l_id=l_id,user_id=u_id).first()
            if u:
                if li:
                    li.l_name=l_name
                    li.dsp=dsp
                
                    db.session.commit()
                    l=List.query.filter_by(l_id=l_id,user_id=u_id).first()
                    return l, 200
                else:
                    raise InvalidListError(status_code=404)           
                     
            else:
                raise UserNotFoundError(status_code=404)                                     
          

#*******************************CARD API********************************************************************
class Cardapi(Resource):
    def get(self,user_id, list_id):
       

            found_usr=Users.query.filter_by(id_=user_id).first()
            found_li=List.query.filter_by(l_id=list_id,user_id=user_id).first()
            found_cr=Card.query.filter_by(list_id=list_id).all()

        
            if found_usr:
                if found_li:
                    if found_cr:
                        cards=[]
                        for i in found_cr:
                            td=str(date.today())
                            if i.comp=="comp":
                                if i.deadline>=td:
                                    status="completed"
                                else:
                                    status="successfully submitted "
                            else:
                                if i.deadline<td:
                                    status="failed to submit"
                                if i.deadline>td:
                                    status="pending"
                                if i.deadline==td:
                                    status="the deadline is today"
                            c={
                                "card_id":i.c_id,
                                "card_name":i.c_name,
                                "content":i.cont,
                                "status":status,
                                "deadline":i.deadline,
                                "list_id":i.list_id
                            }
                            cards.append(c)
                        return cards, 200
                    else:
                        raise NoCardsError(status_code=404)    
                else:
                    raise InvalidListError(status_code=404)    
            else:
                raise UserNotFoundError(status_code=404)
   


    def post(self,user_id,list_id):
        
            args=create_card_parser.parse_args()
            c_name=args.get('c_name', None)
            content=args.get('cont', None)
            completed=args.get('comp', None)
            deadline=args.get('deadline', None)
            
            
            if c_name is None or len(c_name)<1 or len(c_name)>20:
                raise ValidationError(status_code=400,error_code="U08", error_mssg="Invalid Card name.")
            if len(content)>50:
                raise ValidationError(status_code=400,error_code="U015", error_mssg="Invalid content.")
            if c_name[0]==" ":
                raise ValidationError(status_code=400,error_code="U08", error_mssg="Invalid Card name.")        
            if completed is not None :
                if completed!="comp":
                    raise ValidationError(status_code=400,error_code="U018", error_mssg="either put 'comp' or null as values.")    
            if deadline is None or len(deadline)!=10 or deadline[4]!="-" or deadline[7]!="-":
                raise ValidationError(status_code=400,error_code="U019", error_mssg="Invalid date format.")
            try:
                if not int(deadline[0:4]) or not int(deadline[5:7]) or not int(deadline[8:10]):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")
                if 12<int(deadline[5:7]) or 0>int(deadline[5:7]):
                    raise ValidationError(status_code=400,error_code="U010", error_mssg="Invalid month values.")
                t=["01","03","05","07","08","10","12"]    
                t1=["04","06","09","11"]
                if (deadline[5:7]) in t and (int(deadline[8:10])>31 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.") 

                if (deadline[5:7]) in t1 and (int(deadline[8:10])>30 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")

                if (deadline[5:7])=="02"and int(deadline[0:4])%4!=0 and (int(deadline[8:10])>28 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")
                if (deadline[5:7])=="02"and int(deadline[0:4])%4==0  and (int(deadline[8:10])>29 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")           
                if deadline<str(date.today()):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")                  
            except ValueError:
                raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")   
            u=Users.query.filter_by(id_=user_id).first()
            
            li=List.query.filter_by(l_id=list_id,user_id=user_id).first()

            if u:
                if li:
                    c=Card(c_name=c_name,cont=content,comp=completed,deadline=deadline,list_id=list_id)          
            

                    db.session.add(c)
                    db.session.commit()

                    found_usr=Users.query.filter_by(id_=user_id).first()
                    lis=List.query.filter_by(l_id=list_id,user_id=user_id).first()
                    car=Card.query.filter_by(list_id=list_id).all()
                    if found_usr:
                        if lis:
                            if car:
                                ca=[]
                                for i in car:
                                    car1={
                                        "card_id":i.c_id,
                                        "card_name":i.c_name,
                                        "content":i.cont,
                                        "completed":i.comp,
                                        "deadline":i.deadline,
                                        "list_id":list_id
                                    }
                                    ca.append(car1)
                                return ca, 201
                            else:
                                raise NoCardsError(status_code=404)    
                        else:
                            raise NoListError(status_code=404)
                    else:
                        raise UserNotFoundError(status_code=404)   
                else:
                    raise InvalidListError(status_code=404)          
            else:
                raise UserNotFoundError(status_code=404)                                     
                         

    def delete(self,user_id,list_id,card_id):
        


            u=Users.query.filter_by(id_=user_id).first()
            l=List.query.filter_by(l_id=list_id,user_id=user_id).first()
            c=Card.query.filter_by(c_id=card_id,list_id=list_id).first()
            if u:
                if l:
                    
                    if c:
                        db.session.delete(c)
                        db.session.commit()
                        raise Success(status_code=200)
                    else:
                        raise CardNotFoundError(status_code=404)

                else:
                    raise InvalidListError(status_code=404)
            else:
                raise UserNotFoundError(status_code=404)
        


    @marshal_with(card_output)
    def put(self,user_id,list_id,card_id):
        
            args=create_card_parser.parse_args()
            c_name=args.get('c_name', None)
            content=args.get('cont', None)
            completed=args.get('comp', None)
            deadline=args.get('deadline', None)
            lis_id=args.get('list_id', None)


            if c_name is None or len(c_name)<1 or len(c_name)>20:
                raise ValidationError(status_code=400,error_code="U08", error_mssg="Invalid Card name.")
            if c_name[0]==" ":
                raise ValidationError(status_code=400,error_code="U08", error_mssg="Invalid Card name.") 
            if len(content)>50:
                raise ValidationError(status_code=400,error_code="U015", error_mssg="Invalid content.")   
            if completed is not None :
                if completed!="comp":
                    raise ValidationError(status_code=400,error_code="U018", error_mssg="either put 'comp' or null as values.")    
            if deadline is None or len(deadline)!=10 or deadline[4]!="-" or deadline[7]!="-":
                raise ValidationError(status_code=400,error_code="U019", error_mssg="Invalid date format.")
            try:
                if not int(deadline[0:4]) or not int(deadline[5:7]) or not int(deadline[8:10]):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")
                if 12<int(deadline[5:7]) or 0>int(deadline[5:7]):
                    raise ValidationError(status_code=400,error_code="U010", error_mssg="Invalid month values.")
                t=["01","03","05","07","08","10","12"]    
                t1=["04","06","09","11"]
                if (deadline[5:7]) in t and (int(deadline[8:10])>31 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.") 

                if (deadline[5:7]) in t1 and (int(deadline[8:10])>30 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")

                if (deadline[5:7])=="02"and int(deadline[0:4])%4!=0 and (int(deadline[8:10])>28 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")
                if (deadline[5:7])=="02"and int(deadline[0:4])%4==0  and (int(deadline[8:10])>29 or int(deadline[8:10])<0):
                    raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")              
            except ValueError:
                raise ValidationError(status_code=400,error_code="U09", error_mssg="Invalid date.")  


            u=Users.query.filter_by(id_=user_id).first()           
            li=List.query.filter_by(l_id=list_id,user_id=user_id).first()
            c=Card.query.filter_by(c_id=card_id,list_id=list_id).first()
            uy= List.query.filter_by(l_id=lis_id,user_id=user_id).first()

            if u:
                if li:
                    if c:  

                        if not uy:
                            raise MovementNotAllowedError(status_code=400)
                        if c.comp!="comp":
                            if completed=="comp":
                                c.d=str(date.today()) 
                                        
                        c.c_name=c_name
                        c.cont=content
                        c.comp=completed
                        c.deadline=deadline    
                        c.list_id=lis_id            
                        db.session.commit()
                        ca=Card.query.filter_by(c_id=card_id,list_id=lis_id).first()
                        return ca, 200
                    else:
                        raise CardNotFoundError(status_code=404)    
                else:
                    raise InvalidListError(status_code=404)           
                     
            else:
                raise UserNotFoundError(status_code=404)                                     
          
#********************************************************************************************
class Summaryapi(Resource):
    def get(self,user_id):

        u=Users.query.filter_by(id_=user_id).first()
        lis=List.query.filter_by(user_id=user_id).all()

        #k=dict()
        if u:
            if lis:
                z=[]
                for l in lis:
                    pl=l.l_id
                    n=l.l_name
                    #k[pl]=[]
                    #k[pl].append(n)
                    car=Card.query.filter_by(list_id=l.l_id).all()
                    t=0
                    s=0
                    p=0
                    c=0
                    f=0
                    if car:
                        for cr in car:
                            if cr:
                                ddl=cr.deadline  
                                td=str(date.today())
                                t+=1
                                if ddl<td and cr.comp==None:
                                    f+=1
                                elif ddl>=td and cr.comp==None:
                                    p+=1
                                elif ddl<td and cr.comp=="comp":
                                    s+=1
                                elif ddl>=td and cr.comp=="comp":
                                    c+=1
                            else:
                                continue     
                    else:
                        ob2={
                            "list_id":pl,
                            "list_name":n,
                            "total_cards":0,
                            "cards_that_crossed_deadline":0,
                            "completed":c,
                            "successfully_submitted":0,
                            "pending":0,
                            "failed_to_submit":0

                        }
                        z.append(ob2)  
                        continue  
                    #complet=s+c   
                    #incomp=f+p
                    crosd=s+f
                
                    ob={
                        
                        "list_name":n,
                        "total_cards":t,
                        "cards_that_crossed_deadline":crosd,
                        "completed":c,
                        "successfully_submitted":s,
                        "pending":p,
                        "failed_to_submit":f
                    }
                    z.append(ob)
                return z, 200
            else:
                raise NoListError(status_code=404)
        else:
            raise UserNotFoundError(status_code=404)        