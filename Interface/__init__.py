"""Interface layer"""

import os
from datetime import (datetime, timedelta)

from flask import (Flask, render_template, redirect, url_for, g)
from Database import db
from Modeling.dish import M_Dish
from Modeling.meal import M_Meal
from Modeling.menu import M_Menu
from Logical import (L_Menu, L_Meal, L_Dish)
from . import UI_Dish
from . import UI_Meal
from . import UI_Menu
from . import UI_User


def create_app(test_config=None):
    """Flask app factory"""

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(                               
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)        
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    @app.route('/')
    @UI_User.login_required
    def calendar():        
        today_raw = datetime.utcnow()
        today = '{:02d}'.format(today_raw.day) + '-' + '{:02d}'.format(today_raw.month) + '-' + str(today_raw.year)

        first_day = datetime(2018, 12, 31)        
        last_day = datetime(2020, 12, 31)
        time_delta = timedelta(days=1)       

        # Calendar mounting        
        cal = list()
        opacity = 'past'
        while first_day <= last_day:
            date_str = '{:02d}'.format(first_day.day) + '-' + '{:02d}'.format(first_day.month) + '-' + str(first_day.year)
            weekday = datetime(first_day.year, first_day.month, first_day.day).weekday()
            
            if date_str == today:
                opacity = ''
                today = 'today'

            # Fetch all menu items in a day
            try:
                menu_select = L_Menu.select(M_Menu(g.user.email, date_str, None, None, None))
                menu_list = list()
                for menu_item in menu_select:
                    meal_tmp = L_Meal.select(M_Meal(g.user.email, menu_item.meal, None))[0]
                    dish_tmp = L_Dish.select(M_Dish(g.user.email, menu_item.dish, None))[0]
                    menu_dict = {
                        'bg_color' : meal_tmp.background_color,
                        'dish' : dish_tmp.name
                    }
                    menu_list.append(menu_dict)
            except:                
                menu_list = ''  # When no menu items

            # Mount a day
            day_tmp = {
                'date' : date_str,
                'menu' : menu_list,
                'opacity' : opacity,
                'today' : today,
                'weekday': weekday
            }

            cal.append(day_tmp)
            first_day = first_day + time_delta  # Move to next day

        return render_template('calendar.html', cal=cal)


    # Blueprints registering
    app.register_blueprint(UI_Dish.ui)
    app.register_blueprint(UI_Meal.ui)
    app.register_blueprint(UI_Menu.ui)
    app.register_blueprint(UI_User.ui)

    '''
    @app.route('/_reset_db')
    def reset_db():
        db._reset_db()
        return redirect(url_for('UI_User.login'))
    '''
    
    '''
    @app.route('/_debug')
    def debug():
        from Database import DB_Mail
        cfg = DB_Mail.select()
        msg = DB_Mail.select('test')        
        return msg.format('hola')
    '''
    
    '''
    from werkzeug.security import check_password_hash, generate_password_hash
    @app.route('/_demoHash')
    def demo_hash():
        return generate_password_hash('demo')
    '''

    return app
    