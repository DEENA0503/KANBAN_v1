from flask import render_template, session, redirect, request, flash, url_for
from application.models import db
from application.models import Users, List, Card
from datetime import date
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('AGG')
from flask import current_app as app



@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        passw=request.form["passw"]
        session["name"]=name
        session["email"]=email
        session["passw"]=passw
       
        found_usr=Users.query.filter_by(name=name, email=email, passw=passw).first()
        #td=(date.today())
        
        if found_usr:
            #uid=found_usr.id_
            return redirect(url_for("user"))
        else:
            fnd_usr=Users.query.filter_by(name=name, email=email).first()
            if fnd_usr:
                flash(message="Incorrect password, please try again!", category="info")
                return render_template("log.html")##
            fnd_usrs=Users.query.filter_by(name=name).all()
            if fnd_usrs:
                flash(message="Incorrect details, please try again!", category="info")
                return render_template("log.html")  
            else:       
                flash(message="Not a user! Please signup to create a new account", category="info")
                return render_template("log.html")                 
    else:   
        if "name" in session:
            return redirect(url_for("user"))
        else:
            return render_template("log.html")
#************************************************************************************************************
                    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        passw=request.form["passw"]
        
        fnd_usr=Users.query.filter_by(name=name, email=email, passw=passw).first()
        if fnd_usr:
            flash(message="Already a user, please login!", category="info")
            return render_template("log.html")

        fd_usr=Users.query.filter_by( email=email).first()
        if fd_usr:
            flash(message="Email id is not unique.", category="info")
            return render_template("log.html")    

        usr=Users(name=name, email=email, passw=passw)
        db.session.add(usr)
        db.session.commit()
        session["name"]=name
        session["email"]=email
        session["passw"]=passw
        fd_usr=Users.query.filter_by(name=name, email=email, passw=passw).first()
        _id_=fd_usr.id_   
        flash(message="Account created! Please add a list.", category="info")
        return redirect(url_for("add_list", user=_id_))    
    else:   
        if "name" in session:
            return redirect(url_for("user"))
        else:
            return render_template("log.html")
#**************************************************************************************************************

@app.route("/user", methods=["GET"])
def user(): 
    name=session["name"]
    email=session["email"]
    passw=session["passw"]
    f_usr=Users.query.filter_by(name=name, email=email,passw=passw).first()
    _id_=f_usr.id_
    n=f_usr.name
    ls=List.query.filter_by(user_id=_id_).all()
   
    if request.method=="GET":
        if ls:
            cards={}
            for l in ls:
                cards[l]=Card.query.filter_by(list_id=l.l_id).all()
            no=len(ls)
            td=str(date.today())
            return render_template("users.html", user_id=_id_, u_name=n,ls=ls,cards=cards, td=td)
        else:
            flash(message="You have no lists in your account, please add a list to continue.", category="info")
            return redirect(url_for("add_list", user=_id_))   

    
 #*************************************************************************************************************************   

@app.route("/<user>/add_list", methods=["GET","POST"])     
def add_list(user):
    if request.method=="POST":
        l_name=request.form["l_name"] 
        dsp=request.form["dsp"]
       
        li=List(user_id=user, l_name=l_name, dsp=dsp)
        db.session.add(li)
        db.session.commit()
        return redirect(url_for("user"))
    if request.method=="GET":
        f_usr=Users.query.filter_by(id_=user).first()
        n=f_usr.name
        #td=str(date.today())
        return render_template("add_list.html", u_name=n,user_id=user)        
#**************************************************************************************************************************

@app.route("/<user>/<l_id>/add_card", methods=["GET","POST"])
def add_card(user,l_id):
    f_usr=Users.query.filter_by(id_=user).first()
    n=f_usr.name
    ls=List.query.filter_by(user_id=user, l_id=l_id).first()
    lis=List.query.filter_by(user_id=user).all()
    
    if request.method=="GET":
        td=str(date.today())
        
        return render_template("add_card.html",ls=lis,l_name=ls.l_name,u_name=n, user_id=user,td=td)
    if request.method=="POST":
        card_name=request.form["card_name"]
        cont=request.form["cont"]
        comp = request.form.get("done")
        deadline=request.form["deadline"]
        cr=Card(c_name=card_name, cont=cont, comp=comp, deadline=deadline,list_id=l_id)
        db.session.add(cr)
        db.session.commit()
        return redirect(url_for("user"))  
#**************************************************************************************************************

@app.route('/user/<l_id>/del_lis')
def del_lis(l_id):
    ln=List.query.filter_by(l_id=l_id).first()
    user=ln.user_id
    f_usr=Users.query.filter_by(id_=user).first()
    c=Card.query.filter_by(list_id=l_id).all()
    td=str(date.today())
    card=len(c)
    lis=List.query.filter_by(user_id=user).all()
    return render_template("alert.html",ln=ln,user_id=user,u_name=f_usr.name,ls=lis,card=card)
#********************************************************************************************************************
@app.route('/user/<l_id>/del_li', methods=["POST"])
def del_li(l_id):
    if request.method=="POST":
        list=List.query.filter_by(l_id=l_id).first()
        n=list.l_name
        if list is not None:
            db.session.delete(list)
            db.session.commit()
            flash(message=f"The list {n} was deleted with all its cards.", category="info")
            return redirect(url_for("user"))
        else:
            flash(message="The list you tried to delete does not exist!", category="info",user_id=user)
            return redirect(url_for("user"))
