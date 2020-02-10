""" User Interface for dish management """

from flask import (Blueprint, render_template, request, flash, g)
from Modeling.dish import M_Dish
from Modeling import error
from Logical import L_Dish
from . import UI_User


ui = Blueprint('UI_Dish', __name__, url_prefix='/dish')

@ui.route('/card', methods=('GET', 'POST'))
@UI_User.login_required
def card():

    if request.method == 'POST':
        if 'save_button' in request.form:
            code = request.form['code']
            name = request.form['name']

            try:
                L_Dish.save(M_Dish(g.user.email, code.upper(), name))
                flash(error.Saved_Successfully)            
            except RuntimeError as err:
                flash(err.args[0])
    
        if 'delete_button' in request.form:
            code = request.form['code']

            try:
                L_Dish.delete(M_Dish(g.user.email, code.upper(),''))
                flash(error.Deleted_Successfully)            
            except RuntimeError as err:
                flash(err.args[0])


    # Mount dish list
    try:
        data = list()    
        for item in L_Dish.select(M_Dish(g.user.email, None, None)):        
            data.append([item.code, item.name])
    except RuntimeError as err:       
        pass
        
    return render_template('UI_Dish/card.html', data =  data)