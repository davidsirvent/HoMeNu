""" User Interface for menu management """

from flask import (Blueprint, render_template, request, flash, url_for, redirect, g)
from datetime import datetime
from Modeling.menu import M_Menu
from Modeling.dish import M_Dish
from Modeling.meal import M_Meal
from Modeling import error
from Logical import (L_Menu, L_Meal, L_Dish, utils)
from . import UI_User


ui = Blueprint('UI_Menu', __name__, url_prefix='/menu')


@ui.route('/card', methods=('GET', 'POST'))
@ui.route('/card//undefined/undefined', methods=('GET', 'POST'))
@UI_User.login_required
def card():
    """
    Just redirects to current day
    """
    date_raw = datetime.now()    
    return redirect(url_for('.card_day', year=str(date_raw.year), month=str(date_raw.month), day=str(date_raw.day)))


@ui.route('/card/<year>/<month>/<day>', methods=('GET', 'POST'))
@UI_User.login_required
def card_day(year: str, month: str, day: str):

    # Add leading zero if needed.    
    day = '{:02d}'.format(int(day))
    month = '{:02d}'.format(int(month))

    # Preparing date    
    date = {
        'day': day,
        'month': month,
        'year': year
    }
    date_tmp = day + '-' + month + '-' + year

    # Button control
    if 'save_button' in request.form:                
        date_dmy = utils.parse_date(request.form['date'])  # Date: Day-Month-Year        
        meal = request.form['meal-id']
        dish = request.form['dish']

        if meal == 'None':
            flash(error.Meal_not_selected)
        else:
            try:
                L_Menu.save(M_Menu(g.user.email, date_dmy, None, meal, dish))
                flash(error.Saved_Successfully)
            except RuntimeError as err:
                flash(err.args[0])

    if 'delete_button' in request.form:
        date_dmy = utils.parse_date(request.form['date'])
        meal = request.form['meal-id']
        dish = request.form['delete_button']

        try:
            L_Menu.delete(M_Menu(g.user.email, date_dmy, None, meal, dish))
            flash(error.Deleted_Successfully)            
        except RuntimeError as err:
            flash(err.args[0])
        

    # Mount menu list
    try:
        data_menu = list()
        for menu_item in L_Menu.select(M_Menu(g.user.email, date_tmp, None, None, None)):
            meal_item = L_Meal.select(M_Meal(g.user.email, menu_item.meal, None))[0]
            dish_item = L_Dish.select(M_Dish(g.user.email, menu_item.dish, None))[0]
            data_menu.append([meal_item.name, meal_item.background_color, dish_item.code, dish_item.name])
    except RuntimeError as err:
        pass

    # Mount meal list
    try:
        data_meal = list()
        for item in L_Meal.select(M_Meal(g.user.email, None, None)):
            data_meal.append([item.name, item.background_color])
    except RuntimeError as err:
        pass

    # Mount dish list
    try:
        data_dish = list()
        for item in L_Dish.select(M_Dish(g.user.email, None, None)):
            data_dish.append([item.code, item.name])
    except RuntimeError as err:
        pass

    return render_template('UI_Menu/card.html', date=date, data_meal=data_meal, data_dish=data_dish, data_menu=data_menu)