#******************************************************************************************************************

@app.route('/user/<l_id>/<c_id>/del_cr')
def del_cr(l_id,c_id):
    card=Card.query.filter_by(c_id=c_id,list_id=l_id).first()
    cn=card.c_name
    if card is not None:
        db.session.delete(card)
        db.session.commit()
        flash(message=f"You have deleted {cn} card.", category="info")
        return redirect(url_for("user"))
    else:
        flash(message="The card you tried to delete does not exist!", category="info")
        return redirect(url_for("user"))
#***************************************************************************************************************

@app.route('/<users>/<l_id>/edit_li', methods=["GET","POST"])
def edit_li(users,l_id):
    if request.method=="GET": 
        l=List.query.filter_by(l_id=l_id).first()
        user=l.user_id
        f_usr=Users.query.filter_by(id_=user).first()
        lis=List.query.filter_by(user_id=user).all()
        return render_template("edit_li.html", l=l,u_name=f_usr.name,user_id=user,ls=lis)
    if request.method=="POST":
        lis=List.query.filter_by(l_id=l_id).first()
    
        lis.l_name=request.form["l_name"]
        lis.dsp=request.form["dsp"]
        db.session.commit()
        return redirect(url_for("user"))
#**************************************************************************************************************************

@app.route('/<l_id>/<c_id>/edit_card', methods=["GET","POST"])
def edit_card(l_id,c_id):
    if request.method=="GET":
        cr=Card.query.filter_by(c_id=c_id,list_id=l_id).one()
        la=List.query.filter_by(l_id=l_id).first()
        
        car=Card.query.filter_by(list_id=l_id).all()
        f_usr=Users.query.filter_by(id_=la.user_id).first()
        
        #td=str(date.today())
        return render_template("edit_card.html",la=la,cr=cr,u_name=f_usr.name,car=car,user_id=la.user_id)
    if request.method=="POST":
        c=Card.query.filter_by(c_id=c_id,list_id=l_id).one()
        c.c_name=request.form["card_name"]
        c.cont=request.form["cont"]
        if c.comp!="comp":
            if request.form.get("done")=="comp":
                 c.d=str(date.today())
        c.comp = request.form.get("done")
        c.deadline=request.form["deadline"]
    
        #c.d=str(date.today())
        db.session.commit()
        return redirect(url_for("user"))  
#*****************************************************************************************************************************

@app.route('/user/<l_id>/<c_id>/move_card', methods=["POST"])
def move_card(l_id,c_id):
    if request.method=="POST":
        c=Card.query.filter_by(c_id=c_id).first()
        
        li_id=request.form["l_id"]
        
        c.list_id=li_id#or=l_id
        db.session.commit()
        return redirect(url_for("user"))
#******************************************************************************************************************
@app.route('/user/<l_id>/move_cards', methods=["POST"])
def move_cards(l_id):
    if request.method=="POST":        
        li_id=request.form["l_id"]
        list2=List.query.filter_by(l_id=li_id).first()
        n2=list2.l_name
        cars=Card.query.filter_by(list_id=l_id).all()
        for cr in cars:
            cr.list_id=li_id
            db.session.commit()
        list=List.query.filter_by(l_id=l_id).first()
        n=list.l_name
        db.session.delete(list)
        db.session.commit()
        flash(message=f"The list {n} was deleted and its cards were moved to the list {n2}. ", category="info")
        return redirect(url_for("user"))    
#********************************************************************************************************************

@app.route("/<user>/summary")
def summary(user):
    
    lis=List.query.filter_by(user_id=user).all()
    k=dict()
    f_usr=Users.query.filter_by(id_=user).first()
    n=f_usr.name
    
    if lis is not None :
        for l in lis:
            pl=l.l_id
            n=l.l_name
            k[pl]=[]
            k[pl].append(n)
            car=Card.query.filter_by(list_id=l.l_id).all()
            t=0
            s=0
            p=0
            c=0
            f=0
            for cr in car:
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
            complet=s+c   
            incomp=f+p
            crosd=s+f

            k[pl].append(str(c))
            k[pl].append(str(p))
            
            k[pl].append(str(s))
            k[pl].append(str(f))
            k[pl].append(str(t))
            k[pl].append(str(crosd))

            y = [s, f, p, c]
            mylabels = ["succes", "failed to submit", "pending", "completed"]
            ci=["#a2f9aa", "#880e4f", "#f50057", "#4CAF50"]
            plt.bar(mylabels,y, width=0.4,color=ci)
           
            plt.title(n)
            plt.xlabel("status")
            plt.ylabel(f"no. of tasks out of total {t}")
            plt.savefig(f"static\{pl}.png", dpi=80)
            plt.title('{n}')
            plt.clf()    
    return render_template("summary.html",u_name=f_usr.name, user_id=user,k=k)
    
#**********************************************************************************************************************

@app.route("/logout")
def logout():   
    session.pop("name", None)
    session.pop("email", None)##
    session.pop("passw", None)##
    return redirect(url_for("login"))
#*********************************************************************