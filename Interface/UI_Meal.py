""" User Interface for meal management """

from flask import (Blueprint, render_template, request, flash, g)
from Modeling.meal import M_Meal
from Modeling import error
from Logical import L_Meal
from . import UI_User

ui = Blueprint('UI_Meal', __name__, url_prefix='/meal')

@ui.route('/card', methods=('GET', 'POST'))
@UI_User.login_required
def card():

    if request.method == 'POST':
        if 'save_button' in request.form:
            name = request.form['name']
            background_color = request.form['bg-color']

            try:
                L_Meal.save(M_Meal(g.user.email, name.upper(), background_color))
                flash(error.Saved_Successfully)            
            except RuntimeError as err:
                flash(err.args[0])

        if 'delete_button' in request.form:
            name = request.form['name']

            try:
                L_Meal.delete(M_Meal(g.user.email, name.upper(), ''))
                flash(error.Deleted_Successfully)            
            except RuntimeError as err:
                flash(err.args[0])

    # Mount meal list
    try:
        data = list()    
        for item in L_Meal.select(M_Meal(g.user.email, None, None)):        
            data.append([item.name, item.background_color])
    except RuntimeError as err:       
        pass

    return render_template('UI_Meal/card.html', data = data)